import context
from pygamengine import *
from pygamengine.ui import Button, Text, Anchor, Panel
import os

if __name__ == "__main__":
    # Create simple button
    button = Button("b", (30, 30), size=(200,100), anchor=Anchor.TOP_LEFT)
    button.count = 0

    def on_button_click():
        button.count += 1
        button.text.set_update(f"You clicked {button.count} times!")
    
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
        (100, 300), (255,255,0), anchor=Anchor.TOP_LEFT
    )

    Ngine.create_new_gameobject(panel)
    
    text2 = Text("panel_text", Transform.get_vectors_sum(panel.get_position(), (0, panel.height + 30)), anchor=Anchor.TOP_LEFT )
    text2.text = "This one above is a panel"
    text2.max_width = panel.width
    Ngine.create_new_gameobject(text2)

    
    Ngine.run_engine()