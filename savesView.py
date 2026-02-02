import arcade
import json
import pickle
from pathlib import Path
from arcade.gui import UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIInteractiveWidget, Surface, UIMessageBox
from arcade import Section
from baseView import BaseView
from GameView import GameView
from saveSlot import SaveSlot
from CustomButton import CustomButton


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

        self.button_back = CustomButton(self.width * 0.15, self.height * 0.075, "BACK", self.width * 0.00019,
                                        self.width * 0.00019,
                                        self.window.textures['button_n'],
                                        self.window.textures['button_a'],
                                        self.window.textures['button_t'])

        self.button_start = CustomButton(self.width * 0.2, self.height * 0.1, "START", self.width * 0.00023,
                                         self.width * 0.00023,
                                         self.window.textures['button_n'],
                                         self.window.textures['button_a'],
                                         self.window.textures['button_t'])

        self.button_delete = CustomButton(self.width * 0.2, self.height * 0.1, "DELETE", self.width * 0.00023,
                                          self.width * 0.00023,
                                          self.window.textures['button_n'],
                                          self.window.textures['button_a'],
                                          self.window.textures['button_t'])

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
                filejson = Path(f"./saves/{self.saves[save].data['name']}.json")
                filesaves = Path(f"./saves/{self.saves[save].data['name']}.sv")
                filejson.unlink(missing_ok=True)
                filesaves.unlink(missing_ok=True)
                self.cv_layout.remove(self.saves[save])
                del self.saves[save]

    def start_triggered(self, event):
        clicked = []
        for save in self.saves:
            if save.is_clicked():
                clicked.append(save)
        if len(clicked) == 1:
            self.window.game_view = GameView(self.window, data=clicked[0].data)
            self.window.is_game = True
            self.window.show_view(self.window.game_view)
        elif len(clicked) > 1:
            self.message_box = UIMessageBox(
                width=300,
                height=200,
                message_text=(
                    "Можно запустить только одну игру за раз"
                ),
                buttons=["OK"])
            self.manager.add(self.message_box)

    def on_draw(self):
        super().on_draw()
        if not self.saves:
            x_offset = self.width // 2 - 140
            y_offset = self.height // 2
            for char in "EMPTY":
                self.surface.draw_texture(x_offset, y_offset, 48, 68, self.window.textures[f"{char}_n"])
                x_offset += 58
        else:
            for save in self.saves:
                if save not in self.cv_layout.children:
                    self.cv_layout.add(save)

    # Функция добавления виджетов сохранения в стек
    def load_saves(self):
        path = Path("./saves")
        saves_json = list(path.glob("*.json"))
        saves_sv = list(path.glob("*.sv"))
        for i in range(len(self.saves) - 1, -1, -1):
            self.cv_layout.remove(self.saves[i])
            del self.saves[i]
        for save in range(len(saves_json)):
            with open(saves_json[save].resolve(), "r", encoding='utf-8') as save_json:
                data_json = json.load(save_json)
                try:
                    with open(saves_sv[save].resolve(), "rb") as save_sv:
                        data_sv = pickle.load(save_sv)
                        if data_json == data_sv:
                            self.saves.append(
                                SaveSlot(data=data_json, slot=save, width=self.width * 0.47, height=self.height * 0.13))
                except IndexError:
                    continue
