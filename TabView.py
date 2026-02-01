import arcade
from CustomButton import CustomButton
from arcade.gui import UIAnchorLayout, UIBoxLayout, UIManager
from math import radians, cos

from baseView import BaseView


class TabView(BaseView):
    def __init__(self, view, window):
        super().__init__(window)
        self.is_radial = True
        self.radial_manager = UIManager()
        self.radial_manager.enable()
        self.is_fabrics = False
        self.fabrics_manager = UIManager()
        self.fabrics_manager.enable()
        self.is_conveyors = False
        self.conveyors_manager = UIManager()
        self.conveyors_manager.enable()
        self.is_electricity = False
        self.electricity_manager = UIManager()
        self.electricity_manager.enable()
        self.is_drills = False
        self.drills_manager = UIManager()
        self.drills_manager.enable()
        self.is_turrets = False
        self.turrets_manager = UIManager()
        self.turrets_manager.enable()
        self.is_walls = False
        self.walls_manager = UIManager()
        self.walls_manager.enable()
        self.is_inventory = False
        self.inventory_manager = UIManager()
        self.inventory_manager.enable()

        self.game_view = view
        self.textures = {}
        self.load_textures()
        self.create_widget()

    def load_textures(self):
        self.textures["radial_menu"] = arcade.load_texture("sprites/tab/radial_menu.png")
        self.textures["menu"] = arcade.load_texture("sprites/tab/menu.png")

    def create_widget(self):
        self.radial_menu_list = arcade.SpriteList()
        self.fabrics_list = arcade.SpriteList()
        self.conveyors_list = arcade.SpriteList()
        self.electricity_list = arcade.SpriteList()
        self.drills_list = arcade.SpriteList()
        self.walls_list = arcade.SpriteList()
        self.turrets_list = arcade.SpriteList()
        self.inventory_list = arcade.SpriteList()

        self.radial_menu_list.append(
            arcade.Sprite(self.textures["radial_menu"], 1, self.width // 2, self.height // 2))
        fabrics = CustomButton(100, 100, "FABS", 0.1, 0.1, self.window.textures['button_n'],
                               self.window.textures['button_a'], self.window.textures['button_t'])
        fabrics.center_x, fabrics.center_y = self.width // 2, self.height // 2 + 176

        conveyors = CustomButton(100, 100, "CONVS", 0.1, 0.1, self.window.textures['button_n'],
                                 self.window.textures['button_a'], self.window.textures['button_t'])
        conveyors.center_x, conveyors.center_y = self.width // 2 + int(176 * cos(radians(30))), (self.height + 176) // 2

        electricity = CustomButton(100, 100, "ELECTR", 0.1, 0.1, self.window.textures['button_n'],
                                   self.window.textures['button_a'], self.window.textures['button_t'])
        electricity.center_x, electricity.center_y = self.width // 2 + int(176 * cos(radians(30))), (
                self.height - 176) // 2

        drills = CustomButton(100, 100, "DRILL", 0.1, 0.1, self.window.textures['button_n'],
                              self.window.textures['button_a'], self.window.textures['button_t'])
        drills.center_x, drills.center_y = self.width // 2, self.height // 2 - 176

        turrets = CustomButton(100, 100, "TURR", 0.1, 0.1, self.window.textures['button_n'],
                               self.window.textures['button_a'], self.window.textures['button_t'])
        turrets.center_x, turrets.center_y = self.width // 2 - int(176 * cos(radians(30))), (self.height - 176) // 2

        walls = CustomButton(100, 100, "WALLS", 0.1, 0.1, self.window.textures['button_n'],
                             self.window.textures['button_a'], self.window.textures['button_t'])
        walls.center_x, walls.center_y = self.width // 2 - int(176 * cos(radians(30))), (self.height + 176) // 2

        inventory = CustomButton(100, 100, "INV", 0.1, 0.1, self.window.textures['button_n'],
                                 self.window.textures['button_a'], self.window.textures['button_t'])
        inventory.center_x, inventory.center_y = self.width // 2, self.height // 2

        self.radial_manager.add(fabrics)
        self.radial_manager.add(conveyors)
        self.radial_manager.add(electricity)
        self.radial_manager.add(drills)
        self.radial_manager.add(turrets)
        self.radial_manager.add(walls)
        self.radial_manager.add(inventory)

        fabrics.on_click = lambda event: self.fabrics_triggered(event)
        conveyors.on_click = lambda event: self.conveyors_triggered(event)
        electricity.on_click = lambda event: self.electricity_triggered(event)
        drills.on_click = lambda event: self.drills_triggered(event)
        turrets.on_click = lambda event: self.turrets_triggered(event)
        walls.on_click = lambda event: self.walls_triggered(event)
        inventory.on_click = lambda event: self.inventory_triggered(event)

        self.fabrics_list.append(
            arcade.Sprite(self.textures["menu"], 1.5, self.width // 2, self.height // 2))
        fabric1 = CustomButton(100, 100, "FAB1", 0.1, 0.1, self.game_view.textures["iron"])
        fabric1.center_x, fabric1.center_y = self.width // 2, self.height // 2
        self.fabrics_manager.add(fabric1)
        self.conveyors_list.append(
            arcade.Sprite(self.textures["menu"], 1.5, self.width // 2, self.height // 2))
        self.electricity_list.append(
            arcade.Sprite(self.textures["menu"], 1.5, self.width // 2, self.height // 2))
        self.drills_list.append(
            arcade.Sprite(self.textures["menu"], 1.5, self.width // 2, self.height // 2))
        self.walls_list.append(
            arcade.Sprite(self.textures["menu"], 1.5, self.width // 2, self.height // 2))
        self.turrets_list.append(
            arcade.Sprite(self.textures["menu"], 1.5, self.width // 2, self.height // 2))
        self.inventory_list.append(
            arcade.Sprite(self.textures["menu"], 1.5, self.width // 2, self.height // 2))
        # Сюда надо будет добавить спрайты построек
        fabric1.on_click = lambda event: self.item_triggered(event, fabric1.texture_normal)

    def on_draw(self):
        self.game_view.on_draw()
        if self.is_radial:
            self.radial_menu_list.draw()
            self.radial_manager.draw()
        elif self.is_fabrics:
            self.fabrics_list.draw()
            self.fabrics_manager.draw()
        elif self.is_conveyors:
            self.conveyors_list.draw()
            self.conveyors_manager.draw()
        elif self.is_electricity:
            self.electricity_list.draw()
            self.electricity_manager.draw()
        elif self.is_drills:
            self.drills_list.draw()
            self.drills_manager.draw()
        elif self.is_turrets:
            self.turrets_list.draw()
            self.turrets_manager.draw()
        elif self.is_walls:
            self.walls_list.draw()
            self.walls_manager.draw()
        elif self.is_inventory:
            self.inventory_list.draw()
            self.inventory_manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.TAB:
            self.exit_triggered()
        elif key == arcade.key.KEY_1:
            self.fabrics_triggered(True)
        elif key == arcade.key.KEY_2:
            self.conveyors_triggered(True)
        elif key == arcade.key.KEY_3:
            self.electricity_triggered(True)
        elif key == arcade.key.KEY_4:
            self.drills_triggered(True)
        elif key == arcade.key.KEY_5:
            self.turrets_triggered(True)
        elif key == arcade.key.KEY_6:
            self.walls_triggered(True)
        elif key == arcade.key.KEY_7:
            self.inventory_triggered(True)

    def fabrics_triggered(self, event):
        self.is_fabrics = True
        self.is_radial = False

    def conveyors_triggered(self, event):
        self.is_conveyors = True
        self.is_radial = False

    def electricity_triggered(self, event):
        self.is_electricity = True
        self.is_radial = False

    def drills_triggered(self, event):
        self.is_drills = True
        self.is_radial = False

    def turrets_triggered(self, event):
        self.is_turrets = True
        self.is_radial = False

    def walls_triggered(self, event):
        self.is_walls = True
        self.is_radial = False

    def inventory_triggered(self, event):
        self.is_inventory = True
        self.is_radial = False

    def item_triggered(self, event, texture):
        x, y = self.width // 2, self.height // 2
        self.game_view.building = arcade.Sprite(texture, 1/160 * self.game_view.tile_size, x, y)
        self.exit_triggered()

    def exit_triggered(self):
        self.is_radial = True
        self.is_fabrics = False
        self.is_conveyors = False
        self.is_electricity = False
        self.is_drills = False
        self.is_turrets = False
        self.is_walls = False
        self.is_inventory = False
        self.window.show_view(self.game_view)
