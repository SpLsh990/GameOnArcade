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

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)

    def on_update(self, delta_time):
        fps = 1 / delta_time if delta_time > 0 else 0
        if fps < 20:
            print(f"FPS {fps:.3f}")
