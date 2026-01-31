import arcade
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIInteractiveWidget
from baseView import BaseView
import json
import pickle
from random import randint
from datetime import date
from CustomButton import CustomButton


class PauseView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.create_widget()

    def create_widget(self):
        c_space = UISpace(width=800, height=100, color=(0, 0, 0, 0))
        self.button_continue = CustomButton(768 * 0.4, 248 * 0.4, "CONTINUE", 0.362, 0.362,
                                            self.window.sprites['button_n'],
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
        self.cv_layout.add(self.button_continue)
        self.cv_layout.add(self.button_settings)
        self.cv_layout.add(self.button_exit)

        self.c_anchor.add(self.cv_layout)

        self.manager.add(self.c_anchor)

        self.button_continue.on_click = lambda event: self.continue_triggered(event)
        self.button_exit.on_click = lambda event: self.exit_triggered(event)
        self.button_settings.on_click = lambda event: self.settings_triggered(event)

    def continue_triggered(self, event):
        self.window.game_view.pause = False
        self.window.show_view(self.window.game_view)

    def exit_triggered(self, event):
        self.data = self.window.game_view.data
        self.data['date'] = str(date.today())
        with open(f"saves/{self.data.get("name")}.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)
        with open(f"saves/{self.data.get("name")}.sv", "wb") as file:
            pickle.dump(self.data, file)
        self.window.is_game = False
        self.window.show_view(self.window.menu_view)

    def settings_triggered(self, event):
        self.window.show_view(self.window.settings_view)
