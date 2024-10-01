from .engine import PyGameNgine
from .gameobject import Transform, GameObject, Rectangle, Text

Ngine = PyGameNgine()

__all__ = [
    "PyGameNgine",
    "Ngine",
    "Transform",
    "GameObject",
    "Rectangle",
    "Text"
    ]

__version__ = "0.1.1"