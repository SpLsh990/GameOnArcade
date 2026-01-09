import arcade
from SeedNoiseGenerator import SeedNoiseGenerator
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
        self.generator = SeedNoiseGenerator(seed)
        self.colors = {'endworld': (40, 20, 30),
                       'stone': (100, 100, 100),
                       'snow': (255, 255, 255),
                       'water': (48, 15, 240),
                       'copper': (244, 132, 5),
                       'iron': (180, 175, 170),
                       'coal': (40, 40, 40),
                       'lithium': (100, 105, 155),
                       'titanium': (35, 45, 105),
                       'uranium': (55, 255, 0)
                       }
        self.world = {}
        print(self.generator.get_seed())

    def add_item(self, color, limit, octaves=4, seed_offset=0, persistence=0.5, lacunarity=2.0,
                 scale=0.01):
        for r in range(2, ROWS):
            for c in range(2, COLS):
                x = TILE_SIZE * (c - 1)
                y = TILE_SIZE * (r - 1)
                value = self.generator.noise(x, y, octaves, seed_offset, persistence, lacunarity, scale)
                if value > limit and (
                        self.world[(x, y)] == self.colors['stone'] or self.world[(x, y)] == self.colors['snow']):
                    self.world[(x, y)] = color

    def edges(self):
        for r in range(1, ROWS + 1):
            for c in range(1, COLS + 1):
                x = TILE_SIZE * (c - 1)
                y = TILE_SIZE * (r - 1)
                if r == 1 or r == ROWS or c == 1 or c == COLS:
                    self.world[(x, y)] = self.colors['endworld']

    def add_bioms(self):
        for r in range(2, ROWS):
            for c in range(2, COLS):
                x = TILE_SIZE * (c - 1)
                y = TILE_SIZE * (r - 1)
                snow = self.generator.noise(x, y, octaves=4, persistence=0.5, lacunarity=2.0)
                if snow > 1.55:
                    self.world[(x, y)] = self.colors['snow']
                else:
                    self.world[(x, y)] = self.colors['stone']

    def add_lithium(self):
        pass

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
                    'right': self.world[x + TILE_SIZE, y]
                }
                if res['center'] != res['up'] and res['center'] != res['down']:
                    if res['center'] != res['left'] and res['center'] != res['right']:
                        colors = list(res.values())[1:]
                        while self.colors['endworld'] in colors:
                            colors.pop(colors.index(self.colors['endworld']))
                        self.world[x, y] = most_frequent_simple(colors)

    def on_draw(self):
        self.clear()
        self.edges()
        self.add_bioms()
        self.add_item(self.colors['water'], 0.67, octaves=2, seed_offset=1000)
        self.add_item(self.colors['copper'], 0.67, octaves=2, seed_offset=255)
        self.add_item(self.colors['iron'], 0.67, octaves=2, seed_offset=2500)
        self.add_item(self.colors['coal'], 0.67, octaves=2, seed_offset=3000)
        self.add_item(self.colors['lithium'], 0.67, octaves=2, seed_offset=3500)
        self.add_item(self.colors['titanium'], 0.67, octaves=2, seed_offset=4500)
        self.add_item(self.colors['uranium'], 0.7, octaves=4, seed_offset=500)
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
