from pygamengine.ui.ui_element import Anchor
from .panel import Panel
from .text import Text
from .ui_element import Anchor
from typing import Union
from pygamengine.transform import Transform

class TextPanel(Panel):
    def __init__(self, name: str, text: str = "Insert here your text", position: tuple[float, float] = (100,100), size: Union[tuple[float, float], None] = (100,100), background: Union[str | tuple[int, int, int, int]] = (255,255,255,255), anchor=Anchor.CENTER,
            padding_top: float = 5, padding_right: float = 5, padding_bottom: float = 5, padding_left: float = 5 
        ) -> None:
        super().__init__(name, position, size, background, anchor)
        self.padding = {"top": padding_top, "left": padding_left, "right": padding_right, "bottom": padding_bottom}
        self.text = Text(
            f"{name}_text", (position[0] + padding_left, position[1] + padding_top), text=text, anchor=Anchor.TOP_LEFT
        )
        self.text.max_width = self.width - padding_left - padding_right
        self.children.append(self.text)
    
    def tick(self):
        # super().start()
        self.text.set_position(
            Transform.get_vectors_sum(self.get_position(), (self.padding["left"], self.padding["top"]))
        )
