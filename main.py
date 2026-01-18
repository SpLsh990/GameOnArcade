import arcade
from arcade import View
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox

from newGameView import NewGameView
from savesView import SavesView
from settingsView import SettingsView
from background import BackgroundView
from gameView import GameView

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Миллион оттенков серого и синего"


class Window(arcade.Window):
    def __init__(self, width, height, title, resizable):
        super().__init__()

        self.background = BackgroundView(self.width, self.height)
        self.backList = arcade.SpriteList()
        self.backList.append(self.background)

        self.menu_view = MainMenuView(self)
        self.settings_view = SettingsView(self)
        self.new_game_view = NewGameView(self)
        self.saves_view = SavesView(self)
        self.game_view = GameView(self)

    def on_draw(self):
        self.clear()
        self.backgrList.draw()

    def on_update(self, delta_time: float):
        self.background.update_animation(delta_time)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.background.resize(width, height)

    def show_view(self, new_view):
        if not isinstance(new_view, GameView):
            self.background.enable()
        else:
            self.background.disable()

        super().show_view(new_view)



if __name__ == "__main__":
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    arcade.run()
