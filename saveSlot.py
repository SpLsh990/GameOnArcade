import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UITextureButton, UISpace, UIOnClickEvent, \
    UIInteractiveWidget, Surface


class SaveSlot(UIInteractiveWidget):
    def __init__(self, data=None, slot=None):
        super().__init__(width=800, height=100)
        self.data = data
        self.slot = slot
        self.clicked = False

        self.sprites = {}
        self.load_textures()
        self.alph = self.sprites.keys()

        self.update_data(data)

    def load_textures(self):
        for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.sprites[i] = arcade.load_texture(f"sprites/letters/{i}.png")
        for i in "0123456789":
            self.sprites[i] = arcade.load_texture(f"sprites/digits/{i}.png")
        for i in ['', '-', '+', '_']:
            self.sprites[i] = arcade.load_texture(f"sprites/signs/{i}.png")
        self.sprites['slot_n'] = arcade.load_texture("sprites/button/button_normal.png")
        self.sprites['slot_a'] = arcade.load_texture("sprites/button/button_selected.png")

    def update_data(self, data):
        self.data = data
        self.name = self.data['name'].upper() if self.data else "EMPTY"
        self.wave = self.data['wave'] if self.data else "0"
        self.date = self.data['date'] if self.data else "00-00-0000"

    def on_click(self, event):
        super().on_click(event)
        self.clicked = not self.clicked

    def on_update(self, dt):
        self.texture = self.sprites['slot_a'] if self.clicked else self.sprites['slot_n']

    def back(self):
        self.clicked = False

    def is_clicked(self):
        return self.clicked

    def do_render(self, surface: Surface):
        if self.clicked or self.hovered:
            texture = self.sprites['slot_a']
        else:
            texture = self.sprites['slot_n']

        if texture:
            surface.draw_texture(0, 0, self.width, self.height, texture)

        x_offset = 30
        y_offset = int(self.height * 0.7)
        for i in self.name:
            if i in self.alph:
                char = self.sprites[i]
                if char:
                    surface.draw_texture(x_offset, y_offset, 14, 20, char)
                x_offset += 24
            else:
                x_offset += 10

        x_offset = self.width - 50
        for i in self.date[::-1]:
            if i in self.alph:
                char = self.sprites[i]
                if char:
                    surface.draw_texture(x_offset, y_offset, 14, 20, char)
                x_offset -= 24
            else:
                x_offset -= 10
        x_offset = 30
        y_offset = self.height * 0.3
        for i in f"WAVE - {self.slot}":
            if i in self.alph:
                char = self.sprites[i]
                if char:
                    surface.draw_texture(x_offset, y_offset, 14, 20, char)
                x_offset += 24
            else:
                x_offset += 10
