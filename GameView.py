import arcade
from world import World
from random import randint
from baseView import BaseView
from pauseView import PauseView


class GameView(BaseView):
    def __init__(self, window, rows=100, cols=100, tile_size=10, data=None):
        super().__init__(window)
        self.window = window
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size

        self.data = data
        self.sprites = {
            "coal": arcade.load_texture("sprites/world/coal.png"),
            "copper": arcade.load_texture("sprites/world/copper.png"),
            "endworld": arcade.load_texture("sprites/world/endworld.png"),
            "iron": arcade.load_texture("sprites/world/iron.png"),
            "lithium": arcade.load_texture("sprites/world/lithium.png"),
            "mountains": arcade.load_texture("sprites/world/mountain.png"),
            "stone": arcade.load_texture("sprites/world/stone.png"),
            "uranium": arcade.load_texture("sprites/world/uranium.png"),
            "water": arcade.load_texture("sprites/world/water.png"),
            "titanium": arcade.load_texture("sprites/world/titanium.png")
        }
        self.spriteList = arcade.SpriteList()

        self.pause = False

        self.data['seed'] = data['seed'] if data['seed'] else randint(1, 100000000)

        self.world = World(self.data['seed'], self.rows, self.cols, self.tile_size)
        self.world.create_world()

        self.map, self.collisions = self.world.get_world()

        self.camera = arcade.camera.Camera2D()
        self.camera_pos = [self.cols // 2 * self.tile_size, self.rows // 2 * self.tile_size]
        self.camera_zoom = 3.0

        for (x, y), item in self.map.items():
            tile = arcade.Sprite(self.sprites[item], 1 / 160 * self.tile_size, x + self.tile_size // 2,
                                 y + self.tile_size // 2)
            self.spriteList.append(tile)

        self.dash = {}
        # self.phys_engine = arcade.PhysicsEngineSimple(self.data['entity'], self.collisions)

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.spriteList.draw()

    def on_update(self, delta_time):
        if self.pause:
            return
        self.check_camera()
        self.camera.position = self.camera_pos
        self.camera.zoom = self.camera_zoom
        # self.phys_engine.update()

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
            if self.camera_zoom / zoom_factor > 1.5:
                self.camera_zoom /= zoom_factor

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.pause = True
            if self.pause:
                self.window.show_view(self.window.pause_view)

    # Ограничение камеры в пределах игрового мира
    def check_camera(self):
        zoom = self.camera.zoom

        half_viewport_width = (self.width / 2) / zoom
        half_viewport_height = (self.height / 2) / zoom

        min_x = half_viewport_width
        max_x = (self.cols * self.tile_size) - half_viewport_width
        min_y = half_viewport_height
        max_y = (self.rows * self.tile_size) - half_viewport_height

        self.camera_pos[0] = max(min_x, min(self.camera_pos[0], max_x))
        self.camera_pos[1] = max(min_y, min(self.camera_pos[1], max_y))
