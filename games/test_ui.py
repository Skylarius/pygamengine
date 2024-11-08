import context
from pygamengine import *
from pygamengine.ui import Button, Text, Anchor
import os

if __name__ == "__main__":

    r = Rectangle("ciao", Ngine.display[0] - 20, Ngine.display[1]/2, (230, 50, 0, 255))
    r.set_position((Ngine.display[0]/2,Ngine.display[1]/4))
    Ngine.create_new_gameobject(r)

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
    
    Ngine.run_engine()