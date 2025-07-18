from .ui_element import UIElement, Anchor
from typing import Union
from pygamengine.exceptions import ConstructionOrderError
import pygame

class TextRenderer:
    def __init__(self, font: Union[pygame.font.Font, None], color=(240,240,240,255), max_width=100,
        max_lines=999, remove_lines_on_top: bool = False, fixed_width: bool = False) -> None:
        self.font = font or pygame.font.SysFont(None, 24)
        self.color = color
        self.max_width = max_width
        self.max_lines = max_lines
        self.remove_lines_on_top = remove_lines_on_top
        self.fixed_width = fixed_width
        self.init()

    def init(self):
        self.width = 0
        self.height = 0
        self.current_line_text = ""
        self.current_max_width = 0
        self.line_spacing = 0
        self.lines: list[str] = []

    def insert_word(self, word: str):
        new_current_line = self.current_line_text + word
        line_x, line_y = self.font.size(new_current_line)
        self.line_spacing = max(self.line_spacing, line_y)
        if line_x < self.max_width:
            self.width = line_x
            self.current_line_text = new_current_line
        else:
            self.make_new_line()
            self.width = self.font.size(word)[0]
            self.current_line_text = word

    def make_new_line(self):
        self.current_max_width = max(self.width, self.current_max_width)
        self.lines.append(self.current_line_text)
        self.height += self.line_spacing
        self.current_line_text = ""

    def render(self) -> pygame.Surface:
        #Clamp lines accordingly
        if len(self.lines) > self.max_lines:
            if self.remove_lines_on_top:
                self.lines = self.lines[len(self.lines) - self.max_lines:]
            else:
                self.lines = self.lines[:self.max_lines]
        width = self.current_max_width if not self.fixed_width else self.max_width
        height = self.height
        rendered_text_image = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        for h in range(0, len(self.lines)):
            rendered_line = self.font.render(self.lines[h], False, self.color)
            rendered_text_image.blit(rendered_line, (0, h*self.line_spacing))
        # rendered_text_image.convert_alpha()
        return rendered_text_image

class Text(UIElement):
    def __init__(self, name: str, position: tuple[float, float] = (0,0), color=(240,240,240,255),
                text: Union[str,None] = None, anchor: Anchor = Anchor.CENTER, max_width=300,
                max_lines = 999, remove_lines_on_top: bool = False, fixed_width: bool = False, font_size=24) -> None:
        super().__init__(name, position, (1,1), anchor)
        self.font: pygame.font.Font = pygame.font.SysFont(None, font_size)
        self.text = text or name
        self.color = color
        self.line_spacing = 10
        self.max_width = max_width
        self.max_lines = max_lines
        self.remove_lines_on_top = remove_lines_on_top
        self.fixed_width = fixed_width

    def construct(self):
        self.current_image = self.render_text()
        self.mark_as_to_update = True
        self.set_position(self.transform.get_position())
        self.transform.force_update()

    def set_font_size(self, size: int):
        self.font = self.font.__class__(None, size)

    def render_text(self) -> pygame.Surface:
        if self.text == None:
            return self.font.render("", False, self.color)
        renderer = TextRenderer(self.font, self.color, self.max_width, self.max_lines, self.remove_lines_on_top, self.fixed_width)
        word = ""
        for char in self.text:
            if char == " ":
                word+=char
                renderer.insert_word(word)
                word=""
            elif char == "\n":
                renderer.insert_word(word)
                renderer.make_new_line()
                word=""
            else:
                word+=char
        renderer.insert_word(word)
        renderer.make_new_line()
        image = renderer.render()
        self.width, self.height = image.get_size()
        return image

    '''
    Test: unused in deploy
    '''
    def render_text_alt(self) -> pygame.Surface:
        if self.text == None:
            return self.font.render("", False, self.color)
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
        lines.append(current_text)
        height += line_spacing

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

    def start(self):
        super().start()