import arcade

from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIInputText, Surface, UIMessageBox
from arcade.types import Color
from baseView import BaseView
from GameView import GameView
from re import fullmatch


class NewGameView(BaseView):
    def __init__(self, window):
        super().__init__(window)

        self.create_widget()

    def create_widget(self):
        self.l_anchor = UIAnchorLayout()
        self.l_anchor.default_anchor_x = 'left'
        self.l_anchor.default_anchor_y = 'bottom'

        self.lv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.lh_layout = UIBoxLayout(vertical=False, space_between=10)

        vert_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        hor_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        self.button_back = UITextureButton(texture=self.window.sprites['back_n'],
                                           texture_hovered=self.window.sprites['back_a'],
                                           texture_pressed=self.window.sprites['back_t'],
                                           scale=0.13)

        self.lv_layout.add(self.button_back)
        self.lv_layout.add(vert_space)
        self.lh_layout.add(hor_space)
        self.lh_layout.add(self.lv_layout)
        self.l_anchor.add(self.lh_layout)
        self.manager.add(self.l_anchor)

        self.c_anchor = UIAnchorLayout()
        self.cv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.sch_layout = UIBoxLayout(vertical=False, space_between=10)
        self.ch_layout = UIBoxLayout(vertical=False, space_between=10)

        self.input_name = UIInputText(width=600, height=112 * 0.4, border_color=(255, 255, 0), border_width=5,
                                      text_color=(255, 255, 0), font_size=20)

        self.input_seed = UIInputText(width=600, height=112 * 0.4, border_color=(255, 255, 0), border_width=5,
                                      text_color=(255, 255, 0), font_size=20)

        self.button_start = UITextureButton(texture=self.window.sprites['start_n'],
                                            texture_hovered=self.window.sprites['start_a'],
                                            texture_pressed=self.window.sprites['start_t'],
                                            scale=0.3)

        space = UISpace(width=100, height=100, color=(0, 0, 0, 0))
        sv_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        sh_space = UISpace(width=110, height=25, color=(0, 0, 0, 0))

        self.ch_layout.add(sh_space)
        self.ch_layout.add(self.input_name)
        self.sch_layout.add(sh_space)
        self.sch_layout.add(self.input_seed)
        self.cv_layout.add(self.ch_layout)
        self.cv_layout.add(self.sch_layout)
        self.cv_layout.add(space)
        self.c_anchor.add(self.cv_layout)
        self.manager.add(self.c_anchor)

        self.surface = Surface(size=(100, 100))

        self.b_anchor = UIAnchorLayout()
        self.b_anchor.default_anchor_y = "bottom"

        self.bv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.bv_layout.add(self.button_start)
        self.bv_layout.add(sv_space)

        self.b_anchor.add(self.bv_layout)
        self.manager.add(self.b_anchor)
        self.button_back.on_click = lambda event: self.back_triggered(event)
        self.button_start.on_click = lambda event: self.start_triggered(event)

    def on_draw(self):
        super().on_draw()

        x_offset = self.width // 2 - 375
        y_offset = self.height * 0.55 + 25

        for i in "NAME":
            self.surface.draw_texture(x_offset, y_offset, 24, 34, self.window.sprites[i])
            x_offset += 34

        x_offset = self.width // 2 - 375
        y_offset = self.height * 0.55 - 32

        for i in "SEED":
            self.surface.draw_texture(x_offset, y_offset, 24, 34, self.window.sprites[i])
            x_offset += 34

    def back_triggered(self, event):
        self.input_name.text = ""
        self.input_seed.text = ""
        self.window.show_view(self.window.menu_view)

    def start_triggered(self, event):
        name = self.input_name.text
        seed = self.input_seed.text
        self.input_name.text = ""
        self.input_seed.text = ""
        if fullmatch(r'\S\w*\S', name):
            data = {'name': name, 'seed': seed}
            self.window.game_view = GameView(self.window, data=data)
            self.window.is_game = True
            self.window.show_view(self.window.game_view)
        else:
            self.message_box = UIMessageBox(
                width=300,
                height=200,
                message_text=(
                    "Некорректное название мира"
                ),
                buttons=["OK"])
            self.manager.add(self.message_box)