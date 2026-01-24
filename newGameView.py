import arcade

from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIInputText
from baseView import BaseView


class NewGameView(BaseView):
    def __init__(self, window):
        super().__init__(window)

        self.load_textures()
        self.create_widget()

    def load_textures(self):
        self.texture_back_normal = arcade.load_texture("sprites/button_back/back_normal.png")
        self.texture_back_active = arcade.load_texture("sprites/button_back/back_active.png")
        self.texture_back_triggered = arcade.load_texture("sprites/button_back/back_triggered.png")

        self.texture_start_normal = arcade.load_texture("sprites/button_start/start_normal.png")
        self.texture_start_active = arcade.load_texture("sprites/button_start/start_active.png")
        self.texture_start_triggered = arcade.load_texture("sprites/button_start/start_triggered.png")

        self.texture_letter_S = arcade.load_texture("sprites/letters/S.png")
        self.texture_letter_E = arcade.load_texture("sprites/letters/E.png")
        self.texture_letter_D = arcade.load_texture("sprites/letters/D.png")

    def create_widget(self):
        self.l_anchor = UIAnchorLayout()
        self.l_anchor.default_anchor_x = 'left'
        self.l_anchor.default_anchor_y = 'bottom'

        self.lv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.lh_layout = UIBoxLayout(vertical=False, space_between=10)

        vert_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        hor_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        self.button_back = UITextureButton(texture=self.texture_back_normal,
                                           texture_hovered=self.texture_back_active,
                                           texture_pressed=self.texture_back_triggered,
                                           scale=0.13)

        self.lv_layout.add(self.button_back)
        self.lv_layout.add(vert_space)
        self.lh_layout.add(hor_space)
        self.lh_layout.add(self.lv_layout)
        self.l_anchor.add(self.lh_layout)
        self.manager.add(self.l_anchor)

        self.c_anchor = UIAnchorLayout()
        self.cv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.ch_layout = UIBoxLayout(vertical=False, space_between=10)

        self.letter_S = UITextureButton(texture=self.texture_letter_S, scale=0.4)
        self.fletter_E = UITextureButton(texture=self.texture_letter_E, scale=0.4)
        self.sletter_E = UITextureButton(texture=self.texture_letter_E, scale=0.4)
        self.letter_D = UITextureButton(texture=self.texture_letter_D, scale=0.4)

        self.ch_layout.add(self.letter_S)
        self.ch_layout.add(self.fletter_E)
        self.ch_layout.add(self.sletter_E)
        self.ch_layout.add(self.letter_D)

        self.input_seed = UIInputText(width=600, height=112 * 0.4, border_color=(255, 255, 0), border_width=5,
                                      text_color=(255, 255, 0), font_size=20)

        self.button_start = UITextureButton(texture=self.texture_start_normal,
                                            texture_hovered=self.texture_start_active,
                                            texture_pressed=self.texture_start_triggered,
                                            scale=0.3)

        space = UISpace(width=100, height=100, color=(0, 0, 0, 0))
        second_vert_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))


        self.ch_layout.add(self.input_seed)
        self.cv_layout.add(self.ch_layout)
        self.cv_layout.add(space)
        self.c_anchor.add(self.cv_layout)
        self.manager.add(self.c_anchor)

        self.b_anchor = UIAnchorLayout()
        self.b_anchor.default_anchor_y = "bottom"

        self.bv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.bv_layout.add(self.button_start)
        self.bv_layout.add(second_vert_space)

        self.b_anchor.add(self.bv_layout)
        self.manager.add(self.b_anchor)

        self.button_back.on_click = lambda event: self.back_triggered(event)

    def back_triggered(self, event):
        self.window.show_view(self.window.menu_view)