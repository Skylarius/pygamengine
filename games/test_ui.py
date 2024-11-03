import context
from pygamengine import *
from pygamengine.ui import Button

if __name__ == "__main__":
    button = Button("mybutton", (100, 100), size=(200,200))
    r = Rectangle("ciao")
    r.set_position((400,400))
    Ngine.create_new_gameobject(button)
    Ngine.create_new_gameobject(r)
    Ngine.run_engine()