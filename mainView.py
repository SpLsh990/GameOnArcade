import arcade
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIInteractiveWidget
from baseView import BaseView


class MainMenuView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.load_textures()
        self.create_widget()

    def load_textures(self):
        self.texture_new_game_normal = arcade.load_texture("sprites/button_new_game/new_game_normal.png")
        self.texture_new_game_active = arcade.load_texture("sprites/button_new_game/new_game_active.png")
        self.texture_new_game_triggered = arcade.load_texture("sprites/button_new_game/new_game_triggered.png")

        self.texture_saves_normal = arcade.load_texture('sprites/button_saves/saves_normal.png')
        self.texture_saves_active = arcade.load_texture('sprites/button_saves/saves_active.png')
        self.texture_saves_triggered = arcade.load_texture('sprites/button_saves/saves_triggered.png')

        self.texture_exit_normal = arcade.load_texture("sprites/button_exit/exit_normal.png")
        self.texture_exit_active = arcade.load_texture("sprites/button_exit/exit_active.png")
        self.texture_exit_triggered = arcade.load_texture("sprites/button_exit/exit_triggered.png")

        self.texture_gear_normal = arcade.load_texture("sprites/gear/gear_normal.png")
        self.texture_gear_active = arcade.load_texture("sprites/gear/gear_active.png")
        self.texture_gear_triggered = arcade.load_texture("sprites/gear/gear_triggered.png")


    def create_widget(self):
        c_space = UISpace(width=300, height=250, color=(0, 0, 0, 0))
        v_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        h_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        button_new_game = UITextureButton(texture=self.texture_new_game_normal,
                                          texture_hovered=self.texture_new_game_active,
                                          texture_pressed=self.texture_new_game_triggered,
                                          scale=0.4)

        button_saves = UITextureButton(texture=self.texture_saves_normal,
                                       texture_hovered=self.texture_saves_active,
                                       texture_pressed=self.texture_saves_triggered,
                                       scale=0.4)

        button_exit = UITextureButton(texture=self.texture_exit_normal,
                                      texture_hovered=self.texture_exit_active,
                                      texture_pressed=self.texture_exit_triggered,
                                      scale=0.4)

        button_settings = UITextureButton(texture=self.texture_gear_normal,
                                          texture_hovered=self.texture_gear_active,
                                          texture_pressed=self.texture_gear_triggered,
                                          scale=0.2)
        button_settings.center_x, button_settings.center_y = 60, 60

        self.c_anchor = UIAnchorLayout()

        self.l_anchor = UIAnchorLayout()
        self.l_anchor.default_anchor_x = 'left'
        self.l_anchor.default_anchor_y = 'bottom'

        self.c_layout = UIBoxLayout(vertical=True, space_between=10)

        self.lv_layout = UIBoxLayout(vertical=True, space_between=10)

        self.lh_layout = UIBoxLayout(vertical=False, space_between=10)

        self.lv_layout.add(button_settings)
        self.lv_layout.add(v_space)

        self.lh_layout.add(h_space)
        self.lh_layout.add(self.lv_layout)

        self.l_anchor.add(self.lh_layout)

        self.c_layout.add(c_space)
        self.c_layout.add(button_new_game)
        self.c_layout.add(button_saves)
        self.c_layout.add(button_exit)

        self.c_anchor.add(self.c_layout)

        self.manager.add(self.c_anchor)
        self.manager.add(self.l_anchor)

        button_new_game.on_click = lambda event: self.new_game_triggered(event)
        button_saves.on_click = lambda event: self.saves_triggered(event)
        button_exit.on_click = lambda event: self.exit_triggered(event)
        button_settings.on_click = lambda event: self.settings_triggered(event)

    def new_game_triggered(self, event):
        self.window.show_view(self.window.new_game_view)

    def saves_triggered(self, event):
        self.window.show_view(self.window.saves_view)

    def exit_triggered(self, event):
        arcade.close_window()

    def settings_triggered(self, event):
        self.window.show_view(self.window.settings_view)