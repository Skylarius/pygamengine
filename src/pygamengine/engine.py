from __future__ import annotations
from typing import Callable
from .gameobject import GameObject, Rectangle, Text
from .event import EventSystem
from .custom_events import ColliderEnabledChangedData, ColliderEnabledChangedEventType
from .custom_events import NewObjectCreated, ObjectDeleted, GameObjectData
from .exceptions import GameObjectNotFoundError
import pygame
from pygame.locals import *
import sys
from .design_patterns import Singleton
from .coroutines import CoroutineSystem
import logging
from threading import Thread

class PygameObject(pygame.sprite.DirtySprite):
    def __init__(self, gameobject: GameObject, image: pygame.Surface) -> None:
        pygame.sprite.DirtySprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.image.convert()
        self.gameobject = gameobject
        self.__original_image = image
        self.__has_start_executed = False
        self.__filtered_collidable_objects_cache = list[PygameObject]()
        logging.basicConfig(level=logging.DEBUG)

    def update(self) -> None: # Overriding pygame.sprite.DirtySprite.update
        # Start
        if not self.has_started():
            self.gameobject.start()
            self.set_as_started()
        # Tick
        self.gameobject.tick()

        # Handle texts
        if isinstance(self.gameobject, Text) and self.gameobject.mark_as_to_update:
            txt: Text = self.gameobject
            self.image = txt.font.render(txt.text, False, txt.color)
            self.update_original_image(self.image)
            txt.mark_as_to_update = False
        
        # Update transforms in game_objects
        self.rect.center = self.gameobject.transform.get_position()
        self.update_rotation_and_scale()

        # Handle collisions
        self.handle_collisions()

        self.dirty = self.gameobject.transform.is_dirty_and_then_clean()

        self.debug()
    
    def debug_draw_rect(self, color: tuple[4]):
        image = self.image
        pygame.draw.rect(image, color, pygame.rect.Rect(0, 0, image.get_size()[0], 2))
        pygame.draw.rect(image, color, pygame.rect.Rect(0, 0, 2, image.get_size()[1]))
        pygame.draw.rect(image, color, pygame.rect.Rect(image.get_size()[0]/2 - 2, image.get_size()[1]/2 - 2, 2, 2))
        pygame.draw.rect(image, color, pygame.rect.Rect(0, image.get_size()[1] - 2, image.get_size()[0], 2))
        pygame.draw.rect(image, color, pygame.rect.Rect(image.get_size()[0] - 2, 0, 2, image.get_size()[1]))
    
    def debug_draw_rect_condition(self, color: tuple[4], condition_func: Callable[[PygameObject], bool]):
        if condition_func(self):
            self.image.fill(color)
    
    def get_screen_position(self) -> tuple[2]:
        position = self.gameobject.transform.get_position()
        return (position[0] - self.image.get_width()/2, position[1] - self.image.get_height()/2)
    
    def debug(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RALT]: 
            self.debug_draw_rect((255,0,0,255))
        if keys[pygame.K_RCTRL]:
            self.debug_draw_rect_condition((255,0,0,255), lambda x: x.dirty)
    
    def has_started(self) -> bool:
        return self.__has_start_executed

    def set_as_started(self):
        self.__has_start_executed = True
    
    def is_colliding_with(self, other: PygameObject):
        rect1 = self.get_collision_rect()
        rect2 = other.get_collision_rect()
        return rect1.colliderect(rect2)
    
    def get_collision_rect(pygameobj: PygameObject) -> pygame.Rect:
        collider_size = None
        if pygameobj.gameobject.collider.size != (0,0):
            collider_size = pygameobj.gameobject.collider.size
        else:
            collider_size = pygameobj.image.get_size()
        position = pygameobj.get_screen_position()
        return pygame.Rect(position + collider_size)
    
    def update_rotation_and_scale(self):
        center = self.rect.center
        image = self.__original_image
        image = pygame.transform.rotate(
            image,
            self.gameobject.transform.get_rotation()
        )
        image = pygame.transform.scale_by(
            image,
            self.gameobject.transform.get_scale()
        )
        self.image = image
        self.rect = self.image.get_rect(center=center)

    def invalidate_filtered_collidable_objects_cache(self):
        self.__filtered_collidable_objects_cache.clear()
    
    def is_collider_ignored(self, other: PygameObject) -> bool:
        for c in self.gameobject.collider.ignored_colliders:
            if isinstance(other.gameobject, c):
                return True
        return False

    def handle_collisions(self):
        if not self.gameobject.collider.is_enabled():
            return
        if len(self.__filtered_collidable_objects_cache) == 0:
            self.__filtered_collidable_objects_cache = Ngine.get_filtered_collidable_objects(self)
        for pyobj2 in self.__filtered_collidable_objects_cache:
            if self == pyobj2:
                continue
            if pyobj2 is None:
                continue
            if self.is_collider_ignored(pyobj2):
                continue
            if self.is_colliding_with(pyobj2):
                self.gameobject.on_collision(pyobj2.gameobject)
    
    def update_original_image(self, new_image: pygame.Surface):
        self.__original_image = new_image
        self.__original_image.convert()


