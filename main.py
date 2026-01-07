import arcade
from SeedNoiseGenerator import SeedNoiseGenerator
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SCREEN_TITLE = "mindustry0.5"

TILE_SIZE = 10
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
        seed = 19 #randint(1, 1000) ##100158
        self.generator = SeedNoiseGenerator(seed)
        self.world = {}
        print(self.generator.get_seed())

    def edges(self):
        for r in range(1, ROWS + 1):
            for c in range(1, COLS + 1):
                x = TILE_SIZE * (c - 1)
                y = TILE_SIZE * (r - 1)
                if r == 1 or r == ROWS or c == 1 or c == COLS:
                    self.world[(x, y)] = (40, 20, 30)

    def create_snow_and_water(self):
        for r in range(2, ROWS):
            for c in range(2, COLS):
                x = TILE_SIZE * (c - 1)
                y = TILE_SIZE * (r - 1)
                snow = self.generator.noise(x, y, octaves=4, persistence=0.5, lacunarity=2.0)
                water = self.generator.noise(x, y, octaves=2, seed_offset=1000)
                if snow > 0.565:
                    color = (255, 255, 255)  # Снег
                if water > 0.65:
                    color = (48, 15, 240)
                if snow < 0.56 and water < 0.66:
                    color = (120, 120, 120)  # Камень
                self.world[(x, y)] = color
        self.edges()

    def create_copper(self):
        for r in range(2, ROWS):
            for c in range(2, COLS):
                x = TILE_SIZE * (c - 1)
                y = TILE_SIZE * (r - 1)
                copper = self.generator.noise(x, y, octaves=1, seed_offset=255)
                if self.world[(x, y)] != (48, 15, 240) and copper > 0.7:
                    self.world[(x, y)] = (244, 132, 5)

    def checking(self):
        for r in range(2, ROWS):
            for c in range(2, COLS):
                x = TILE_SIZE * (c - 1)
                y = TILE_SIZE * (r - 1)
                res = {
                    'center': self.world[x, y],
                    'up': self.world[x, y + TILE_SIZE],
                    'down': self.world[x, y - TILE_SIZE],
                    'left': self.world[x - TILE_SIZE, y],
                    'right': self.world[x + TILE_SIZE, y],
                    'up-left': self.world[x - TILE_SIZE, y + TILE_SIZE],
                    'up-right': self.world[x + TILE_SIZE, y + TILE_SIZE],
                    'down-left': self.world[x - TILE_SIZE, y - TILE_SIZE],
                    'down-right': self.world[x + TILE_SIZE, y - TILE_SIZE],
                }
                if res['center'] != res['up'] and res['center'] != res['down']:
                    if res['center'] != res['left'] and res['center'] != res['right']:
                        colors = list(res.values())[1:]
                        while (40, 20, 30) in colors:
                            colors.pop(colors.index((40, 20, 30)))
                        self.world[x, y] = most_frequent_simple(colors)

    def on_draw(self):
        self.clear()
        self.create_snow_and_water()
        self.create_copper()
        self.checking()
        for r in range(1, ROWS + 1):
            for c in range(1, COLS + 1):
                x = TILE_SIZE * (c - 1)
                y = TILE_SIZE * (r - 1)
                arcade.draw_lbwh_rectangle_filled(x, y, TILE_SIZE, TILE_SIZE, self.world[(x, y)])


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
