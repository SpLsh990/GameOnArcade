import arcade
from SeedNoiseGenerator import SeedNoiseGenerator
from ground import World
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Миллион оттенков серого и синего"

TILE_SIZE = 5
COLS = SCREEN_WIDTH // TILE_SIZE
ROWS = SCREEN_HEIGHT // TILE_SIZE


def most_frequent_simple(lst):
    counts = {}
    for item in lst:
        counts[item] = counts.get(item, 0) + 1
    max_item = max(counts, key=counts.get)
    return max_item


class MyGame(arcade.Window):
    def __init__(self, WIDTH, HEIGHT, SCREEN_TITLE):
        super().__init__(WIDTH, HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        seed = randint(1, 1000)
        self.world = World(seed, ROWS, COLS, TILE_SIZE)
        self.world.create_world()
        self.map = self.world.get_world()

        self.camera = arcade.camera.Camera2D()
        self.camera_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.camera_zoom = 1.0

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            for r in range(1, ROWS + 1):
                for c in range(1, COLS + 1):
                    x = TILE_SIZE * (c - 1)
                    y = TILE_SIZE * (r - 1)
                    arcade.draw_lbwh_rectangle_filled(x, y, TILE_SIZE, TILE_SIZE, self.map[x, y])

    def on_update(self, delta_time):
        self.camera.position = self.camera_pos
        self.camera.zoom = self.camera_zoom

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == arcade.MOUSE_BUTTON_LEFT:
            self.camera_pos[0] -= dx / self.camera_zoom
            self.camera_pos[1] -= dy / self.camera_zoom

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        zoom_factor = 1.1
        if scroll_y > 0:
            self.camera_zoom *= zoom_factor
        elif scroll_y < 0:
            self.camera_zoom /= zoom_factor


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
