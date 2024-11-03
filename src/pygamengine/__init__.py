from .engine import PyGameNgine, PygameObject
from .gameobject import GameObject, Rectangle
from .ui.text import Text
from .transform import Transform
from .background import Background
from .input import Input

Ngine = PyGameNgine()

__all__ = [
    "PyGameNgine",
    "PygameObject",
    "Ngine",
    "Background",
    "Transform",
    "GameObject",
    "Rectangle",
    "Input",
    "Text"
    ]

__version__ = "0.1.2"