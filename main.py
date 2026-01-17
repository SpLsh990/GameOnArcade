import arcade
from SeedNoiseGenerator import SeedNoiseGenerator
from GameView import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Миллион оттенков серого и синего"

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = Game()
    window.show_view(menu_view)
    arcade.run()