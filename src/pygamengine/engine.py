from __future__ import annotations
from typing import Callable
from .gameobject import GameObject, Rectangle
from .background import Background

from .ui.ui_element import UIElement
from .event import EventSystem
from .custom_events import ColliderEnabledChangedData, ColliderEnabledChangedEventType, ObjectLayerUpdated, CoroutineEnd, VideoResize
from .custom_events import NewObjectCreated, ObjectDeleted, ObjectStarted, ComponentAddedToObject, GameObjectData, ComponentData, EventData
from .components import Component
from .exceptions import GameObjectNotFoundError, ComponentNotFoundError, DisplayError
from .input import Input

import pygame
from pygame.locals import *
import sys
from .design_patterns import Singleton
from .coroutines import CoroutineSystem, WaitSeconds, Coroutine
import logging
from threading import Thread
from .caches import SpriteCache

class PygameObject(pygame.sprite.DirtySprite):

    sprite_cache = SpriteCache()

    def __init__(self, gameobject: GameObject, image: pygame.Surface) -> None:
        pygame.sprite.DirtySprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.image.convert()
        self.gameobject = gameobject
        self.__original_image = image
        self.__has_start_executed = False
        self.__filtered_collidable_objects_cache = list[PygameObject]()
        self.components: list[Component] = []
        self.dirty = False
        self.mark_as_to_update = False
        logging.basicConfig(level=logging.DEBUG)


    def update(self) -> None: # Overriding pygame.sprite.DirtySprite.update
        self.visible = self.gameobject.enabled
        # Tick
        if not self.gameobject.enabled:
            return
        
        self.gameobject.tick()

        if self.gameobject.mark_as_to_update:
            if isinstance(self.gameobject, UIElement):
                self.image = self.gameobject.current_image
            elif not isinstance(self.gameobject, Rectangle):
                self.image = PygameObject.sprite_cache.load_sprite(self.gameobject.sprite)
            self.update_original_image(self.image)
            self.mark_as_to_update = False
        
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
        if Input().get_key("RALT"): 
            self.debug_draw_rect((255,0,0,255))
        if Input().get_key("RCTRL"):
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
        if getattr(self.gameobject, 'collider', None) is None or not self.gameobject.collider.is_enabled():
            return
        if len(self.__filtered_collidable_objects_cache) == 0:
            self.__filtered_collidable_objects_cache = Ngine.get_filtered_collidable_objects(self)
        for pyobj2 in self.__filtered_collidable_objects_cache:
            if self == pyobj2:
                continue
            if not pyobj2.gameobject.enabled:
                continue
            if pyobj2 is None:
                continue
            if self.is_collider_ignored(pyobj2):
                continue
            if self.is_colliding_with(pyobj2):
                self.gameobject.on_collision(pyobj2.gameobject)
    
    def get_original_image(self) -> pygame.Surface:
        return self.__original_image
    
    def update_original_image(self, new_image: pygame.Surface):
        self.__original_image = new_image
        self.__original_image.convert()
    
    def add_component(self, component: Component):
        self.components.append(component)
        return component
    
    def remove_component(self, component: Component):
        self.components.remove(component)
    
    def get_component(self, component_type: type):
        for c in self.components:
            if isinstance(c, component_type):
                return c
        return None


