import arcade
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout
from background import BackgroundView

class PauseView(arcade.View):
    def __init__(self, view):
        super().__init__()
        self.game_view = view
        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()
        self.background_list = arcade.SpriteList()
        self.background = BackgroundView(self.width, self.height)
        self.background_list.append(self.background)

    def setup_widgets(self):
        texture_normal = arcade.load_texture("sprites/button/button_normal.png")
        texture_active = arcade.load_texture("sprites/button/button_active.png")
        texture_triggered = arcade.load_texture("sprites/button/button_triggered.png")

        gear_normal = arcade.load_texture("sprites/gear/gear_normal.png")
        gear_active = arcade.load_texture("sprites/gear/gear_active.png")
        gear_triggered = arcade.load_texture("sprites/gear/gear_triggered.png")

        button_play = UITextureButton(texture=texture_normal,
                                      texture_hovered=texture_active,
                                      texture_pressed=texture_triggered,
                                      scale=0.3)
        button_settings = UITextureButton(texture=gear_normal,
                                          texture_hovered=gear_active,
                                          texture_pressed=gear_triggered,
                                          scale=0.15, x=30, y=30)
        button_exit = UITextureButton(texture=texture_normal,
                                      texture_hovered=texture_active,
                                      texture_pressed=texture_triggered,
                                      scale=0.3)

        self.box_layout.add(button_play)
        self.box_layout.add(button_exit)
        self.manager.add(button_settings)


    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        self.background_list.update()
        self.background.update_animation()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.background.update_position(width, height)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
            self.game_view.manager.enable()