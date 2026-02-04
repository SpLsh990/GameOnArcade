import arcade
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIInteractiveWidget
from baseView import BaseView
import json
import pickle
import time
from random import randint
from CustomButton import CustomButton


class PauseView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.create_widget()

    def create_widget(self):
        c_space = UISpace(width=800, height=100, color=(0, 0, 0, 0))
        self.button_continue = CustomButton(self.width * 0.2, self.height * 0.1, "CONTINUE", self.width * 0.00023,
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
        self.cv_layout.add(self.button_continue)
        self.cv_layout.add(self.button_settings)
        self.cv_layout.add(self.button_exit)

        self.c_anchor.add(self.cv_layout)

        self.manager.add(self.c_anchor)

        self.button_continue.on_click = lambda event: self.continue_triggered(event)
        self.button_exit.on_click = lambda event: self.exit_triggered(event)
        self.button_settings.on_click = lambda event: self.settings_triggered(event)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.continue_triggered(True)

    def continue_triggered(self, event):
        self.window.game_view.pause = False
        self.window.show_view(self.window.game_view)

    def exit_triggered(self, event):
        self.window.game_view.save()
        self.window.is_game = False
        self.window.show_view(self.window.menu_view)

    def settings_triggered(self, event):
        self.window.show_view(self.window.settings_view)