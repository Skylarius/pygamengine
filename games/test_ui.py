import context
from pygamengine import *
from pygamengine.ui import *
import os
import random

from pygamengine.ui.ui_element import Anchor

class MovingButton(Button):
    def __init__(self, name: str, position: tuple[float, float] = ..., size: tuple[float, float] = ..., anchor=Anchor.CENTER) -> None:
        super().__init__(name, position, size, anchor=anchor)
        self.speed = 0.5
        self.direction = 1
    
    def start(self):
        super().start()
        self.text.set_update("MovingButton")
        
    def tick(self):
        super().tick()
        pos = self.get_position()
        if pos[0] > Ngine.get_display()[0] - self.width:
            self.direction = -1
        if pos[0] < 0:
            self.direction = 1
        self.set_position_with_children(Transform.get_vectors_sum(self.get_position(),(self.direction * self.speed,0)))

if __name__ == "__main__":
    Ngine.set_caption("TEST UI")
    #Ngine.set_display(1920,1080)
    
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
        (100, 200), (255,255,0), anchor=Anchor.TOP_LEFT, border=10, border_color=(255,0,0)
    )
    
    Ngine.create_new_gameobject(panel)
    # Create panel description text (to test positioning)
    text2 = Text("panel_description", Transform.get_vectors_sum(panel.get_position(), 
        (0, panel.height + 30)), text="/\ This one above is a panel", anchor=Anchor.TOP_LEFT, max_width=panel.width
    )
    Ngine.create_new_gameobject(text2)

    # Create Panel
    textpanel = TextPanel(
        "mytextpanel", 
        "This text is inside this magical textpanel\nAnd this text is on another line", 
        (panel.get_position()[0] + panel.width + 30, 30), 
        (100, 200), (0,255,0), anchor=Anchor.TOP_LEFT
    )
    textpanel.text.color = (0,0,255)
    textpanel.text.max_lines = 10
    textpanel.text.remove_lines_on_top = True
    Ngine.create_new_gameobject(textpanel)

    # create moving button (defined above)
    moving_button = MovingButton(
        "my_moving_button", 
        position=(button.get_position()[0], button.get_position()[1] + button.height + 30),
        size=(200,100), anchor=Anchor.TOP_LEFT
    )
    Ngine.create_new_gameobject(moving_button)

    def on_click_moving_button():
        x, y = random.randint(200, 1000), random.randrange(20, 600)
        textpanel.set_position_with_children((x,y))
        textpanel.text.set_update(f"{textpanel.text.text}\nNew position ({x},{y})")
        textpanel.update_text_position()

    moving_button.on_click = on_click_moving_button
    
    # Place panel with 4 text on corners
    pos = (textpanel.get_position()[0] + textpanel.width + 30, 30)
    bigpanel = Panel("mybigpanel", pos, 
        (Ngine.get_display()[0] - 30 - pos[0], Ngine.get_display()[1] - 30 - pos[1]), (255,0,255), anchor=Anchor.TOP_LEFT, border=30, border_color=(0,0,255)
    )
    Ngine.create_new_gameobject(bigpanel)
    Ngine.create_new_gameobject(Text("txt_tl", bigpanel.get_position_with_anchor(Anchor.TOP_LEFT), text="TL"))
    Ngine.create_new_gameobject(Text("txt_tr", bigpanel.get_position_with_anchor(Anchor.TOP_RIGHT), text="TR"))
    Ngine.create_new_gameobject(Text("txt_bl", bigpanel.get_position_with_anchor(Anchor.BOTTOM_LEFT), text="BL"))
    Ngine.create_new_gameobject(Text("txt_br", bigpanel.get_position_with_anchor(Anchor.BOTTOM_RIGHT), text="BR"))
    Ngine.create_new_gameobject(Text("txt_top_left", bigpanel.transform.get_position(), text="*TopLeft", anchor=Anchor.TOP_LEFT, font_size=16))
    Ngine.create_new_gameobject(Text("txt_top_right", bigpanel.transform.get_position(), text="TopRight*", anchor=Anchor.TOP_RIGHT, font_size=16))
    Ngine.create_new_gameobject(Text("txt_bottom_left", bigpanel.transform.get_position(), text="_BottomLeft", anchor=Anchor.BOTTOM_LEFT,font_size=16))
    Ngine.create_new_gameobject(Text("txt_bottom_right", bigpanel.transform.get_position(), text="BottomRight_", anchor=Anchor.BOTTOM_RIGHT, font_size=16))

    # Create Slider
    slider_horizontal = Slider("slider_h", Transform.get_vectors_sum(moving_button.get_position(),(0, moving_button.height + 30)),
        Anchor.TOP_LEFT, start_value=12.5, max_value=14, min_value=9, step=0.1
    )

    Ngine.create_new_gameobject(slider_horizontal)   

    def change_slider_horizontal_text(new_value: float):
        text_slider_horizontal.set_update(f"Slider: {new_value:.2f}")
        text_slider_horizontal.set_font_size(int(new_value)*2)
    
    slider_horizontal.on_slider_change = change_slider_horizontal_text

    text_slider_horizontal = Text(
        "slider_horizontal_text", 
        Transform.get_vectors_sum(slider_horizontal.get_position(), (slider_horizontal.width + 30,0)),
        anchor=Anchor.TOP_LEFT
    )
    Ngine.create_new_gameobject(text_slider_horizontal)

    slider_sprite_folder = "src/sprites/ui/sliders"
    slider_vertical = Slider("slider_y", 
        Transform.get_vectors_sum(slider_horizontal.get_position(),(0, 30)), Anchor.TOP_LEFT, 
        bar_image=os.path.join(slider_sprite_folder, "slider_bar.png"), 
        indicator_image=os.path.join(slider_sprite_folder, "slider_cursor.png"),
        slider_type=SliderType.Vertical,
        max_value=100, min_value=10, start_value=20, step=20
    )

    Ngine.create_new_gameobject(slider_vertical)

    def change_slider_vertical_text(new_value: float):
        text_slider_vertical.set_update(f"Slider: {new_value:.2f}")
    
    slider_vertical.on_slider_change = change_slider_vertical_text

    text_slider_vertical = Text(
        "slider_vertical_text", 
        Transform.get_vectors_sum(slider_vertical.get_position(), (0,slider_vertical.height + 30)),
        anchor=Anchor.TOP_LEFT
    )
    Ngine.create_new_gameobject(text_slider_vertical)

    Ngine.run_engine()