import arcade
from pyglet.graphics import Batch
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'MainMenuTest'


class BackgroundMenu(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.textures = []
        self.scale = 1.3
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        for i in range(60):
            texture = arcade.load_texture(f'sprites/menu/{i}.png')
            self.textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.03

    def update_animation(self, delta_time: float = 1 / 60):
        self.texture_change_time += delta_time
        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time = 0
            self.current_texture += 1
            if self.current_texture >= len(self.textures):
                self.current_texture = 0
            self.texture = self.textures[self.current_texture]


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = (0, 0, 0)

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

        self.background_list = arcade.SpriteList()
        self.background = BackgroundMenu()
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
                                          scale=0.3)
        button_exit = UITextureButton(texture=texture_normal,
                                      texture_hovered=texture_active,
                                      texture_pressed=texture_triggered,
                                      scale=0.3)
        self.box_layout.add(button_play)
        self.box_layout.add(button_exit)
        self.box_layout.add(button_settings)

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        self.background_list.update()
        self.background.update_animation()

    def on_mouse_press(self, x, y, button, modifiers):
        pass


if __name__ == '__main__':
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()