class PyGameNgine(metaclass=Singleton):
    def __init__(self) -> None:
        self.tick_time = 60
        self.__pygameobjects = list[PygameObject]()
        self.__pygameobjects_marked_for_deletion = list[PygameObject]()
        self.__collidable_objects = list[PygameObject]()
        self.__all_sprites: pygame.sprite.LayeredDirty = None
        pygame.init()
        self.__clock = pygame.time.Clock()
        # flags = FULLSCREEN | DOUBLEBUF
        
        self.set_display(1280, 720)

        # Start CoroutineSystem
        self.__coroutine_system = CoroutineSystem()

        self.setup_event_system()
    
    def set_display(self, x: int, y: int):
        # Create The Backgound
        flags = DOUBLEBUF
        # flags = FULLSCREEN | DOUBLEBUF
        self.display = x, y
        self.__screen = pygame.display.set_mode(self.display, flags, 16)
        self.__background = pygame.Surface(self.__screen.get_size())
        r = self.__background.get_rect()
        self.__background.convert()
        self.__background.fill(0)
    
    def setup_event_system(self):
        event_system = EventSystem()

        def collider_enabled_changed_callback(data: ColliderEnabledChangedData):
            game_object = data.get_game_object()
            pygameobject: PygameObject = self.__get_pygameobject(game_object)
            if pygameobject is None:
                logging.warning("PygameObject Not Found: Do not enable/disable the collider in __init__. Do it in start()")
                return
            if data.get_condition():
                self.add_collidable(pygameobject)
            else:
                self.remove_collidable(pygameobject)
                
        event_system.subscribe(ColliderEnabledChangedEventType, collider_enabled_changed_callback)

        def invalidate_filtered_collidable_objects_cache_all(data: GameObjectData):
            gameobject = data.get_game_object()
            pygameobject_of_event = self.__get_pygameobject(gameobject)
            if pygameobject_of_event is None:
                raise GameObjectNotFoundError("Couldn't find Pygameobject passed on this event as GameObject")
            for pygameobject in self.__pygameobjects:
                if not pygameobject.is_collider_ignored(pygameobject_of_event):
                    logging.debug(f"Filtered collidable cache invalidated for {pygameobject.gameobject}")
                    pygameobject.invalidate_filtered_collidable_objects_cache()
        
        event_system.subscribe(NewObjectCreated.event_type, invalidate_filtered_collidable_objects_cache_all)
        event_system.subscribe(ObjectDeleted.event_type, invalidate_filtered_collidable_objects_cache_all)
    
    def game_over(self):
        pygame.quit()
        sys.exit()
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen
    
    def add_collidable(self, pygameobject: PygameObject):
        if pygameobject not in self.__collidable_objects:
            self.__collidable_objects.append(pygameobject)

    def remove_collidable(self, pygameobject: PygameObject):
        if pygameobject in self.__collidable_objects:
            self.__collidable_objects.remove(pygameobject)

    def get_collidable_objects(self):
        return self.__collidable_objects
    
    def get_filtered_collidable_objects(self, pygameobject: PygameObject) -> list[PygameObject]:
        filtered_list = list[PygameObject]()
        for other in self.__pygameobjects:
            if other == pygameobject:
                continue
            found = False
            for cls in pygameobject.gameobject.collider.ignored_colliders:
                if isinstance(other.gameobject, cls):
                    found = True
                    break
            if found is False:
                filtered_list.append(other)
        return filtered_list
        
    def __get_pygameobject(self, gameobject: GameObject) -> PygameObject:
        '''
        Note: This will be able to get even gameobjects marked for deletion
        '''
        return next((pygo for pygo in self.__pygameobjects if pygo.gameobject == gameobject), None)

    def has_gameobject(self, gameobject: GameObject):
        return self.__get_pygameobject(gameobject) != None
    
    def get_gameobjects_by_name(self, name: str) -> list[PygameObject]:
        return [obj for obj in self.__pygameobjects if obj.gameobject.name == name and obj not in self.__pygameobjects_marked_for_deletion]
    
    def get_gameobjects_by_class(self, Class: type) -> list[PygameObject]:
        return [obj for obj in self.__pygameobjects if isinstance(obj.gameobject, Class) and obj not in self.__pygameobjects_marked_for_deletion]
    
    def handle_collisions_between_pygameobjects(self, pyobj1: PygameObject, pyobj2: PygameObject):
        if pyobj1.is_colliding_with(pyobj2):
            pyobj1.gameobject.on_collision(pyobj2.gameobject)
            pyobj2.gameobject.on_collision(pyobj1.gameobject)
    
    def __handle_collisions_all_objects_with_parallel_threads(self): # works like shit
        count = len(self.__pygameobjects)
        for i in range(0, count):
            pyobj1 = self.__pygameobjects[i]
            for j in range (i, count):
                pyobj2 = self.__pygameobjects[j]
                t = Thread(target=self.handle_collisions_between_pygameobjects, args=(pyobj1, pyobj2))
                t.run()
        # for t in tuples:
        #     handle_collisions_between_pygameobjects(*t)

    def create_new_gameobject(self, gameobject: GameObject) -> PygameObject:
        image = pygame.Surface((1,1))
        if isinstance(gameobject, Rectangle):
            # Generate rectangle image
            rectangle: Rectangle = gameobject
            image = pygame.Surface((rectangle.width, rectangle.height))
            rect = pygame.Rect(1, 1, rectangle.width - 1, rectangle.height -1)
            pygame.draw.rect(image, pygame.Color(*rectangle.color), rect)
        elif isinstance(gameobject, Text):
            # Create text
            text: Text = gameobject
            text.font = pygame.font.SysFont(None, 24)
            image = text.font.render(text.text, True, text.color)
        else:
            # Load sprite
            if gameobject.sprite:
                image = pygame.image.load(gameobject.sprite)
        image.convert()
        pygameobject = PygameObject(gameobject, image)
        pygameobject.rect.size = pygameobject.image.get_size()
        self.__pygameobjects.append(pygameobject)
        if self.__all_sprites:
            self.__all_sprites.add(pygameobject)
        NewObjectCreated(gameobject)
        logging.debug(f"+Created {gameobject}")
        return pygameobject
        
    
    def destroy(self, gameobject: GameObject):
        pygameobject = self.__get_pygameobject(gameobject)
        if pygameobject != None:
            self.__pygameobjects_marked_for_deletion.append(pygameobject)
            gameobject.on_destroy()
            ObjectDeleted(gameobject)
            logging.debug(f"-Deleted {gameobject}")
    
    def remove_objects_marked_for_deletion(self):
        for pygameobject in self.__pygameobjects_marked_for_deletion:
            if pygameobject in self.__pygameobjects:
                self.__pygameobjects.remove(pygameobject)
            if self.__all_sprites:
                self.__all_sprites.remove(pygameobject)
            if pygameobject in self.__collidable_objects:
                self.remove_collidable(pygameobject)
        self.__pygameobjects_marked_for_deletion.clear()
                
    
    def is_in_display(self, position: tuple[2]):
        return 0 < position[0] < self.display[0] and 0 < position[1] < self.display[1]

    def run_engine(self):
        # Prepare dirty sprites
        self.__all_sprites = pygame.sprite.LayeredDirty(self.__pygameobjects)
        
        # Display background
        self.__all_sprites.clear(self.__screen, self.__background)

        for pygameobject in self.__pygameobjects:
            pygameobject.rect.size = pygameobject.image.get_size()
        
        # Start infinite loop
        while True:
            # Execute Start and Tick (now using DirtySprite update function)
            self.__all_sprites.update()            
            
            # Draw Everything
            rects = self.__all_sprites.draw(self.__screen)
            pygame.display.update(rects)
            
            # Run Coroutines
            self.__coroutine_system.run_coroutines()

            # Handle all collisions (NO!)
            #self.__handle_collisions_all_objects_with_parallel_threads()

            # Delete all gameobjects marked for deletion
            self.remove_objects_marked_for_deletion()

            # Update
            pygame.event.pump() # process event queue
            self.__clock.tick(self.tick_time)


Ngine = PyGameNgine()