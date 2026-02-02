import arcade
from arcade.gui import UIAnchorLayout, UIBoxLayout, UISpace, UITextureButton, UIMessageBox
from baseView import BaseView
from CustomButton import CustomButton


class SettingsView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.create_widget()

    def create_widget(self):
        c_space = UISpace(width=800, height=100, color=(0, 0, 0, 0))

        self.button_back = CustomButton(
            self.width * 0.2, self.height * 0.1, "BACK",
            size_letter=self.width * 0.00023, size_space=self.width * 0.00023,
            texture_normal=self.window.textures['button_n'],
            texture_active=self.window.textures['button_a'],
            texture_triggered=self.window.textures['button_t']
        )

        self.button_resolution = CustomButton(
            self.width * 0.2, self.height * 0.1, "RESOLUTION",
            size_letter=self.width * 0.00023, size_space=self.width * 0.00023,
            texture_normal=self.window.textures['button_n'],
            texture_active=self.window.textures['button_a'],
            texture_triggered=self.window.textures['button_t']
        )

        self.button_fullscreen = CustomButton(
            self.width * 0.2, self.height * 0.1, "FULLSCREEN",
            size_letter=self.width * 0.00023, size_space=self.width * 0.00023,
            texture_normal=self.window.textures['button_n'],
            texture_active=self.window.textures['button_a'],
            texture_triggered=self.window.textures['button_t']
        )

        self.button_music = CustomButton(
            self.width * 0.2, self.height * 0.1, "MUSIC",
            size_letter=self.width * 0.00023, size_space=self.width * 0.00023,
            texture_normal=self.window.textures['button_n'],
            texture_active=self.window.textures['button_a'],
            texture_triggered=self.window.textures['button_t']
        )

        self.c_anchor = UIAnchorLayout()
        self.cv_layout = UIBoxLayout(vertical=True, space_between=10)

        self.cv_layout.add(c_space)
        self.cv_layout.add(self.button_back)
        self.cv_layout.add(self.button_resolution)
        self.cv_layout.add(self.button_fullscreen)
        self.cv_layout.add(self.button_music)

        self.c_anchor.add(self.cv_layout)
        self.manager.add(self.c_anchor)

        self.button_back.on_click = lambda event: self.back_triggered(event)
        self.button_resolution.on_click = lambda event: self.resolution_triggered(event)
        self.button_fullscreen.on_click = lambda event: self.fullscreen_triggered(event)
        self.button_music.on_click = lambda event: self.music_triggered(event)

    def back_triggered(self, event):
        if self.window.is_game:
            self.window.show_view(self.window.pause_view)
        else:
            self.window.show_view(self.window.menu_view)

    def resolution_triggered(self, event):
        message = UIMessageBox(
            width=300, height=200,
            message_text="Функция изменения разрешения \nпока не реализована",
            buttons=["OK"]
        )
        self.manager.add(message)

    def fullscreen_triggered(self, event):
        message = UIMessageBox(
            width=300, height=200,
            message_text="Функция переключения \nполноэкранного режима пока не реализована",
            buttons=["OK"]
        )
        self.manager.add(message)

    def music_triggered(self, event):
        message = UIMessageBox(
            width=300, height=200,
            message_text="Функция управления музыкой \nпока не реализована",
            buttons=["OK"]
        )
        self.manager.add(message)