import arcade
from SeedNoiseGenerator import SeedNoiseGenerator
from random import randint

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "mindustry0.5"

TILE_SIZE = 10
COLS = SCREEN_WIDTH // TILE_SIZE + 1
ROWS = SCREEN_HEIGHT // TILE_SIZE + 1


class MyGame(arcade.Window):
    def __init__(self, WIDTH, HEIGHT, SCREEN_TITLE):
        super().__init__(WIDTH, HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        seed = 58 # randint(1, 1000) #1001
        self.generator = SeedNoiseGenerator(seed)
        self.world = {}
        print(self.generator.get_seed())

    def create_snow_and_water(self):
        for r in range(1, ROWS):
            for c in range(1, COLS):
                x = c * TILE_SIZE - TILE_SIZE // 2
                y = r * TILE_SIZE - TILE_SIZE // 2
                snow = self.generator.noise(x, y, octaves=4, persistence=0.5, lacunarity=2.0)
                water = self.generator.noise(x, y, octaves=2, seed_offset=1000)
                if snow > 0.565:
                    color = (255, 255, 255)  # Снег
                if water > 0.65:
                    color = (48, 15, 240)
                if snow < 0.56 and water < 0.66:
                    color = (120, 120, 120)  # Камень
                self.world[(x, y)] = color

    def create_copper(self):
        for r in range(1, ROWS):
            for c in range(1, COLS):
                x = c * TILE_SIZE - TILE_SIZE // 2
                y = r * TILE_SIZE - TILE_SIZE // 2
                copper = self.generator.noise(x, y, octaves=1, seed_offset=255)
                if self.world[(x, y)] != (48, 15, 240) and copper > 0.7:
                    self.world[(x, y)] = (244, 132, 5)

    def on_draw(self):
        self.clear()
        self.create_snow_and_water()
        self.create_copper()
        for r in range(1, ROWS):
            for c in range(1, COLS):
                x = c * TILE_SIZE - TILE_SIZE // 2
                y = r * TILE_SIZE - TILE_SIZE // 2
                arcade.draw_lbwh_rectangle_filled(x, y, TILE_SIZE, TILE_SIZE, self.world[(x, y)])


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
