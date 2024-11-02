from .engine import PyGameNgine, PygameObject
from .gameobject import GameObject, Rectangle, Text
from .transform import Transform
from .background import Background
import pygamengine.input as Input

Ngine = PyGameNgine()

__all__ = [
    "PyGameNgine",
    "PygameObject",
    "Ngine",
    "Background",
    "Transform",
    "GameObject",
    "Rectangle",
    "Text",
    "Input"
    ]

__version__ = "0.1.2"