class PyGameNgine(metaclass=Singleton):
    def __init__(self) -> None:
        self.tick_time = 60
        self.__pygameobjects = list[PygameObject]()
        self.__pygameobjects_marked_for_deletion = list[PygameObject]()
        self.__collidable_objects = list[PygameObject]()
        self.__all_sprites: pygame.sprite.LayeredDirty = None
        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__input = Input()
        # flags = FULLSCREEN | DOUBLEBUF
        self.__is_display_set = False
        self.__is_running = False
        self.__force_quit = False
        self.__display = None

        # Deprecated, do not use it
        self.display = (1280, 720)

        # Start CoroutineSystem
        self.__coroutine_system = CoroutineSystem()

        # Setup Caches
        self.sprite_cache = SpriteCache()

        self.setup_event_system()
    
    def set_caption(self, caption: str):
        pygame.display.set_caption(caption)
    
    def set_display(self, x: int, y: int, color: pygame.Color = 0, in_flags: int = 0, fullscreen: bool = False, resizable: bool = True, scaled: bool = True, vsync: bool = True):
        # Create The Backgound
        if in_flags > 0:
            flags = in_flags
        else:
            flags = DOUBLEBUF
            if fullscreen:
                flags |= FULLSCREEN
            if resizable:
                flags |= RESIZABLE
            if scaled and x == 1280 and y == 720:
                flags |= SCALED
        vsync_value = 0 if not vsync else 1
        # flags = FULLSCREEN | DOUBLEBUF
        self.display = x, y
        self.__display = x, y
        self.__display_flags = flags
        self.__display_vsync = vsync_value
        self.__screen = pygame.display.set_mode(self.__display, flags, 16, vsync=vsync_value)
        self.__background = pygame.Surface(self.__screen.get_size())
        r = self.__background.get_rect()
        self.__background.convert()
        self.__is_display_set = True
    
    def get_display(self):
        if not self.__display:
            raise DisplayError("Display not set at function call. Tip: don't call it on object's __init__() if you didn't explicitly use set_display(). Use start() instead.")
        return self.__display
    
    def set_background(self, background: Background):
        self.__background.blit(pygame.image.load(background.get_path(self.__display)), (0,0))
        self.__background.convert()
    
    def set_background_color(self, color: pygame.Color):
        self.__background.fill(color)

    def setup_default_display(self):
        self.set_display(1280, 720)
        self.set_background_color(0)
    
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
            gameobject: GameObject = data.get_game_object()
            pygameobject_of_event = self.__get_pygameobject(gameobject)
            if pygameobject_of_event is None:
                raise GameObjectNotFoundError("Couldn't find Pygameobject passed on this event as GameObject")
            for pygameobject in self.__pygameobjects:
                if not pygameobject.gameobject.is_collider_enabled():
                    continue
                if not pygameobject.is_collider_ignored(pygameobject_of_event):
                    logging.debug(f"Filtered collidable cache invalidated for {pygameobject.gameobject}")
                    pygameobject.invalidate_filtered_collidable_objects_cache()
        
        event_system.subscribe(NewObjectCreated.event_type, invalidate_filtered_collidable_objects_cache_all)
        event_system.subscribe(ObjectDeleted.event_type, invalidate_filtered_collidable_objects_cache_all)

        def execute_start_on_object(data: GameObjectData):
            gameobject: GameObject = data.get_game_object()
            pygameobject_of_event = self.__get_pygameobject(gameobject)
            if pygameobject_of_event is None:
                raise GameObjectNotFoundError("Couldn't find Pygameobject passed on this event as GameObject")
            # Start
            if not pygameobject_of_event.has_started():
                pygameobject_of_event.gameobject.start()
                pygameobject_of_event.set_as_started()
        
        event_system.subscribe(ObjectStarted.event_type, execute_start_on_object)

        def execute_start_on_component(data: ComponentData):
            pygameobject: PygameObject = data.get_pygameobject()
            if pygameobject is None:
                raise GameObjectNotFoundError("Pygameobject is None")
            component: Component = data.get_component()
            if component not in pygameobject.components:
                raise ComponentNotFoundError("Component Not Found on Pygameobject")
            component.set_pygameobject(pygameobject)
            component.start()
        
        event_system.subscribe(ComponentAddedToObject.event_type, execute_start_on_component)

        def on_video_resize(new_size_data: EventData):
            logging.debug(f"New Video Size: {new_size_data.data}")
            # TODO: We don't need to reset the display for every video size event, but a game programmer might, so here an example
            # self.set_display(new_size_data.data[0], new_size_data.data[1], in_flags=self.__display_flags, vsync=self.__display_vsync)
        
        event_system.subscribe(VideoResize.event_type, on_video_resize)

    
    def game_over(self):
        self.__is_running = False
    
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
            if getattr(other.gameobject, 'collider', None) is None:
                 continue
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
    
    def __get_image_from_sprite_path(self, sprite_path) -> pygame.Surface:
        return self.sprite_cache.load_sprite(sprite_path)
    
    def refresh_all_objects(self):
        for pygameobject in self.__pygameobjects:
            pygameobject.gameobject.transform.force_update()
        
    def create_new_gameobject(self, gameobject: GameObject) -> PygameObject:
        if not self.__is_display_set:
            self.setup_default_display()
        additional_gameobjects_to_create = []
        image = pygame.Surface((1,1))
        if isinstance(gameobject, Rectangle):
            # Generate rectangle image
            rectangle: Rectangle = gameobject
            image = pygame.Surface((rectangle.width, rectangle.height))
            rect = pygame.Rect(1, 1, rectangle.width - 1, rectangle.height -1)
            pygame.draw.rect(image, pygame.Color(*rectangle.color), rect)
        elif isinstance(gameobject, UIElement):
            uielement: UIElement = gameobject
            uielement.construct()
            for child in uielement.children:
                additional_gameobjects_to_create.append(child)
            image = uielement.current_image
        else:
            # Load sprite
            if gameobject.sprite:
                image = self.__get_image_from_sprite_path(gameobject.sprite)
        image.convert()
        pygameobject = PygameObject(gameobject, image)
        pygameobject.rect.size = pygameobject.image.get_size()
        self.__pygameobjects.append(pygameobject)
        if self.__all_sprites:
            self.__all_sprites.add(pygame.sprite.LayeredDirty(pygameobject, layer=pygameobject.gameobject.draw_order))
        NewObjectCreated(gameobject)
        if Ngine.__is_running:
            ObjectStarted(gameobject)
        logging.debug(f"+Created {gameobject}")
        for g in additional_gameobjects_to_create:
            Ngine.create_new_gameobject(g)
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
    
    '''Update layer in gameobject. This must be called otherwise the layer change won't be effective'''
    def update_draw_order(self, gameobject: GameObject):
        pygameobject = self.__get_pygameobject(gameobject)
        if pygameobject != None:
            self.__all_sprites.change_layer(pygameobject, pygameobject.gameobject.draw_order)
            ObjectLayerUpdated(pygameobject.gameobject)         
    
    def is_in_display(self, position: tuple[2]):
        return 0 < position[0] < self.__display[0] and 0 < position[1] < self.__display[1]
    
    def add_new_component(self, component: Component, gameobject: GameObject):
        pygameobject = self.__get_pygameobject(gameobject)
        if pygameobject is None:
            raise GameObjectNotFoundError("Couldn't find Pygameobject passed on this event as GameObject. NB. Don't add components in __init__, use start()")
        c = pygameobject.add_component(component)
        ComponentAddedToObject(pygameobject, component)
        return c 
    
    def quit(self):
        self.__is_running = False if not self.__force_quit else sys.exit(0)

    def set_force_quit(self, value: bool):
        self.__force_quit = value


    def run_engine(self):
        # Prepare dirty sprites
        self.__all_sprites = pygame.sprite.LayeredDirty(self.__pygameobjects)

        # Execute start on all objects instanced before running
        for pygameobject in self.__pygameobjects:
            ObjectStarted(pygameobject.gameobject)
            self.__all_sprites.change_layer(pygameobject, pygameobject.gameobject.draw_order)
        
        # Display background
        self.__all_sprites.clear(self.__screen, self.__background)

        for pygameobject in self.__pygameobjects:
            pygameobject.rect.size = pygameobject.image.get_size()
        
        # Start infinite loop
        self.__is_running = True
        while self.__is_running:
            # Execute Start and Tick (now using DirtySprite update function)
            self.__all_sprites.update()
            
            # Draw Everything
            rects = self.__all_sprites.draw(self.__screen)
            pygame.display.update(rects)
            
            # Run Coroutines
            for ended_coroutine in self.__coroutine_system.run_coroutines():
                CoroutineEnd(ended_coroutine)


            # Handle all collisions (NO!)
            #self.__handle_collisions_all_objects_with_parallel_threads()

            # Delete all gameobjects marked for deletion
            self.remove_objects_marked_for_deletion()

            # Update
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == VIDEORESIZE:
                    pygame.display.update(self.__background.get_rect())
                    PyGameNgine().refresh_all_objects()
                    VideoResize(event.dict["size"])
                
            # Handle keys input:
            self.__input.update_pressed()

            self.__clock.tick(self.tick_time)
            # pygame.event.pump() # process event queue

Ngine = PyGameNgine()