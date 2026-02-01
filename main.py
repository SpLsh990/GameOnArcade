import arcade
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox
import threading

from background import BackgroundView
from mainView import MainMenuView
from settingsView import SettingsView
from newGameView import NewGameView
from savesView import SavesView
from GameView import GameView
from pauseView import PauseView

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "АВАВААВАВАВАВАВАВА"


class Window(arcade.Window):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen, resizable):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen, resizable)

        self.background = BackgroundView(self.width, self.height)
        self.backList = arcade.SpriteList()
        self.backList.append(self.background)

        self.textures = {}
        self.load_textures()

        self.music = {}
        self.musicPlayer = None
        self.load_music()

        self.menu_view = MainMenuView(self)
        self.settings_view = SettingsView(self)
        self.new_game_view = NewGameView(self)
        self.saves_view = SavesView(self)
        self.saves_view.load_saves()
        self.pause_view = PauseView(self)
        self.is_game = False
        self.show_view(self.menu_view)

    def load_music(self):
        self.music["menu"] = arcade.load_sound("music/menu.ogg")
        self.music["game"] = arcade.load_sound("music/game.ogg")

    def load_textures(self):
        for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.textures[f"{i}_n"] = arcade.load_texture(f"sprites/letters_normal/{i}.png")
            self.textures[f"{i}_a"] = arcade.load_texture(f"sprites/letters_active/{i}.png")
            self.textures[f"{i}_t"] = arcade.load_texture(f"sprites/letters_triggered/{i}.png")
        for i in "0123456789":
            self.textures[f"{i}_n"] = arcade.load_texture(f"sprites/digits_normal/{i}.png")
            self.textures[f"{i}_a"] = arcade.load_texture(f"sprites/digits_active/{i}.png")
            self.textures[f"{i}_t"] = arcade.load_texture(f"sprites/digits_triggered/{i}.png")
        for i in ['', '-', '+', '_']:
            self.textures[i] = arcade.load_texture(f"sprites/signs/{i}.png")

        self.textures['skip_n'] = arcade.load_texture("sprites/buttons/button_skip/skip_normal.png")
        self.textures['skip_a'] = arcade.load_texture("sprites/buttons/button_skip/skip_active.png")
        self.textures['skip_t'] = arcade.load_texture("sprites/buttons/button_skip/skip_triggered.png")
        self.textures['button_n'] = arcade.load_texture("sprites/buttons/button2/button_normal.png")
        self.textures['button_a'] = arcade.load_texture("sprites/buttons/button2/button_active.png")
        self.textures['button_t'] = arcade.load_texture("sprites/buttons/button2/button_triggered.png")
        self.textures['button_e'] = arcade.load_texture("sprites/buttons/button2/button_empty.png")

    def on_draw(self):
        self.clear()
        if self.background.enabled:
            self.backList.draw()
        self._current_view.on_draw()

    def on_update(self, delta_time: float):
        self.background.update_animation(delta_time)
        if self._current_view:
            self._current_view.on_update(delta_time)
    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.background.resize(width, height)

    def show_view(self, new_view):
        if isinstance(new_view, GameView):
            self.background.disable()
        else:
            self.background.enable()
        if self._current_view:
            self._current_view.on_hide()
        super().show_view(new_view)
        self._current_view.on_show()


if __name__ == "__main__":
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Больше не миллион оттенков серого и синего", False, False)
    arcade.run()
