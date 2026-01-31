from SeedNoiseGenerator import SeedNoiseGenerator


def most_frequent_simple(lst):
    counts = {}
    for item in lst:
        counts[item] = counts.get(item, 0) + 1
    max_item = max(counts, key=counts.get)
    return max_item


class World:
    def __init__(self, seed, ROWS, COLS, TILE_SIZE):
        self.ROWS = ROWS
        self.COLS = COLS
        self.TILE_SIZE = TILE_SIZE
        self.generator = SeedNoiseGenerator(seed)
        self.colors = {'endworld': (40, 20, 30),
                       'mountains': (55, 0, 0),
                       'stone': (100, 100, 100),
                       'snow': (255, 255, 255),
                       'water': (48, 15, 240),
                       'copper': (244, 132, 5),
                       'iron': (255, 255, 180),
                       'coal': (40, 40, 40),
                       'lithium': (100, 105, 155),
                       'titanium': (35, 45, 105),
                       'uranium': (55, 255, 0),
                       'silver': (214, 235, 202)
                       }
        self.world = {}
        self.collisions = []

    def add_item(self, item, limit, octaves=4, seed_offset=0, persistence=0.5, lacunarity=2.0,
                 scale=0.01):
        for r in range(2, self.ROWS):
            for c in range(2, self.COLS):
                x = self.TILE_SIZE * (c - 1)
                y = self.TILE_SIZE * (r - 1)
                value = self.generator.noise(x, y, octaves, seed_offset, persistence, lacunarity, scale)
                if value > limit and self.world[(x, y)] == 'stone':
                    self.world[(x, y)] = item
                    if item == "mountains":
                        self.collisions.append((x, y))

    def edges(self):
        for r in range(1, self.ROWS + 1):
            for c in range(1, self.COLS + 1):
                x = self.TILE_SIZE * (c - 1)
                y = self.TILE_SIZE * (r - 1)
                if r == 1 or r == self.ROWS or c == 1 or c == self.COLS:
                    self.world[(x, y)] = 'endworld'

    def add_bioms(self):
        for r in range(1, self.ROWS):
            for c in range(1, self.COLS):
                x = self.TILE_SIZE * (c - 1)
                y = self.TILE_SIZE * (r - 1)
                if r == 1 or r == self.ROWS or c == 1 or c == self.COLS:  # Добавление краев карты
                    self.world[x, y] = 'endworld'
                else:
                    self.world[x, y] = 'stone'

    def checking(self):
        for r in range(2, self.ROWS):
            for c in range(2, self.COLS):
                x = self.TILE_SIZE * (c - 1)
                y = self.TILE_SIZE * (r - 1)
                res = {
                    'center': self.world[(x, y)],
                    'up': self.world[(x, y + self.TILE_SIZE)],
                    'down': self.world[(x, y - self.TILE_SIZE)],
                    'left': self.world[(x - self.TILE_SIZE, y)],
                    'right': self.world[(x + self.TILE_SIZE, y)]
                }
                if res['center'] != res['up'] and res['center'] != res['down']:
                    if res['center'] != res['left'] and res['center'] != res['right']:
                        tiles = list(res.values())[1:]
                        while 'endworld' in tiles:
                            tiles.pop(tiles.index('endworld'))
                        self.world[(x, y)] = most_frequent_simple(tiles)

    def create_world(self):
        self.edges()
        self.add_bioms()
        self.add_item('mountains', 0.6, octaves=2, seed_offset=5000)
        self.add_item('water', 0.66, octaves=2, seed_offset=1000)
        self.add_item('copper', 0.63, octaves=3, seed_offset=255)
        self.add_item('coal', 0.652, octaves=2, seed_offset=3100)
        self.add_item('iron', 0.66, octaves=2, seed_offset=2500)
        self.add_item('silver', 0.66, octaves=2, seed_offset=5000)
        self.add_item('lithium', 0.67, octaves=2, seed_offset=3500)
        # self.add_item('titanium', 0.67, octaves=1, seed_offset=4500)
        self.add_item('uranium', 0.69, octaves=4, seed_offset=500)
        self.checking()

    def get_world(self):
        return self.world, self.collisions
