import arcade
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox, UISlider
from baseView import BaseView


class SettingsView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.bool_sound = True
        self.bool_music = True

        self.sound = 0
        self.music = 0

        self.load_textures()
        self.create_widget()

    def load_textures(self):
        self.texture_back_normal = arcade.load_texture("sprites/button_back/back_normal.png")
        self.texture_back_active = arcade.load_texture("sprites/button_back/back_active.png")
        self.texture_back_triggered = arcade.load_texture("sprites/button_back/back_triggered.png")

        self.texture_apply_normal = arcade.load_texture("sprites/button_apply/apply_normal.png")
        self.texture_apply_active = arcade.load_texture("sprites/button_apply/apply_active.png")
        self.texture_apply_triggered = arcade.load_texture("sprites/button_apply/apply_triggered.png")

        self.texture_music_normal = arcade.load_texture("sprites/button_music/music_normal.png")
        self.texture_music_active = arcade.load_texture("sprites/button_music/music_active.png")
        self.texture_music_triggered = arcade.load_texture("sprites/button_music/music_triggered.png")

        self.texture_sound_normal = arcade.load_texture("sprites/button_sound/sound_normal.png")
        self.texture_sound_active = arcade.load_texture("sprites/button_sound/sound_active.png")
        self.texture_sound_triggered = arcade.load_texture("sprites/button_sound/sound_triggered.png")

        self.texture_minus = arcade.load_texture("sprites/signs/minus.png")
        self.texture_plus = arcade.load_texture("sprites/signs/plus.png")

        self.texture_letter_F = arcade.load_texture("sprites/letters/F.png")
        self.texture_letter_O = arcade.load_texture("sprites/letters/O.png")

        self.digits = {
            "0": arcade.load_texture("sprites/digits/0.png"),
            "1": arcade.load_texture("sprites/digits/1.png"),
            "2": arcade.load_texture("sprites/digits/2.png"),
            "3": arcade.load_texture("sprites/digits/3.png"),
            "4": arcade.load_texture("sprites/digits/4.png"),
            "5": arcade.load_texture("sprites/digits/5.png"),
            "6": arcade.load_texture("sprites/digits/6.png"),
            "7": arcade.load_texture("sprites/digits/7.png"),
            "8": arcade.load_texture("sprites/digits/8.png"),
            "9": arcade.load_texture("sprites/digits/9.png"),
        }

    def create_widget(self):
        self.l_anchor = UIAnchorLayout()
        self.l_anchor.default_anchor_x = 'left'
        self.l_anchor.default_anchor_y = 'bottom'

        self.lv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.lh_layout = UIBoxLayout(vertical=False, space_between=10)

        v_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        h_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        self.button_back = UITextureButton(texture=self.texture_back_normal,
                                      texture_hovered=self.texture_back_active,
                                      texture_pressed=self.texture_back_triggered, scale=0.13)

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

        self.button_music = UITextureButton(texture=self.texture_music_normal,
                                            texture_hovered=self.texture_music_active,
                                            texture_pressed=self.texture_music_triggered, scale=0.3)

        self.button_sound = UITextureButton(texture=self.texture_sound_normal,
                                            texture_hovered=self.texture_sound_active,
                                            texture_pressed=self.texture_sound_triggered, scale=0.3)

        """button_apply = UITextureButton(texture=self.texture_apply_normal,
                                       texture_hovered=self.texture_apply_active,
                                       texture_pressed=self.texture_apply_triggered, scale=0.25)
        """
        cu_space = UISpace(width=100, height=200, color=(0, 0, 0, 0))
        cd_space = UISpace(width=100, height=200, color=(0, 0, 0, 0))

        self.music_slider = UISlider(width=300, height=50, min_value=0, max_value=100, value=self.music)
        self.sound_slider = UISlider(width=300, height=50, min_value=0, max_value=100, value=self.sound)

        self.first_dig_music = UITextureButton(texture=self.digits[f"{self.music:03}"[0]], scale=0.3)
        self.second_dig_music = UITextureButton(texture=self.digits[f"{self.music:03}"[1]], scale=0.3)
        self.third_dig_music = UITextureButton(texture=self.digits[f"{self.music:03}"[2]], scale=0.3)

        self.first_dig_sound = UITextureButton(texture=self.digits[f"{self.sound:03}"[0]], scale=0.3)
        self.second_dig_sound = UITextureButton(texture=self.digits[f"{self.sound:03}"[1]], scale=0.3)
        self.third_dig_sound = UITextureButton(texture=self.digits[f"{self.sound:03}"[2]], scale=0.3)

        self.minus_music = UITextureButton(texture=self.texture_minus, scale=0.35)
        self.plus_music = UITextureButton(texture=self.texture_plus, scale=0.35)

        self.minus_sound = UITextureButton(texture=self.texture_minus, scale=0.35)
        self.plus_sound = UITextureButton(texture=self.texture_plus, scale=0.35)

        self.cmusic_layout.add(self.button_music)
        self.cmusic_layout.add(self.music_slider)
        self.cmusic_layout.add(self.first_dig_music)
        self.cmusic_layout.add(self.second_dig_music)
        self.cmusic_layout.add(self.third_dig_music)
        self.cmusic_layout.add(self.minus_music)
        self.cmusic_layout.add(self.plus_music)

        self.csound_layout.add(self.button_sound)
        self.csound_layout.add(self.sound_slider)
        self.csound_layout.add(self.first_dig_sound)
        self.csound_layout.add(self.second_dig_sound)
        self.csound_layout.add(self.third_dig_sound)
        self.csound_layout.add(self.minus_sound)
        self.csound_layout.add(self.plus_sound)

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

        self.minus_music.on_click = lambda event: self.reduce_music(event)
        self.plus_music.on_click = lambda event: self.increase_music(event)

        self.minus_sound.on_click = lambda event: self.reduce_sound(event)
        self.plus_sound.on_click = lambda event: self.increase_sound(event)

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
            self.set_texture(self.first_dig_music, self.digits[music[0]])
            self.set_texture(self.second_dig_music, self.digits[music[1]])
            self.set_texture(self.third_dig_music, self.digits[music[2]])
        else:
            self.set_texture(self.first_dig_music, self.texture_letter_O)
            self.set_texture(self.second_dig_music, self.texture_letter_F)
            self.set_texture(self.third_dig_music, self.texture_letter_F)

    def change_digits_sound(self):
        if self.bool_sound:
            sound = list(str(f"{self.sound:03}"))
            self.set_texture(self.first_dig_sound, self.digits[sound[0]])
            self.set_texture(self.second_dig_sound, self.digits[sound[1]])
            self.set_texture(self.third_dig_sound, self.digits[sound[2]])
        else:
            self.set_texture(self.first_dig_sound, self.texture_letter_O)
            self.set_texture(self.second_dig_sound, self.texture_letter_F)
            self.set_texture(self.third_dig_sound, self.texture_letter_F)

    def change_texture_music(self):
        if self.bool_music:
            self.button_music.texture = self.texture_music_normal
            self.button_music.texture_pressed = self.texture_music_triggered
        else:
            self.button_music.texture = self.texture_music_triggered
            self.button_music.texture_pressed = self.texture_music_normal

    def change_texture_sound(self):
        if self.bool_sound:
            self.button_sound.texture = self.texture_sound_normal
            self.button_sound.texture_pressed = self.texture_sound_triggered
        else:
            self.button_sound.texture = self.texture_sound_triggered
            self.button_sound.texture_pressed = self.texture_sound_normal

    def set_texture(self, object, texture):
        object.texture = texture
        object.texture_hovered = texture
        object.texture_pressed = texture
