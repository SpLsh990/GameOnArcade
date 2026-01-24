import arcade
from arcade.gui import UIManager


class BaseView(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.manager = UIManager()

    def on_draw(self):
        self.manager.draw()

    def on_show(self):
        self.manager.enable()

    def on_hide(self):
        self.manager.disable()