import arcade
from arcade.gui import UIInteractiveWidget, Surface


class CustomButton(UIInteractiveWidget):
    def __init__(self, width, height, text="", size_letter=1, size_space=1, texture_normal=None, texture_active=None,
                 texture_triggered=None, change_text=True):
        super().__init__(width=width, height=height)
        self.texture_normal = texture_normal
        self.texture_active = texture_active if texture_active else texture_normal
        self.texture_triggered = texture_triggered if texture_triggered else texture_normal
        self.texture = self.texture_normal

        self.is_active = True
        self.change_text = change_text

        self.size_letter = size_letter
        self.size_space = size_space

        self.text = text.upper()
        self.textList_normal = arcade.SpriteList()
        self.textList_active = arcade.SpriteList()
        self.textList_triggered = arcade.SpriteList()

        self.alph = {}
        self.load_textures()
        self.load_text()

    def load_textures(self):
        for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.alph[f"{i}_n"] = arcade.load_texture(f"sprites/letters_normal/{i}.png")
            self.alph[f"{i}_a"] = arcade.load_texture(f"sprites/letters_active/{i}.png")
            self.alph[f"{i}_t"] = arcade.load_texture(f"sprites/letters_triggered/{i}.png")
        for i in "0123456789":
            self.alph[f"{i}_n"] = arcade.load_texture(f"sprites/digits_normal/{i}.png")
            self.alph[f"{i}_a"] = arcade.load_texture(f"sprites/digits_active/{i}.png")
            self.alph[f"{i}_t"] = arcade.load_texture(f"sprites/digits_triggered/{i}.png")
        for i in ['-', '+', '_']:
            self.alph[f"{i}_n"] = arcade.load_texture(f"sprites/signs/{i}.png")

    def load_text(self, text=None):
        if text:
            self.text = text
            self.textList_normal.clear()
            self.textList_active.clear()
            self.textList_triggered.clear()
        texure_n = ""
        texture_a = ""
        texture_t = ""
        letter_size = 80 * self.size_letter
        space_size = 16 * self.size_space
        lentext = len(self.text) - self.text.count(" ")
        x_offset = (self.width - (lentext * letter_size + (lentext - 1) * space_size)) // 2
        y_offset = self.height // 2 - (112 * self.size_letter // 2)
        for letter in self.text:
            if letter != " ":
                if letter not in "-_+" and self.change_text:
                    texture_n = self.alph.get(f"{letter}_n")
                    texture_a = self.alph.get(f"{letter}_a")
                    texture_t = self.alph.get(f"{letter}_t")
                else:
                    texture_n = self.alph.get(f"{letter}_n")
                    texture_a = self.alph.get(f"{letter}_n")
                    texture_t = self.alph.get(f"{letter}_n")
                self.textList_normal.append(
                    arcade.Sprite(texture_n, (self.size_letter, self.size_letter),
                                  x_offset + (80 * self.size_letter) // 2,
                                  y_offset + (112 * self.size_letter // 2)))
                self.textList_active.append(
                    arcade.Sprite(texture_a, (self.size_letter, self.size_letter),
                                  x_offset + (80 * self.size_letter) // 2,
                                  y_offset + (112 * self.size_letter // 2)))
                self.textList_triggered.append(
                    arcade.Sprite(texture_t, (self.size_letter, self.size_letter),
                                  x_offset + (80 * self.size_letter) // 2,
                                  y_offset + (112 * self.size_letter // 2)))
                x_offset += letter_size + space_size
            else:
                x_offset += space_size * 2

    def do_render(self, surface: Surface):
        if self.pressed:
            self.texture = self.texture_triggered if self.is_active else self.texture_normal
            self.textList = self.textList_triggered if self.is_active else self.textList_normal
        elif self.hovered:
            self.texture = self.texture_active
            self.textList = self.textList_active
        else:
            self.texture = self.texture_normal if self.is_active else self.texture_triggered
            self.textList = self.textList_normal if self.is_active else self.textList_triggered

        surface.draw_texture(0, 0, self.width, self.height, self.texture)
        self.textList.draw()

    def change(self, value):
        self.is_active = value


