import arcade
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox, UISlider
from baseView import BaseView
from CustomButton import CustomButton


class SettingsView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.bool_sound = True
        self.bool_music = True

        self.sound = 56
        self.music = 89
        self.menu_music = arcade.load_sound("music/menu.ogg")
        self.game_music = arcade.load_sound("music/game.ogg")
        self.player = None
        self.create_widget()

    def create_widget(self):
        self.l_anchor = UIAnchorLayout()
        self.l_anchor.default_anchor_x = 'left'
        self.l_anchor.default_anchor_y = 'bottom'

        self.lv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.lh_layout = UIBoxLayout(vertical=False, space_between=10)

        v_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        h_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        self.button_back = CustomButton(self.width * 0.15, self.height * 0.075, "BACK", self.width * 0.00019,
                                        self.width * 0.00019,
                                        self.window.textures['button_n'],
                                        self.window.textures['button_a'],
                                        self.window.textures['button_t'])

        self.lv_layout.add(self.button_back)
        self.lv_layout.add(v_space)

        self.lh_layout.add(h_space)
        self.lh_layout.add(self.lv_layout)

        self.l_anchor.add(self.lh_layout)

        self.manager.add(self.l_anchor)

        self.c_anchor = UIAnchorLayout()

        self.cv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.cmusic_layout = UIBoxLayout(vertical=False, space_between=10)
        self.csound_layout = UIBoxLayout(vertical=False, space_between=10)

        self.button_music = CustomButton(self.width * 0.2, self.height * 0.1, "MUSIC", self.width * 0.00023,
                                         self.width * 0.00023,
                                         self.window.textures['button_n'],
                                         self.window.textures['button_a'],
                                         self.window.textures['button_t'])

        self.button_sound = CustomButton(self.width * 0.2, self.height * 0.1, "SOUND", self.width * 0.00023,
                                         self.width * 0.00023,
                                         self.window.textures['button_n'],
                                         self.window.textures['button_a'],
                                         self.window.textures['button_t'])
        c_space = UISpace(width=100, height=200, color=(0, 0, 0, 0))

        self.music_slider = UISlider(width=300, height=50, min_value=0, max_value=100, value=self.music)
        self.sound_slider = UISlider(width=300, height=50, min_value=0, max_value=100, value=self.sound)

        self.digits_music = CustomButton(self.width * 0.066, self.height * 0.039, f"{int(self.music_slider.value):03}",
                                         self.width * 0.0002, self.width * 0.0002,
                                         self.window.textures['button_e'], change_text=False)

        self.digits_sound = CustomButton(self.width * 0.066, self.height * 0.039, f"{int(self.sound_slider.value):03}",
                                         self.width * 0.0002, self.width * 0.0002,
                                         self.window.textures['button_e'], change_text=False)

        self.cmusic_layout.add(self.button_music)
        self.cmusic_layout.add(self.music_slider)
        self.cmusic_layout.add(self.digits_music)

        self.csound_layout.add(self.button_sound)
        self.csound_layout.add(self.sound_slider)
        self.csound_layout.add(self.digits_sound)

        self.cv_layout.add(c_space)
        self.cv_layout.add(self.cmusic_layout)
        self.cv_layout.add(self.csound_layout)
        self.cv_layout.add(c_space)

        self.c_anchor.add(self.cv_layout)

        self.manager.add(self.c_anchor)

        self.button_back.on_click = lambda event: self.back_triggered(event)
        self.button_music.on_click = lambda event: self.music_triggered(event)
        self.button_sound.on_click = lambda event: self.sound_triggered(event)

        self.music_slider.on_change = lambda value: self.change_music(value)
        self.sound_slider.on_change = lambda value: self.change_sound(value)

    def back_triggered(self, event):
        if self.window.is_game:
            self.window.show_view(self.window.pause_view)
        else:
            self.window.show_view(self.window.menu_view)

    def music_triggered(self, event):
        self.bool_music = not self.bool_music
        self.button_music.change(self.bool_music)
        text = f"{int(self.music_slider.value):03}" if self.bool_music else "OFF"
        self.digits_music.load_text(text)

    def sound_triggered(self, event):
        self.bool_sound = not self.bool_sound
        self.button_sound.change(self.bool_sound)
        text = f"{int(self.sound_slider.value):03}" if self.bool_sound else "OFF"
        self.digits_sound.load_text(text)

    def change_music(self, value):
        self.music = int(value.new_value)
        self.bool_music = bool(self.music)
        self.button_music.change(self.bool_music)
        text = f"{int(self.music_slider.value):03}" if self.bool_music else "OFF"
        self.digits_music.load_text(text)

    def change_sound(self, value):
        self.sound = int(value.new_value)
        self.bool_sound = bool(self.sound)
        self.button_sound.change(self.bool_sound)
        text = f"{int(self.sound_slider.value):03}" if self.bool_sound else "OFF"
        self.digits_sound.load_text(text)

    def change(self):
        if self.bool_music:
            self.player = self.menu_music.play(volume=0.5 * self.music, loop=True)
        else:
            if self.player:
                self.player.stop()
