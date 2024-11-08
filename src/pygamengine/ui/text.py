from .ui_element import UIElement, Anchor
from pygamengine.exceptions import ConstructionOrderError
from pygamengine.transform import Transform
import pygame

class Text(UIElement):
    def __init__(self, name: str, position: tuple[float, float] = (0,0), color=(240,240,240,255), anchor: Anchor = Anchor.CENTER) -> None:
        super().__init__(name, position, (1,1), anchor)
        self.font: pygame.font.Font = pygame.font.SysFont(None, 24)
        self.text = name
        self.color = color
        self.line_spacing = 10
        self.max_width = 300

    def construct(self):
        self.current_image = self.render_text()

    def render_text(self) -> pygame.Surface:
        width, height = 0, 0
        max_width = 0
        current_text = ""
        line_spacing = 0
        lines = []
        for word in self.text.split(' '):
            word_formatted = f"{word} "
            word_x, word_y = self.font.size(word_formatted)
            line_spacing = max(line_spacing, word_y)            
            if width + word_x < self.max_width:
                width += word_x
                current_text += word_formatted
            else:
                max_width = max(width, max_width)
                lines.append(current_text)
                height += line_spacing
                width = word_x
                current_text = f"{word} "
        max_width = max(max_width, width)
        height += line_spacing
        lines.append(current_text)
        self.width = max_width
        self.height = height
        rendered_text_image = pygame.surface.Surface((max_width, height), pygame.SRCALPHA)
        for h in range(0, len(lines)):
            rendered_line = self.font.render(lines[h], False, self.color)
            rendered_text_image.blit(rendered_line, (0, h*line_spacing))
        # rendered_text_image.convert_alpha()
        return rendered_text_image

    def update_text(self):
        if self.font is None:
            raise ConstructionOrderError("Text.font is None: maybe you're tryig to call update_text before the Ngine created the object...")
        # self.current_image = self.font.render(self.text, False, self.color)
        self.current_image = self.render_text()
        self.mark_as_to_update = True
        self.transform.force_update()

    def set_update(self, text: str):
        self.text = text
        self.update_text()