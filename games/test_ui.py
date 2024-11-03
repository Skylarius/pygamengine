import context
from pygamengine import *
from pygamengine.ui import Button, Text

if __name__ == "__main__":
    button = Button("b", (110, 60), size=(200,100))
    
    text = Text("Mytext", (1000, 300))
    text.text = "I'm a test text.."
    button.count = 0

    def on_button_click():
        button.count += 1
        button.text.set_update(f"You clicked {button.count} times!")

    button.on_click = on_button_click
    
    r = Rectangle("ciao", 20, 100, (230, 50, 0, 255))
    r.set_position((400,400))
    Ngine.create_new_gameobject(button)
    Ngine.create_new_gameobject(r)
    Ngine.create_new_gameobject(text)
    Ngine.run_engine()