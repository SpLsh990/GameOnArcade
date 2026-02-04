from SeedNoiseGenerator import SeedNoiseGenerator


def most_frequent_simple(lst):
    counts = {}
    for item in lst:
        counts[item] = counts.get(item, 0) + 1
    max_item = max(counts, key=counts.get)
    return max_item


class World:
    def __init__(self, seed, rows, cols, tile_size):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.generator = SeedNoiseGenerator(seed)
        self.world = {}

    def add_item(self, item, limit, octaves=4, seed_offset=0, persistence=0.5,
                 lacunarity=2.0, scale=0.01):
        for r in range(2, self.rows):
            for c in range(2, self.cols):
                x = self.tile_size * (c - 1)
                y = self.tile_size * (r - 1)
                value = self.generator.noise(x, y, octaves, seed_offset,
                                             persistence, lacunarity, scale)
                if value > limit and self.world[(x, y)] == 'stone':
                    self.world[(x, y)] = item

    def add_bioms(self):
        for r in range(1, self.rows + 1):
            for c in range(1, self.cols + 1):
                x = self.tile_size * (c - 1)
                y = self.tile_size * (r - 1)
                if r == 1 or r == self.rows or c == 1 or c == self.cols:
                    self.world[(x, y)] = 'endworld'
                else:
                    self.world[(x, y)] = 'stone'

    def checking(self):
        for r in range(2, self.rows):
            for c in range(2, self.cols):
                x = self.tile_size * (c - 1)
                y = self.tile_size * (r - 1)

                res = {
                    'center': self.world[(x, y)],
                    'up': self.world[(x, y + self.tile_size)],
                    'down': self.world[(x, y - self.tile_size)],
                    'left': self.world[(x - self.tile_size, y)],
                    'right': self.world[(x + self.tile_size, y)]
                }

                if (res['center'] != res['up'] and res['center'] != res['down'] and
                        res['center'] != res['left'] and res['center'] != res['right']):

                    tiles = list(res.values())[1:]
                    while 'endworld' in tiles:
                        tiles.pop(tiles.index('endworld'))

                    self.world[(x, y)] = most_frequent_simple(tiles)

    def clear_area(self, center_x, center_y, radius):
        start_x = max(center_x - (radius // 2), 2)
        end_x = min(center_x + (radius // 2) + 1, self.cols * self.tile_size - 2)
        start_y = max(center_y - (radius // 2), 2)
        end_y = min(center_y + (radius // 2) + 1, self.rows * self.tile_size - 2)
        for y in range(start_y, end_y, self.tile_size):
            for x in range(start_x, end_x, self.tile_size):
                self.world[(x, y)] = "stone"

    def create_world(self):
        self.add_bioms()
        self.add_item('mountains', 0.6, octaves=2, seed_offset=5000)
        self.add_item('water', 0.66, octaves=2, seed_offset=1000)
        self.add_item('copper', 0.64, octaves=3, seed_offset=255)
        self.add_item('coal', 0.652, octaves=3, seed_offset=3100)
        self.add_item('iron', 0.66, octaves=4, seed_offset=2500)
        self.add_item('lithium', 0.67, octaves=4, seed_offset=3500)
        self.add_item('titanium', 0.67, octaves=4, seed_offset=4500)
        self.add_item('uranium', 0.69, octaves=4, seed_offset=500)
        self.checking()
        self.clear_area(100, 100, 10 * self.tile_size)
        self.clear_area((self.cols - 15) * self.tile_size, (self.rows - 15) * self.tile_size, 10 * self.tile_size)

    def get_world(self):
        return self.world
