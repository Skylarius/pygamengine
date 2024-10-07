from .engine import PyGameNgine, PygameObject
from .gameobject import Transform, GameObject, Rectangle, Text
from .background import Background

Ngine = PyGameNgine()

__all__ = [
    "PyGameNgine",
    "PygameObject",
    "Ngine",
    "Background",
    "Transform",
    "GameObject",
    "Rectangle",
    "Text"
    ]

__version__ = "0.1.2"