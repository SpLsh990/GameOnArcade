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

        self.button_new_game = CustomButton(self.width * 0.2, self.height * 0.1, "NEW GAME",
                                            size_letter=self.width * 0.00023, size_space=self.width * 0.00023,
                                            texture_normal=self.window.textures['button_n'],
                                            texture_active=self.window.textures['button_a'],
                                            texture_triggered=self.window.textures['button_t'])

        self.button_saves = CustomButton(self.width * 0.2, self.height * 0.1, "SAVES", self.width * 0.00023,
                                         self.width * 0.00023,
                                         self.window.textures['button_n'],
                                         self.window.textures['button_a'],
                                         self.window.textures['button_t'])

        self.button_settings = CustomButton(self.width * 0.2, self.height * 0.1, "SETTINGS", self.width * 0.00023,
                                            self.width * 0.00023,
                                            self.window.textures['button_n'],
                                            self.window.textures['button_a'],
                                            self.window.textures['button_t'])

        self.button_exit = CustomButton(self.width * 0.2, self.height * 0.1, "EXIT", self.width * 0.00023,
                                        self.width * 0.00023,
                                        self.window.textures['button_n'],
                                        self.window.textures['button_a'],
                                        self.window.textures['button_t'])

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
