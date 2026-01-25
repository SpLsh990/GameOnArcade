import arcade
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIInteractiveWidget, Surface
from baseView import BaseView
from gameView import GameView
from saveSlot import SaveSlot


class SavesView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.saves = []
        self.surface = Surface(size=(100, 100))
        self.fl = True
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
                                           texture_pressed=self.window.sprites['back_t'],
                                           scale=0.13)

        self.button_start = UITextureButton(texture=self.window.sprites['start_n'],
                                            texture_hovered=self.window.sprites['start_a'],
                                            texture_pressed=self.window.sprites['start_t'],
                                            scale=0.3)

        self.button_delete = UITextureButton(texture=self.window.sprites['delete_n'],
                                             texture_hovered=self.window.sprites["delete_a"],
                                             texture_pressed=self.window.sprites['delete_t'],
                                             scale=0.3
                                             )

        sv_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        self.lv_layout.add(self.button_back)
        self.lv_layout.add(v_space)
        self.lh_layout.add(h_space)
        self.lh_layout.add(self.lv_layout)
        self.l_anchor.add(self.lh_layout)
        self.manager.add(self.l_anchor)

        self.b_anchor = UIAnchorLayout()
        self.b_anchor.default_anchor_y = "bottom"

        self.bh_layout = UIBoxLayout(vertical=False, space_between=10)
        self.bv_layout = UIBoxLayout(vertical=True, space_between=10)
        self.bh_layout.add(self.button_delete)
        self.bh_layout.add(self.button_start)
        self.bv_layout.add(self.bh_layout)
        self.bv_layout.add(sv_space)

        self.b_anchor.add(self.bv_layout)
        self.manager.add(self.b_anchor)

        self.c_anchor = UIAnchorLayout()
        self.cv_layout = UIBoxLayout(vertical=True, space_between=10)

        self.c_anchor.add(self.cv_layout)
        self.manager.add(self.c_anchor)

        self.button_back.on_click = lambda event: self.back_triggered(event)
        self.button_delete.on_click = lambda event: self.delete_triggered(event)
        self.button_start.on_click = lambda event: self.start_triggered(event)

    def back_triggered(self, event):
        self.window.show_view(self.window.menu_view)
        for i in self.saves:
            i.back()

    def delete_triggered(self, event):
        for save in range(len(self.saves) - 1, -1, -1):
            if self.saves[save].is_clicked():
                self.cv_layout.remove(self.saves[save])
                self.saves.pop(save)

    def start_triggered(self, event):
        clicked = 0
        for save in self.saves:
            if save.is_clicked():
                clicked.append(save)
        if len(clicked) == 0:
            ...
        elif len(clicked) > 1:
            ...
        else:
            self.window.gameview = GameView(self.window, data=clicked[0].data)
            self.window.show_view(self.window.gameview)

    def on_draw(self):
        super().on_draw()
        if not self.saves:
            x_offset = self.width // 2 - 140
            y_offset = self.height // 2
            for char in "EMPTY":
                self.surface.draw_texture(x_offset, y_offset, 48, 68, self.window.sprites[char])
                x_offset += 58
        else:
            for save in self.saves:
                if save not in self.cv_layout.children:
                    self.cv_layout.add(save)
