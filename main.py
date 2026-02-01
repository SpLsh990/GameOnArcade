import arcade
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox
from background import BackgroundView
from mainView import MainMenuView
from settingsView import SettingsView
from newGameView import NewGameView
from savesView import SavesView
from GameView import GameView
from pauseView import PauseView

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "АВАВААВАВАВАВАВАВА"


# TODO Сделать игровой GUI, исправить кучу костылей
class Window(arcade.Window):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen, resizable):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen, resizable, center_window=True)

        self.background = BackgroundView(self.width, self.height)
        self.backList = arcade.SpriteList()
        self.backList.append(self.background)

        self.sprites = {}
        self.load_textures()

        self.menu_view = MainMenuView(self)
        self.settings_view = SettingsView(self)
        self.new_game_view = NewGameView(self)
        self.saves_view = SavesView(self)
        self.saves_view.load_saves()
        self.pause_view = PauseView(self)
        self.is_game = False
        self.show_view(self.menu_view)


    def load_textures(self):
        for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.sprites[f"{i}_n"] = arcade.load_texture(f"sprites/letters_normal/{i}.png")
            self.sprites[f"{i}_a"] = arcade.load_texture(f"sprites/letters_active/{i}.png")
            self.sprites[f"{i}_t"] = arcade.load_texture(f"sprites/letters_triggered/{i}.png")
        for i in "0123456789":
            self.sprites[f"{i}_n"] = arcade.load_texture(f"sprites/digits_normal/{i}.png")
            self.sprites[f"{i}_a"] = arcade.load_texture(f"sprites/digits_active/{i}.png")
            self.sprites[f"{i}_t"] = arcade.load_texture(f"sprites/digits_triggered/{i}.png")
        for i in ['', '-', '+', '_']:
            self.sprites[i] = arcade.load_texture(f"sprites/signs/{i}.png")

        self.sprites['new_game_n'] = arcade.load_texture("sprites/buttons/button_new_game/new_game_normal.png")
        self.sprites['new_game_a'] = arcade.load_texture("sprites/buttons/button_new_game/new_game_active.png")
        self.sprites['new_game_t'] = arcade.load_texture("sprites/buttons/button_new_game/new_game_triggered.png")
        self.sprites['saves_n'] = arcade.load_texture('sprites/buttons/button_saves/saves_normal.png')
        self.sprites['saves_a'] = arcade.load_texture('sprites/buttons/button_saves/saves_active.png')
        self.sprites['saves_t'] = arcade.load_texture('sprites/buttons/button_saves/saves_triggered.png')
        self.sprites['exit_n'] = arcade.load_texture("sprites/buttons/button_exit/exit_normal.png")
        self.sprites['exit_a'] = arcade.load_texture("sprites/buttons/button_exit/exit_active.png")
        self.sprites['exit_t'] = arcade.load_texture("sprites/buttons/button_exit/exit_triggered.png")
        self.sprites['back_n'] = arcade.load_texture("sprites/buttons/button_back/back_normal.png")
        self.sprites['back_a'] = arcade.load_texture("sprites/buttons/button_back/back_active.png")
        self.sprites['back_t'] = arcade.load_texture("sprites/buttons/button_back/back_triggered.png")
        self.sprites['apply_n'] = arcade.load_texture("sprites/buttons/button_apply/apply_normal.png")
        self.sprites['apply_a'] = arcade.load_texture("sprites/buttons/button_apply/apply_active.png")
        self.sprites['apply_t'] = arcade.load_texture("sprites/buttons/button_apply/apply_triggered.png")
        self.sprites['music_n'] = arcade.load_texture("sprites/buttons/button_music/music_normal.png")
        self.sprites['music_a'] = arcade.load_texture("sprites/buttons/button_music/music_active.png")
        self.sprites['music_t'] = arcade.load_texture("sprites/buttons/button_music/music_triggered.png")
        self.sprites['sound_n'] = arcade.load_texture("sprites/buttons/button_sound/sound_normal.png")
        self.sprites['sound_a'] = arcade.load_texture("sprites/buttons/button_sound/sound_active.png")
        self.sprites['sound_t'] = arcade.load_texture("sprites/buttons/button_sound/sound_triggered.png")
        self.sprites['start_n'] = arcade.load_texture("sprites/buttons/button_start/start_normal.png")
        self.sprites['start_a'] = arcade.load_texture("sprites/buttons/button_start/start_active.png")
        self.sprites['start_t'] = arcade.load_texture("sprites/buttons/button_start/start_triggered.png")
        self.sprites['delete_n'] = arcade.load_texture("sprites/buttons/button_delete/delete_normal.png")
        self.sprites['delete_a'] = arcade.load_texture("sprites/buttons/button_delete/delete_active.png")
        self.sprites['delete_t'] = arcade.load_texture("sprites/buttons/button_delete/delete_triggered.png")
        self.sprites['settings_n'] = arcade.load_texture("sprites/buttons/button_settings/settings_normal.png")
        self.sprites['settings_a'] = arcade.load_texture("sprites/buttons/button_settings/settings_active.png")
        self.sprites['settings_t'] = arcade.load_texture("sprites/buttons/button_settings/settings_triggered.png")
        self.sprites['continue_n'] = arcade.load_texture("sprites/buttons/button_continue/continue_normal.png")
        self.sprites['continue_a'] = arcade.load_texture("sprites/buttons/button_continue/continue_active.png")
        self.sprites['continue_t'] = arcade.load_texture("sprites/buttons/button_continue/continue_triggered.png")
        self.sprites['skip_n'] = arcade.load_texture("sprites/buttons/button_skip/skip_normal.png")
        self.sprites['skip_a'] = arcade.load_texture("sprites/buttons/button_skip/skip_active.png")
        self.sprites['skip_t'] = arcade.load_texture("sprites/buttons/button_skip/skip_triggered.png")
        self.sprites['button_n'] = arcade.load_texture("sprites/buttons/button2/button_normal.png")
        self.sprites['button_a'] = arcade.load_texture("sprites/buttons/button2/button_active.png")
        self.sprites['button_t'] = arcade.load_texture("sprites/buttons/button2/button_triggered.png")
        self.sprites['button_e'] = arcade.load_texture("sprites/buttons/button2/button_empty.png")

    def on_draw(self):
        self.clear()
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
        if not isinstance(new_view, GameView):
            self.background.enable()
        else:
            self.background.disable()
        if self._current_view:
            self._current_view.on_hide()
        super().show_view(new_view)
        self._current_view.on_show()


if __name__ == "__main__":
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Больше не миллион оттенков серого и синего", True, False)
    arcade.run()
