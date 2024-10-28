from pygame import Surface
from pygame import image as pygameimage

class SpriteCache:
    def __init__(self) -> None:
        self.__sprite_cache: dict[str, tuple[Surface, int]] = {}
        self.size = 15

    def load_sprite(self, sprite_path) -> Surface:
        if sprite_path not in self.__sprite_cache:
            if len(self.__sprite_cache) > self.size/2:
                items = self.__sprite_cache.items()
                min_count = min([v[1] for _, v in items])
                k_to_delete = []
                for k, v in items:
                    if v[1] == min_count:
                        k_to_delete.append(k)
                for k in k_to_delete:
                    del self.__sprite_cache[k]
            image = pygameimage.load(sprite_path)
            self.__sprite_cache[sprite_path] = (image, 0)
            return image
        image_and_count: tuple[Surface, int] = self.__sprite_cache[sprite_path]
        self.__sprite_cache[sprite_path] = (image_and_count[0], image_and_count[1] + 1)

        return image_and_count[0]
