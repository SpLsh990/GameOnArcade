import arcade
from ground import World
from random import randint
from baseView import BaseView

# TODO реализовать сохранения

class GameView(BaseView):
    def __init__(self, window, rows=100, cols=100, tile_size=10, data=None):
        super().__init__(window)
        self.window = window
        self.data = data
        self.sprites = {
            "coal":arcade.load_texture("sprites/world/coal.png"),
            "copper": arcade.load_texture("sprites/world/copper.png"),
            "endworld": arcade.load_texture("sprites/world/endworld.png"),
            "iron": arcade.load_texture("sprites/world/iron.png"),
            "lithium": arcade.load_texture("sprites/world/lithium.png"),
            "mountains": arcade.load_texture("sprites/world/mountain.png"),
            "silver": arcade.load_texture("sprites/world/silver.png"),
            "snow": arcade.load_texture("sprites/world/snow.png"),
            "stone": arcade.load_texture("sprites/world/stone.png"),
            "uranium": arcade.load_texture("sprites/world/uranium.png"),
            "water": arcade.load_texture("sprites/world/water.png"),
        }
        self.spriteList = arcade.SpriteList()
        self.pause = False
        self.rows = rows
        self.cols = cols
        self.tile_size =tile_size
        seed = data['seed'] if data['seed'] else randint(1, 100000000)
        self.world = World(seed, self.rows, self.cols, self.tile_size)
        self.world.create_world()
        self.map = self.world.get_world()

        #self.pause_view = PauseView(self)
        self.camera = arcade.camera.Camera2D()
        self.camera_pos = [self.cols // 2 * self.tile_size, self.rows // 2 * self.tile_size]
        self.camera_zoom = 3.0

        for r in range(1, self.rows + 1):
            for c in range(1, self.cols + 1):
                x = self.tile_size * (c - 1)
                y = self.tile_size * (r - 1)
                tile = arcade.Sprite(self.sprites[self.map[x, y]], 1 / 160 * self.tile_size, x + self.tile_size // 2,
                                     y + self.tile_size // 2)
                self.spriteList.append(tile)

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.spriteList.draw()

    def on_update(self, delta_time):
        if self.pause:
            return
        self.camera.position = self.camera_pos
        self.camera.zoom = self.camera_zoom

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == arcade.MOUSE_BUTTON_LEFT:
            self.camera_pos[0] -= dx / self.camera_zoom
            self.camera_pos[1] -= dy / self.camera_zoom

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        zoom_factor = 1.1
        if scroll_y > 0:
            if self.camera_zoom * zoom_factor < 4.0:
                self.camera_zoom *= zoom_factor
        elif scroll_y < 0:
            if self.camera_zoom / zoom_factor > 1:
                self.camera_zoom /= zoom_factor

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            print('esc')
            #self.pause = not self.pause
            #if self.pause:
            #    self.window.show_view(self.pause_view)

