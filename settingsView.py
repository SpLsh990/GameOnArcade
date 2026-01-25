import arcade
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox, UISlider
from baseView import BaseView


class SettingsView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.bool_sound = True
        self.bool_music = True

        self.sound = 56
        self.music = 89

        self.create_widget()

    def create_widget(self):
        self.l_anchor = UIAnchorLayout()
        self.l_anchor.default_anchor_x = 'left'
        self.l_anchor.default_anchor_y = 'bottom'

        self.lv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.lh_layout = UIBoxLayout(vertical=False, space_between=10)

        v_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        h_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        self.button_back = UITextureButton(texture=self.window.sprites['back_n'],
                                           texture_hovered=self.window.sprites['back_a'],
                                           texture_pressed=self.window.sprites['back_t'], scale=0.13)

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

        self.button_music = UITextureButton(texture=self.window.sprites['music_n'],
                                            texture_hovered=self.window.sprites['music_a'],
                                            texture_pressed=self.window.sprites['music_t'], scale=0.3)

        self.button_sound = UITextureButton(texture=self.window.sprites['sound_n'],
                                            texture_hovered=self.window.sprites['sound_a'],
                                            texture_pressed=self.window.sprites['sound_t'], scale=0.3)

        """button_apply = UITextureButton(texture=self.window.sprites['apply_n'],
                                       texture_hovered=self.window.sprites['apply_a'],
                                       texture_pressed=self.window.sprites['apply_t'], scale=0.25)
        """
        cu_space = UISpace(width=100, height=200, color=(0, 0, 0, 0))
        cd_space = UISpace(width=100, height=200, color=(0, 0, 0, 0))

        self.music_slider = UISlider(width=300, height=50, min_value=0, max_value=100, value=self.music)
        self.sound_slider = UISlider(width=300, height=50, min_value=0, max_value=100, value=self.sound)

        self.first_dig_music = UITextureButton(texture=self.window.sprites[f"{self.music:03}"[0]], scale=0.3)
        self.second_dig_music = UITextureButton(texture=self.window.sprites[f"{self.music:03}"[1]], scale=0.3)
        self.third_dig_music = UITextureButton(texture=self.window.sprites[f"{self.music:03}"[2]], scale=0.3)

        self.first_dig_sound = UITextureButton(texture=self.window.sprites[f"{self.sound:03}"[0]], scale=0.3)
        self.second_dig_sound = UITextureButton(texture=self.window.sprites[f"{self.sound:03}"[1]], scale=0.3)
        self.third_dig_sound = UITextureButton(texture=self.window.sprites[f"{self.sound:03}"[2]], scale=0.3)

        self.cmusic_layout.add(self.button_music)
        self.cmusic_layout.add(self.music_slider)
        self.cmusic_layout.add(self.first_dig_music)
        self.cmusic_layout.add(self.second_dig_music)
        self.cmusic_layout.add(self.third_dig_music)

        self.csound_layout.add(self.button_sound)
        self.csound_layout.add(self.sound_slider)
        self.csound_layout.add(self.first_dig_sound)
        self.csound_layout.add(self.second_dig_sound)
        self.csound_layout.add(self.third_dig_sound)

        self.cv_layout.add(cu_space)
        self.cv_layout.add(self.cmusic_layout)
        self.cv_layout.add(self.csound_layout)
        self.cv_layout.add(cd_space)
        # self.cv_layout.add(button_apply)

        self.c_anchor.add(self.cv_layout)

        self.manager.add(self.c_anchor)

        self.button_back.on_click = lambda event: self.back_triggered(event)
        # button_apply.on_click = lambda event: self.apply_triggered(event)

        self.button_music.on_click = lambda event: self.music_triggered(event)
        self.button_sound.on_click = lambda event: self.sound_triggered(event)

        self.music_slider.on_change = lambda value: self.change_music(value)
        self.sound_slider.on_change = lambda value: self.change_sound(value)

        self.first_dig_music.on_click = lambda event: self.reduce_music(event)
        self.third_dig_music.on_click = lambda event: self.increase_music(event)

        self.first_dig_sound.on_click = lambda event: self.reduce_sound(event)
        self.third_dig_sound.on_click = lambda event: self.increase_sound(event)

    def back_triggered(self, event):
        self.window.show_view(self.window.menu_view)

    def apply_triggered(self):
        pass

    def music_triggered(self, event):
        self.bool_music = not self.bool_music
        self.change_texture_music()
        self.change_digits_music()

    def sound_triggered(self, event):
        self.bool_sound = not self.bool_sound
        self.change_texture_sound()
        self.change_digits_sound()

    def change_music(self, value):
        self.music = int(value.new_value)
        self.bool_music = True if self.music else False
        self.change_digits_music()
        self.change_texture_music()

    def change_sound(self, value):
        self.sound = int(value.new_value)
        self.bool_sound = True if self.sound else False
        self.change_digits_sound()
        self.change_texture_sound()

    def reduce_music(self, event):
        self.music -= 1 if self.music - 1 >= 0 else 0
        self.bool_music = True if self.music else False
        self.music_slider.value -= 1 if self.music_slider.value - 1 >= 0 else 0
        self.change_digits_music()
        self.change_texture_music()

    def increase_music(self, event):
        self.music += 1 if self.music + 1 <= 100 else 0
        self.bool_music = True if self.music else False
        self.music_slider.value += 1 if self.music_slider.value + 1 <= 100 else 0
        self.change_digits_music()
        self.change_texture_music()

    def reduce_sound(self, event):
        self.sound -= 1 if self.sound - 1 >= 0 else 0
        self.bool_sound = True if self.sound else False
        self.sound_slider.value -= 1 if self.sound_slider.value - 1 >= 0 else 0
        self.change_digits_sound()
        self.change_texture_sound()

    def increase_sound(self, event):
        self.sound += 1 if self.sound + 1 <= 100 else 0
        self.bool_sound = True if self.sound else False
        self.sound_slider.value += 1 if self.sound_slider.value + 1 <= 100 else 0
        self.change_digits_sound()
        self.change_texture_sound()

    def change_digits_music(self):
        if self.bool_music:
            music = list(f"{self.music:03}")
            self.set_texture(self.first_dig_music, self.window.sprites[music[0]])
            self.set_texture(self.second_dig_music, self.window.sprites[music[1]])
            self.set_texture(self.third_dig_music, self.window.sprites[music[2]])
        else:
            self.set_texture(self.first_dig_music, self.window.sprites['O'])
            self.set_texture(self.second_dig_music, self.window.sprites['F'])
            self.set_texture(self.third_dig_music, self.window.sprites['F'])

    def change_digits_sound(self):
        if self.bool_sound:
            sound = list(str(f"{self.sound:03}"))
            self.set_texture(self.first_dig_sound, self.window.sprites[sound[0]])
            self.set_texture(self.second_dig_sound, self.window.sprites[sound[1]])
            self.set_texture(self.third_dig_sound, self.window.sprites[sound[2]])
        else:
            self.set_texture(self.first_dig_sound, self.window.sprites['O'])
            self.set_texture(self.second_dig_sound, self.window.sprites['F'])
            self.set_texture(self.third_dig_sound, self.window.sprites['F'])

    def change_texture_music(self):
        if self.bool_music:
            self.button_music.texture = self.window.sprites['music_n']
            self.button_music.texture_pressed = self.window.sprites['music_t']
        else:
            self.button_music.texture = self.window.sprites['music_t']
            self.button_music.texture_pressed = self.window.sprites['music_n']

    def change_texture_sound(self):
        if self.bool_sound:
            self.button_sound.texture = self.window.sprites['sound_n']
            self.button_sound.texture_pressed = self.window.sprites['sound_t']
        else:
            self.button_sound.texture = self.window.sprites['sound_t']
            self.button_sound.texture_pressed = self.window.sprites['sound_n']

    def set_texture(self, object, texture):
        object.texture = texture
        object.texture_hovered = texture
        object.texture_pressed = texture
