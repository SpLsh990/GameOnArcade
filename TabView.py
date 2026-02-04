import arcade

from CustomButton import CustomButton
from arcade.gui import UIAnchorLayout, UIBoxLayout, UIManager, UILabel
from math import radians, cos, ceil
from classes import *
from baseView import BaseView


class TabView(BaseView):
    def __init__(self, view, window):
        super().__init__(window)

        self.is_radial = True
        self.radial_manager = UIManager()
        self.radial_manager.enable()

        self.is_fabrics = False
        self.fabrics_manager = UIManager()

        self.is_conveyors = False
        self.conveyors_manager = UIManager()

        self.is_electricity = False
        self.electricity_manager = UIManager()

        self.is_drills = False
        self.drills_manager = UIManager()

        self.is_turrets = False
        self.turrets_manager = UIManager()

        self.is_walls = False
        self.walls_manager = UIManager()

        self.is_inventory = False
        self.inventory_manager = UIManager()

        self.inventory_created = False

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

        self.create_radial_buttons()
        self.create_submenus()

    def create_radial_buttons(self):
        center_x = self.width // 2
        center_y = self.height // 2

        buttons = [
            ("FABS", center_x, center_y + 176, self.fabrics_triggered),
            ("CONVS", center_x + int(176 * cos(radians(30))), (self.height + 176) // 2, self.conveyors_triggered),
            ("ELECTR", center_x + int(176 * cos(radians(30))), (self.height - 176) // 2, self.electricity_triggered),
            ("DRILL", center_x, center_y - 176, self.drills_triggered),
            ("TURR", center_x - int(176 * cos(radians(30))), (self.height - 176) // 2, self.turrets_triggered),
            ("WALLS", center_x - int(176 * cos(radians(30))), (self.height + 176) // 2, self.walls_triggered),
            ("INV", center_x, center_y, self.inventory_triggered)
        ]

        for text, x, y, handler in buttons:
            button = CustomButton(100, 100, text, 0.1, 0.1,
                                  self.window.textures['button_n'],
                                  self.window.textures['button_a'],
                                  self.window.textures['button_t'])
            button.center_x, button.center_y = x, y
            self.radial_manager.add(button)

            button.on_click = lambda event, h=handler: h(event)

    def create_submenus(self):
        for category in ['fabrics', 'conveyors', 'electricity', 'drills', 'turrets', 'walls', 'inventory']:
            sprite_list = getattr(self, f"{category}_list")
            sprite_list.append(
                arcade.Sprite(self.textures["menu"], 1.5, self.width // 2, self.height // 2))

        self.create_fabrics_items()
        self.create_inventory_layout()

    def create_fabrics_items(self):
        fabric1 = CustomButton(100, 100, "Smelter", 0.1, 0.1, self.game_view.textures["smelter"])
        fabric1.center_x, fabric1.center_y = self.width // 2 - 150, self.height // 2
        fabric1.on_click = lambda event: self.item_triggered(self.game_view.textures["smelter"], type='smelter')
        self.fabrics_manager.add(fabric1)

        fabric2 = CustomButton(100, 100, 'Концентратор', 0.1, 0.1, self.game_view.textures['concentrator'])
        fabric2.center_x, fabric2.center_y = self.width // 2, self.height // 2
        fabric2.on_click = lambda event: self.item_triggered(self.game_view.textures['concentrator'], type='concentrator')
        self.fabrics_manager.add(fabric2)

        fabric3 = CustomButton(100, 100, 'Press', 0.1, 0.1, self.game_view.textures['press'])
        fabric3.center_x, fabric3.center_y = self.width // 2 + 150, self.height // 2
        fabric3.on_click = lambda event: self.item_triggered(self.game_view.textures['press'], type='press')
        self.fabrics_manager.add(fabric3)

        wall1 = CustomButton(100, 100, 'Copper wall', 0.1, 0.1, self.game_view.textures['copper_wall'])
        wall1.center_x, wall1.center_y = self.width // 2 - 225, self.height // 2
        wall1.on_click = lambda event: self.item_triggered(self.game_view.textures['copper_wall'], type='copper')
        self.walls_manager.add(wall1)

        wall2 = CustomButton(100, 100, 'Iron wall', 0.1, 0.1, self.game_view.textures['iron_wall'])
        wall2.center_x, wall2.center_y = self.width // 2 - 75, self.height // 2
        wall2.on_click = lambda event: self.item_triggered(self.game_view.textures['iron_wall'], type='iron')
        self.walls_manager.add(wall2)

        wall3 = CustomButton(100, 100, 'titanium wall', 0.1, 0.1, self.game_view.textures['titanium_wall'])
        wall3.center_x, wall3.center_y = self.width // 2 + 75, self.height // 2
        wall3.on_click = lambda event: self.item_triggered(self.game_view.textures['titanium_wall'],
                                                           type='titanium')
        self.walls_manager.add(wall3)

        wall4 = CustomButton(100, 100, 'Steel wall', 0.1, 0.1, self.game_view.textures['steel_wall'])
        wall4.center_x, wall4.center_y = self.width // 2 + 225, self.height // 2
        wall4.on_click = lambda event: self.item_triggered(self.game_view.textures['steel_wall'], type='steel')
        self.walls_manager.add(wall4)

        drill1 = CustomButton(100, 100, 'Copper drill', 0.1, 0.1, self.game_view.textures['copper_drill'])
        drill1.center_x, drill1.center_y = self.width // 2 - 150, self.height // 2
        drill1.on_click = lambda event: self.item_triggered(self.game_view.textures['copper_drill'],
                                                            type='copper')
        self.drills_manager.add(drill1)

        drill2 = CustomButton(100, 100, 'Steel drill', 0.1, 0.1, self.game_view.textures['steel_drill'])
        drill2.center_x, drill2.center_y = self.width // 2, self.height // 2
        drill2.on_click = lambda event: self.item_triggered(self.game_view.textures['steel_drill'], type='steel')
        self.drills_manager.add(drill2)

        drill3 = CustomButton(100, 100, 'Lazer drill', 0.1, 0.1, self.game_view.textures['lazer_drill'])
        drill3.center_x, drill3.center_y = self.width // 2 - 150, self.height // 2
        drill3.on_click = lambda event: self.item_triggered(self.game_view.textures['lazer_drill'], type='lazer')
        self.drills_manager.add(drill3)

        conveyor1 = CustomButton(100, 100, 'conveyor', 0.1, 0.1, self.game_view.textures['conveyor'])
        conveyor1.center_x, conveyor1.center_y = self.width // 2 + 150, self.height // 2
        conveyor1.on_click = lambda event: self.item_triggered(self.game_view.textures['conveyor'],
                                                               direction=(1, 0))
        self.conveyors_manager.add(conveyor1)

    def create_inventory_layout(self):
        if self.inventory_created:
            self.update_inventory()
            return

        self.inventory_manager.clear()

        resources = [
            ("coal", "coal_item"),
            ("copper", "copper_item"),
            ("iron", "iron_item"),
            ("lithium", "lithium_item"),
            ("titanium", "titanium_item"),
            ("steel", "steel_plate"),
            ("graphite", "graphite"),
            ("uranium", "uranium_item"),
            ("water", "water_item"),
            ("energy", "energy")
        ]

        main_container = UIAnchorLayout(width=self.width, height=self.height)
        columns_layout = UIBoxLayout(vertical=False, space_between=100)
        resources_per_column = 4
        num_columns = ceil(len(resources) / resources_per_column)

        self.inventory_labels = {}

        for col_index in range(num_columns):
            column_layout = UIBoxLayout(vertical=True, space_between=30)

            start = col_index * resources_per_column
            end = min(start + resources_per_column, len(resources))

            for i in range(start, end):
                resource_name, texture_key = resources[i]

                resource_row, amount_label = self.create_resource_row(resource_name, texture_key)
                column_layout.add(resource_row)

                self.inventory_labels[resource_name] = amount_label

            columns_layout.add(column_layout)

        main_container.add(columns_layout)
        self.inventory_manager.add(main_container)

        self.inventory_created = True

    def create_resource_row(self, resource_name, texture_key):
        row_layout = UIBoxLayout(vertical=False, space_between=20)

        if texture_key in self.game_view.textures:
            icon_button = CustomButton(
                width=50, height=50,
                text="",
                size_letter=0.1, size_space=0.1,
                texture_normal=self.game_view.textures[texture_key]
            )

        resource_amount = self.game_view.data.get('resources', {}).get(resource_name, 0)
        amount_text = f"{resource_amount}"

        amount_label = UILabel(
            text=amount_text,
            width=100,
            height=50,
            font_size=20,
            font_name="Arial",
            text_color=(255, 255, 0),
            align="left"
        )

        row_layout.add(icon_button)
        row_layout.add(amount_label)

        return row_layout, amount_label

    def update_inventory(self):
        if not self.inventory_created or not self.inventory_labels:
            return

        resources_data = self.game_view.data.get('resources', {})

        for resource_name, label in self.inventory_labels.items():
            amount = resources_data.get(resource_name, 0)
            label.text = f"{amount}"

            if amount <= 0:
                label.text_color = (255, 0, 0)
            else:
                label.text_color = (255, 255, 0)

    def on_draw(self):
        self.game_view.on_draw()

        if self.is_radial:
            self.radial_menu_list.draw()
            self.radial_manager.draw()
            self.radial_manager.enable()

        elif self.is_fabrics:
            self.fabrics_list.draw()
            self.fabrics_manager.draw()
            self.fabrics_manager.enable()

        elif self.is_conveyors:
            self.conveyors_list.draw()
            self.conveyors_manager.draw()
            self.conveyors_manager.enable()

        elif self.is_electricity:
            self.electricity_list.draw()
            self.electricity_manager.draw()
            self.electricity_manager.enable()

        elif self.is_drills:
            self.drills_list.draw()
            self.drills_manager.draw()
            self.drills_manager.enable()

        elif self.is_turrets:
            self.turrets_list.draw()
            self.turrets_manager.draw()
            self.turrets_manager.enable()

        elif self.is_walls:
            self.walls_list.draw()
            self.walls_manager.draw()
            self.walls_manager.enable()

        elif self.is_inventory:
            self.inventory_list.draw()
            self.inventory_manager.draw()
            self.inventory_manager.enable()

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
        self.create_inventory_layout()

    def item_triggered(self, texture, **kwargs):
        x, y = self.width // 2, self.height // 2

        if self.is_fabrics:
            self.game_view.building = Factory(texture, x=x, y=y, hp=100, building_type=kwargs['type'],
                                              tile_size=self.game_view.tile_size)
        elif self.is_conveyors:
            self.game_view.building = Conveyor(texture, x=x, y=y, hp=100, direction=kwargs['direction'],
                                               tile_size=self.game_view.tile_size)
        elif self.is_drills:
            self.game_view.building = Drill(texture, x=x, y=y, hp=100, building_type=kwargs['type'],
                                            world=self.game_view.map,
                                            tile_size=self.game_view.tile_size)
        elif self.is_walls:
            self.game_view.building = Wall(texture, x=x, y=y, building_type=kwargs['type'], tile_size=self.game_view.tile_size)

        self.radial_manager.disable()
        self.fabrics_manager.disable()
        self.conveyors_manager.disable()
        self.electricity_manager.disable()
        self.drills_manager.disable()
        self.turrets_manager.disable()
        self.walls_manager.disable()
        self.inventory_manager.disable()

        self.window.show_view(self.game_view)

    def exit_triggered(self):
        self.is_radial = True
        self.is_fabrics = False
        self.is_conveyors = False
        self.is_electricity = False
        self.is_drills = False
        self.is_turrets = False
        self.is_walls = False
        self.is_inventory = False

        self.radial_manager.disable()
        self.fabrics_manager.disable()
        self.conveyors_manager.disable()
        self.electricity_manager.disable()
        self.drills_manager.disable()
        self.turrets_manager.disable()
        self.walls_manager.disable()
        self.inventory_manager.disable()

        self.window.show_view(self.game_view)
