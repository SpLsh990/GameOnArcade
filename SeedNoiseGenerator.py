from noise import pnoise2, snoise2
from math import pi, e


class SeedNoiseGenerator:
    def __init__(self, seed):
        self.seed = seed

    def noise(self, x, y, octaves=4, seed_offset=0, persistence=0.5, lacunarity=2.0, scale=0.01):
        value = 0
        frequency = scale
        amplitude = 1.0
        max_value = 0
        offset_x = ((self.seed + seed_offset) * 12453) % 65536
        offset_y = ((self.seed + seed_offset) * 78901) % 65536
        for i in range(octaves):
            nx = x * frequency + offset_x + i * 100 * e
            ny = y * frequency + offset_y + i * 200 * pi

            value += pnoise2(nx, ny) * amplitude
            max_value += amplitude

            frequency *= lacunarity
            amplitude *= persistence

        if max_value > 0:
            value = (value / max_value + 1) / 2

        return value

    def get_seed(self):
        return self.seed


# Тестирование
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    width, height = 2 ** 9, 2 ** 9
    noise_map = np.zeros((height, width))

    gen = SeedNoiseGenerator(1001)
    for x in range(width):
        for y in range(height):
            value = gen.noise(x, y, octaves=1, seed_offset=1200)
            noise_map[x, y] = value

    plt.imshow(noise_map, cmap='gray')
    plt.show()
