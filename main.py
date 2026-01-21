import arcade
from arcade import View
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox


from background import BackgroundView
from mainView import MainMenuView
from settingsView import SettingsView
from newGameView import NewGameView
from savesView import SavesView
from gameView import GameView




SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Больше не миллион оттенков серого и синего"


class Window(arcade.Window):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable):
        super().__init__()

        self.background = BackgroundView(self.width, self.height)
        self.backList = arcade.SpriteList()
        self.backList.append(self.background)

        self.menu_view = MainMenuView(self)
        self.settings_view = SettingsView(self)
        #self.new_game_view = NewGameView(self)
        #self.saves_view = SavesView(self)
        #self.game_view = GameView(self)

        self.show_view(self.menu_view)

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
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, True)
    arcade.run()
