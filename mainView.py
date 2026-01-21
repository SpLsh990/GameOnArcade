import arcade
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox
from baseView import BaseView


class MainMenuView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.create_widget()

    def create_widget(self):
        button_new_game_normal = arcade.load_texture("sprites/button_new_game/new_game_normal.png")
        button_new_game_active = arcade.load_texture("sprites/button_new_game/new_game_active.png")
        button_new_game_triggered = arcade.load_texture("sprites/button_new_game/new_game_triggered.png")

        button_saves_normal = arcade.load_texture('sprites/button_saves/saves_normal.png')
        button_saves_active = arcade.load_texture('sprites/button_saves/saves_active.png')
        button_saves_triggered = arcade.load_texture('sprites/button_saves/saves_triggered.png')

        button_exit_normal = arcade.load_texture("sprites/button_exit/exit_normal.png")
        button_exit_active = arcade.load_texture("sprites/button_exit/exit_active.png")
        button_exit_triggered = arcade.load_texture("sprites/button_exit/exit_triggered.png")

        gear_normal = arcade.load_texture("sprites/gear/gear_normal.png")
        gear_active = arcade.load_texture("sprites/gear/gear_active.png")
        gear_triggered = arcade.load_texture("sprites/gear/gear_triggered.png")

        center_space = UISpace(width=300, height=250, color=(0, 0, 0, 0))
        vert_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        hor_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        button_new_game = UITextureButton(texture=button_new_game_normal,
                                          texture_hovered=button_new_game_active,
                                          texture_pressed=button_new_game_triggered,
                                          scale=0.4)

        button_saves = UITextureButton(texture=button_saves_normal,
                                       texture_hovered=button_saves_active,
                                       texture_pressed=button_saves_triggered,
                                       scale=0.4)

        button_exit = UITextureButton(texture=button_exit_normal,
                                      texture_hovered=button_exit_active,
                                      texture_pressed=button_exit_triggered,
                                      scale=0.4)

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

    def new_game_triggered(self, arg):
        self.window.show_view(self.window.new_game_view)

    def saves_triggered(self, arg):
        self.window.show_view(self.window.saves_view)

    def exit_triggered(self, arg):
        arcade.close_window()

    def settings_triggered(self, arg):
        self.window.show_view(self.window.settings_view)