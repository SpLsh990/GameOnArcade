import arcade
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox

from newGameView import NewGameView
from savesView import SavesView
from settingsView import SettingsView
from background import BackgroundView

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'MainMenuTest'


# TODO
#  Изменить положение кнопок(сделать его относительным),
#  Добавить надписи на кнопки
class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = BackgroundView(self.width, self.height)
        self.backgrList = arcade.SpriteList()
        self.backgrList.append(self.background)

        self.manager = UIManager()
        self.manager.enable()

        self.create_widget()

    def create_widget(self):
        button_normal = arcade.load_texture("sprites/button/button_normal.png")
        button_active = arcade.load_texture("sprites/button/button_active.png")
        button_triggered = arcade.load_texture("sprites/button/button_triggered.png")

        gear_normal = arcade.load_texture("sprites/gear/gear_normal.png")
        gear_active = arcade.load_texture("sprites/gear/gear_active.png")
        gear_triggered = arcade.load_texture("sprites/gear/gear_triggered.png")

        center_space = UISpace(width=300, height=250, color=(0, 0, 0, 0))
        vert_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        hor_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        button_new_game = UITextureButton(texture=button_normal,
                                          texture_hovered=button_active,
                                          texture_pressed=button_triggered,
                                          scale=0.3)

        button_saves = UITextureButton(texture=button_normal,
                                       texture_hovered=button_active,
                                       texture_pressed=button_triggered,
                                       scale=0.3)

        button_exit = UITextureButton(texture=button_normal,
                                      texture_hovered=button_active,
                                      texture_pressed=button_triggered,
                                      scale=0.3)

        button_settings = UITextureButton(texture=gear_normal,
                                          texture_hovered=gear_active,
                                          texture_pressed=gear_triggered,
                                          scale=0.2)

        button_settings.center_x, button_settings.center_y = 60, 60

        self.center_anchor = UIAnchorLayout()

        self.left_anchor = UIAnchorLayout()
        self.left_anchor.default_anchor_x = 'left'
        self.left_anchor.default_anchor_y = 'bottom'

        self.center_layout = UIBoxLayout(vertical=True, space_between=10)

        self.left_vert_layout = UIBoxLayout(vertical=True, space_between=10)

        self.left_hor_layout = UIBoxLayout(vertical=False, space_between=10)


        self.left_vert_layout.add(button_settings)
        self.left_vert_layout.add(vert_space)

        self.left_hor_layout.add(hor_space)
        self.left_hor_layout.add(self.left_vert_layout)

        self.left_anchor.add(self.left_hor_layout)

        self.center_layout.add(center_space)
        self.center_layout.add(button_new_game)
        self.center_layout.add(button_saves)
        self.center_layout.add(button_exit)

        self.center_anchor.add(self.center_layout)

        self.manager.add(self.center_anchor)
        self.manager.add(self.left_anchor)

        button_new_game.on_click = self.new_game_triggered
        button_saves.on_click = self.saves_triggered
        button_exit.on_click = self.exit_triggered
        button_settings.on_click = self.settings_triggered

    def on_draw(self):
        self.clear()
        self.backgrList.draw()
        self.manager.draw()

    def on_update(self, delta_time: float):
        self.backgrList.update()
        self.background.update_animation()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.background.resize(width, height)

    def new_game_triggered(self, arg):
        new_game_view = NewGameView()
        self.window.show_view(new_game_view)
        self.manager.disable()

    def saves_triggered(self, arg):
        saves_view = SavesView()
        self.window.show_view(saves_view)
        self.manager.disable()

    def exit_triggered(self, arg):
        arcade.close_window()

    def settings_triggered(self, arg):
        settings_view = SettingsView(self)
        self.window.show_view(settings_view)
        self.manager.disable()

if __name__ == '__main__':
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()
