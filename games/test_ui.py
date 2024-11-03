import context
from pygamengine import *
from pygamengine.ui import Button, Text
import os

if __name__ == "__main__":
    # Create simple button
    button = Button("b", (110, 60), size=(200,100))
    button.count = 0

    def on_button_click():
        button.count += 1
        button.text.set_update(f"You clicked {button.count} times!")
    
    button.on_click = on_button_click
    Ngine.create_new_gameobject(button)
    
    # Create Simple text
    text = Text("Mytext", (300, 60))
    text.text = "I'm a test text.."
    Ngine.create_new_gameobject(text)

    # Create button with sprite images
    button_sprite_folder = "src/sprites/ui/buttons"
    button2 = Button(
        "sprite_b", (500, 60), 
        unselected_image=os.path.join(button_sprite_folder, "Button_7_unselected.png"),
        selected_image=os.path.join(button_sprite_folder, "Button_7_unselected.png"),
        pressed_image=os.path.join(button_sprite_folder, "Button_7_pressed.png"),
        has_text=False
    )
    Ngine.create_new_gameobject(button2)
    
    r = Rectangle("ciao", 20, 100, (230, 50, 0, 255))
    r.set_position((400,400))
    Ngine.create_new_gameobject(r)
    Ngine.run_engine()