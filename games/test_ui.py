import context
from pygamengine import *
from pygamengine.ui import *
import os

from pygamengine.ui.ui_element import Anchor

class MovingButton(Button):
    def __init__(self, name: str, position: tuple[float, float] = ..., size: tuple[float, float] = ..., anchor=Anchor.CENTER) -> None:
        super().__init__(name, position, size, anchor=anchor)
        self.speed = 0.5
        self.direction = 1
        
    def tick(self):
        super().tick()
        pos = self.get_position()
        if pos[0] > Ngine.display[0] - self.width:
            self.direction = -1
        if pos[0] < 0:
            self.direction = 1
        self.set_position(Transform.get_vectors_sum(self.get_position(),(self.direction * self.speed,0)))

if __name__ == "__main__":
    # Create simple button
    button = Button("b", (30, 30), size=(200,100), anchor=Anchor.TOP_LEFT)
    button.count = 0

    def on_button_click():
        button.count += 1
        button.text.set_update(f"You clicked {button.count} times!")
        button.move(0,1)
    
    button.on_click = on_button_click
    Ngine.create_new_gameobject(button)
    
    # Create Simple text
    button_position = button.get_position()
    text = Text("Mytext", (button_position[0] + button.width + 30, 30), anchor=Anchor.TOP_LEFT)
    text.text = "I'm a test text..a very very long text about sadness in this empty screen made exactly to contain me"
    Ngine.create_new_gameobject(text)

    # Create button with sprite images
    button_sprite_folder = "src/sprites/ui/buttons"
    button2 = Button(
        "sprite_b", (text.get_position()[0] + text.width + 30, 30), 
        unselected_image=os.path.join(button_sprite_folder, "Button_7_unselected.png"),
        selected_image=os.path.join(button_sprite_folder, "Button_7_unselected.png"),
        pressed_image=os.path.join(button_sprite_folder, "Button_7_pressed.png"),
        has_text=False,
        anchor=Anchor.TOP_LEFT
    )
    Ngine.create_new_gameobject(button2)

    # Create Panel
    panel = Panel("mypanel", (button2.get_position()[0] + button2.width + 30, 30), 
        (100, 300), (255,255,0), anchor=Anchor.TOP_LEFT, border=10, border_color=(255,0,0)
    )

    Ngine.create_new_gameobject(panel)
    
    text2 = Text("panel_description", Transform.get_vectors_sum(panel.get_position(), 
        (0, panel.height + 30)), text="This one above is a panel", anchor=Anchor.TOP_LEFT
    )
    text2.max_width = panel.width
    Ngine.create_new_gameobject(text2)

    # Create Panel
    textpanel = TextPanel(
        "mytextpanel", 
        "This text is inside this magical text panel\nAnd this is on another line", 
        (panel.get_position()[0] + panel.width + 30, 30), 
        (100, 300), (0,255,0), anchor=Anchor.TOP_LEFT
    )
    textpanel.text.color = (0,0,255)
    Ngine.create_new_gameobject(textpanel)

    Ngine.create_new_gameobject(MovingButton("my_moving_button", position=(button.get_position()[0], button.get_position()[1] + button.height + 30), size=(200,100), anchor=Anchor.TOP_LEFT))
    
    Ngine.run_engine()