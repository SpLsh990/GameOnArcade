import arcade
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIInteractiveWidget
from baseView import BaseView
import json
from random import randint
from datetime import date


class PauseView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.create_widget()

    def create_widget(self):
        c_space = UISpace(width=800, height=100, color=(0, 0, 0, 0))
        try:
            self.button_continue = UITextureButton(texture=self.window.sprites['continue_n'],
                                                   texture_hovered=self.window.sprites['continue_a'],
                                                   texture_pressed=self.window.sprites['continue_t'],
                                                   scale=0.362)

            self.button_exit = UITextureButton(texture=self.window.sprites['exit_n'],
                                               texture_hovered=self.window.sprites['exit_a'],
                                               texture_pressed=self.window.sprites['exit_t'],
                                               scale=0.4)

            self.button_settings = UITextureButton(texture=self.window.sprites['settings_n'],
                                                   texture_hovered=self.window.sprites['settings_a'],
                                                   texture_pressed=self.window.sprites['settings_t'],
                                                   scale=0.362)
        except Exception as e:
            print(e)
            print(self.window.sprites)
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
        with open(f"saves/{self.data.get("name", randint(1, 10000000))}.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)
        self.window.is_game = False
        self.window.show_view(self.window.menu_view)

    def settings_triggered(self, event):
        self.window.show_view(self.window.settings_view)
