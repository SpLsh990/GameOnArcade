import arcade
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIInteractiveWidget
from baseView import BaseView
from CustomButton import CustomButton


class MainMenuView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.create_widget()

    def create_widget(self):
        c_space = UISpace(width=800, height=100, color=(0, 0, 0, 0))

        """self.button_new_game = UITextureButton(texture=self.window.sprites['new_game_n'],
                                               texture_hovered=self.window.sprites['new_game_a'],
                                               texture_pressed=self.window.sprites['new_game_t'],
                                               scale=0.4)
        """

        self.button_new_game = CustomButton(768 * 0.4, 248 * 0.4, "NEW GAME", 0.362, 0.362,
                                            self.window.sprites['button_n'],
                                            self.window.sprites['button_a'],
                                            self.window.sprites['button_t'])

        self.button_saves = CustomButton(768 * 0.4, 248 * 0.4, "SAVES", 0.4, 0.4, self.window.sprites['button_n'],
                                         self.window.sprites['button_a'],
                                         self.window.sprites['button_t'])

        self.button_settings = CustomButton(768 * 0.4, 248 * 0.4, "SETTINGS", 0.362, 0.362,
                                            self.window.sprites['button_n'],
                                            self.window.sprites['button_a'],
                                            self.window.sprites['button_t'])

        self.button_exit = CustomButton(768 * 0.4, 248 * 0.4, "EXIT", 0.4, 0.4, self.window.sprites['button_n'],
                                        self.window.sprites['button_a'],
                                        self.window.sprites['button_t'])

        self.c_anchor = UIAnchorLayout()
        self.cv_layout = UIBoxLayout(vertical=True, space_between=10)

        self.cv_layout.add(c_space)
        self.cv_layout.add(self.button_new_game)
        self.cv_layout.add(self.button_saves)
        self.cv_layout.add(self.button_settings)
        self.cv_layout.add(self.button_exit)

        self.c_anchor.add(self.cv_layout)

        self.manager.add(self.c_anchor)

        self.button_new_game.on_click = lambda event: self.new_game_triggered(event)
        self.button_saves.on_click = lambda event: self.saves_triggered(event)
        self.button_exit.on_click = lambda event: self.exit_triggered(event)
        self.button_settings.on_click = lambda event: self.settings_triggered(event)

    def new_game_triggered(self, event):
        self.window.show_view(self.window.new_game_view)

    def saves_triggered(self, event):
        self.window.saves_view.load_saves()
        self.window.show_view(self.window.saves_view)

    def exit_triggered(self, event):
        arcade.close_window()

    def settings_triggered(self, event):
        self.window.show_view(self.window.settings_view)
