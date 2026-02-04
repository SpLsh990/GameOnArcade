import arcade
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox

from background import BackgroundView
from mainView import MainMenuView
from settingsView import SettingsView
from newGameView import NewGameView
from savesView import SavesView
from GameView import GameView
from pauseView import PauseView

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = '505'


class Window(arcade.Window):
    def __init__(self, width, height, title, fullscreen, resizable):
        super().__init__(width, height, title, fullscreen, resizable)
        self.background = BackgroundView(self.width, self.height)
        self.back_list = arcade.SpriteList()
        self.back_list.append(self.background)

        self.textures = {}

        self.load_textures()
        self.create_views()

        self.menu_music = arcade.load_sound("music/menu.ogg")
        self.game_music = arcade.load_sound("music/game.ogg")
        self.music_player = self.menu_music.play(loop=True, volume=round(
            0.01 * int(self.settings_view.bool_music and self.settings_view.music), 1))
        self.current_music = self.menu_music

        self.show_view(self.menu_view)

    def load_textures(self):
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.textures[f"{letter}_n"] = arcade.load_texture(f"sprites/letters_normal/{letter}.png")
            self.textures[f"{letter}_a"] = arcade.load_texture(f"sprites/letters_active/{letter}.png")
            self.textures[f"{letter}_t"] = arcade.load_texture(f"sprites/letters_triggered/{letter}.png")

        for digit in "0123456789":
            self.textures[f"{digit}_n"] = arcade.load_texture(f"sprites/digits_normal/{digit}.png")
            self.textures[f"{digit}_a"] = arcade.load_texture(f"sprites/digits_active/{digit}.png")
            self.textures[f"{digit}_t"] = arcade.load_texture(f"sprites/digits_triggered/{digit}.png")

        for symbol in ['', '-', '+', '_']:
            self.textures[symbol] = arcade.load_texture(f"sprites/signs/{symbol}.png")

        button_textures = {
            'skip_n': arcade.load_texture("sprites/buttons/button_skip/skip_normal.png"),
            'skip_a': arcade.load_texture("sprites/buttons/button_skip/skip_active.png"),
            'skip_t': arcade.load_texture("sprites/buttons/button_skip/skip_triggered.png"),
            'button_n': arcade.load_texture("sprites/buttons/button2/button_normal.png"),
            'button_a': arcade.load_texture("sprites/buttons/button2/button_active.png"),
            'button_t': arcade.load_texture("sprites/buttons/button2/button_triggered.png"),
            'button_e': arcade.load_texture("sprites/buttons/button2/button_empty.png")
        }

        self.textures = {**self.textures, **button_textures}

    def create_views(self):
        self.menu_view = MainMenuView(self)
        self.settings_view = SettingsView(self)
        self.new_game_view = NewGameView(self)
        self.saves_view = SavesView(self)
        self.saves_view.load_saves()
        self.pause_view = PauseView(self)
        self.game_view = None
        self.is_game = False

    def on_draw(self):
        self.clear()
        if self.background.enabled:
            self.back_list.draw()
        self.current_view.on_draw()

    def on_update(self, delta_time: float):
        self.background.update_animation(delta_time)
        if self.current_view:
            self.current_view.on_update(delta_time)
        if self.music_player:
            self.music_player.volume = round(
                0.01 * int(self.settings_view.bool_music and self.settings_view.music), 1)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.background.resize(width, height)

    def show_view(self, new_view):
        if isinstance(new_view, PauseView):
            self.background.enable()
        elif isinstance(new_view, GameView):
            self.background.disable()
            self.is_game = True
            self.game_view = new_view
        else:
            self.background.enable()
        if self.current_view:
            self.current_view.on_hide()

        super().show_view(new_view)
        if self.is_game and self.current_music != self.game_music:
            arcade.stop_sound(self.music_player)
            self.music_player = self.game_music.play(loop=True, volume=round(
                0.01 * int(self.settings_view.bool_music and self.settings_view.music), 1), speed=0.9)
            self.current_music = self.game_music
        else:
            if not self.music_player:
                self.music_player = self.menu_music.play(loop=True, volume=round(
                    0.01 * int(self.settings_view.bool_music and self.settings_view.music), 1))
                self.current_music = self.menu_music
        self.current_view.on_show()


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, False, False)
    arcade.run()


if __name__ == "__main__":
    main()
