import arcade
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIInteractiveWidget
from baseView import BaseView


class MainMenuView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.create_widget()

    def create_widget(self):
        c_space = UISpace(width=800, height=100, color=(0, 0, 0, 0))
        v_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        h_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        button_new_game = UITextureButton(texture=self.window.sprites['new_game_n'],
                                          texture_hovered=self.window.sprites['new_game_a'],
                                          texture_pressed=self.window.sprites['new_game_t'],
                                          scale=0.4)

        button_saves = UITextureButton(texture=self.window.sprites['saves_n'],
                                       texture_hovered=self.window.sprites['saves_a'],
                                       texture_pressed=self.window.sprites['saves_t'],
                                       scale=0.4)

        button_exit = UITextureButton(texture=self.window.sprites['exit_n'],
                                      texture_hovered=self.window.sprites['exit_a'],
                                      texture_pressed=self.window.sprites['exit_t'],
                                      scale=0.4)

        button_settings = UITextureButton(texture=self.window.sprites['settings_n'],
                                          texture_hovered=self.window.sprites['settings_a'],
                                          texture_pressed=self.window.sprites['settings_t'],
                                          scale=0.362)
        button_settings.center_x, button_settings.center_y = 60, 60

        self.c_anchor = UIAnchorLayout()

        self.l_anchor = UIAnchorLayout()
        self.l_anchor.default_anchor_x = 'left'
        self.l_anchor.default_anchor_y = 'bottom'

        self.c_layout = UIBoxLayout(vertical=True, space_between=10)

        self.lv_layout = UIBoxLayout(vertical=True, space_between=10)

        self.lh_layout = UIBoxLayout(vertical=False, space_between=10)

        #self.lv_layout.add(button_settings)
        self.lv_layout.add(v_space)

        self.lh_layout.add(h_space)
        self.lh_layout.add(self.lv_layout)

        self.l_anchor.add(self.lh_layout)

        self.c_layout.add(c_space)
        self.c_layout.add(button_new_game)
        self.c_layout.add(button_saves)
        self.c_layout.add(button_settings)
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