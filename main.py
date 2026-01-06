import arcade
from SeedNoiseGenerator import SeedNoiseGenerator
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "mindustry0.5"

TILE_SIZE = 10
COLS = SCREEN_WIDTH // TILE_SIZE + 1
ROWS = SCREEN_HEIGHT // TILE_SIZE + 1


class MyGame(arcade.Window):
    def __init__(self, WIDTH, HEIGHT, SCREEN_TITLE):
        super().__init__(WIDTH, HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        seed = randint(1, 1000)
        self.generator = SeedNoiseGenerator(seed)
        self.world = {}

    def create_world(self):
        for r in range(ROWS):
            for c in range(COLS):
                x = c * TILE_SIZE - TILE_SIZE // 2
                y = r * TILE_SIZE - TILE_SIZE // 2
                value = self.generator.noise(x, y)
                if value > 0.55:
                    color = (255, 255, 255) # Снег
                else:
                    color = (120, 120, 120) # Камень
                self.world[(x, y)] = color
    def on_draw(self):
        self.clear()
        self.create_world()
        for r in range(ROWS):
            for c in range(COLS):
                x = c * TILE_SIZE - TILE_SIZE // 2
                y = r * TILE_SIZE - TILE_SIZE // 2
                arcade.draw_lbwh_rectangle_filled(x, y, TILE_SIZE, TILE_SIZE, self.world[(x, y)])


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
