from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygamengine import PygameObject

class Component:
    count = 0
    def __init__(self, name="component") -> None:
        self.name = f"{name}_{Component.count}"
        Component.count+=1

    def update(self, pygameobject: 'PygameObject'):
        pass