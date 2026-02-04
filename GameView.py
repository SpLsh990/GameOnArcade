from arcade.gui import UIAnchorLayout, UIBoxLayout
import threading
import json
import threading
from datetime import date
from random import randint

from arcade.gui import UIAnchorLayout, UIBoxLayout

from CustomButton import CustomButton
from TabView import TabView
from baseView import BaseView
from classes import *
from world import World


class GameView(BaseView):
    def __init__(self, window, rows=150, cols=150, tile_size=10, data=None):
        super().__init__(window)

        self.window = window
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size

        self.data = data or {}
        self.data['seed'] = data.get('seed', None) if data.get('seed', None) else randint(1, 100000000)

        self.textures = {}
        self.dash = {}
        self.world_list = arcade.SpriteList()
        self.collisions = arcade.SpriteList()

        self.entity_list = arcade.SpriteList()

        self.wave = self.data.get('wave', 0)
        self.pause = False
        self.spawn_point = (10 * tile_size, 10 * tile_size)

        self.load_textures()
        self.initialize_data_structure()
        self.create_gui()

        self.world = World(self.data['seed'], self.rows, self.cols, self.tile_size)
        self.world.create_world()
        self.map = self.world.get_world()

        self.camera = arcade.camera.Camera2D()
        self.camera_pos = [self.cols // 2 * self.tile_size, self.rows // 2 * self.tile_size]
        self.camera_zoom = 3.0

        self.load_world()
        self.tab_view = TabView(self, self.window)

        self.building = None
        self.building_list = arcade.SpriteList()

    def initialize_data_structure(self):
        if 'obj' not in self.data:
            self.data['obj'] = {}

            object_types = ['Base', 'Factory', 'Drill', 'Conveyor', 'Wall', 'Turret']
            for obj_type in object_types:
                if obj_type not in self.data['obj']:
                    self.data['obj'][obj_type] = arcade.SpriteList()
            self.data['obj']['Base'].append(Base(self.textures['core'], 95, 95, 100, self.tile_size))
            for i in range(3):
                for j in range(3):
                    self.dash[(80 + self.tile_size * i, 80 + self.tile_size * j)] = self.data['obj']['Base'][0]

            if 'resources' not in self.data:
                self.data['resources'] = {
                    'coal': 0, 'copper': 0, 'iron': 0, 'lithium': 0,
                    'titanium': 0, 'uranium': 0, 'water': 0, 'energy': 0, 'graphite': 0, 'steel_plate': 0
                }
            self.data['obj']['Base'][0].storage = self.data['resources']
        else:
            for group in self.data['obj']:
                data = self.data['obj'][group]
                self.data['obj'][group] = arcade.SpriteList()

                for obj in data:
                    if group == "Factory":
                        self.data['obj'][group].append(
                            Factory(self.textures[obj[3]], obj[0], obj[1], obj[2], obj[3], self.tile_size))
                    elif group == "Drill":
                        self.data['obj'][group].append(
                            Drill(self.textures[f"{obj[3]}_drill"], obj[0], obj[1], obj[2], self.map, self.tile_size))
                    elif group == "Wall":
                        self.data['obj'][group].append(
                            Wall(self.textures[f"{obj[2]}_wall"], obj[0], obj[1], obj[2], self.tile_size))
                    elif group == "Conveyor":
                        self.data["obj"][group].append(
                            Conveyor(self.textures["conveyor"], obj[0], obj[1], obj[2], obj[3], self.tile_size))
                    elif group == "Base":
                        self.data["obj"][group].append(
                            Base(self.textures['core'], obj[0], obj[1], obj[2], self.tile_size))

    def load_textures(self):
        world_textures = {
            "coal": arcade.load_texture("sprites/world/coal.png"),
            "copper": arcade.load_texture("sprites/world/copper.png"),
            "endworld": arcade.load_texture("sprites/world/endworld.png"),
            "iron": arcade.load_texture("sprites/world/iron.png"),
            "lithium": arcade.load_texture("sprites/world/lithium.png"),
            "mountains": arcade.load_texture("sprites/world/mountain.png"),
            "stone": arcade.load_texture("sprites/world/stone.png"),
            "uranium": arcade.load_texture("sprites/world/uranium.png"),
            "water": arcade.load_texture("sprites/world/water.png"),
            "titanium": arcade.load_texture("sprites/world/titanium.png")
        }

        item_textures = {
            "coal_item": arcade.load_texture("sprites/icons/coal_icon.png"),
            "copper_item": arcade.load_texture("sprites/icons/copper_icon.png"),
            "iron_item": arcade.load_texture("sprites/icons/iron_icon.png"),
            "lithium_item": arcade.load_texture("sprites/icons/lithium_icon.png"),
            "titanium_item": arcade.load_texture("sprites/icons/titanium_icon.png"),
            "uranium_item": arcade.load_texture("sprites/icons/uranium_icon.png"),
            "water_item": arcade.load_texture("sprites/icons/water_icon.png"),
            "energy": arcade.load_texture("sprites/icons/energy_icon.png"),
            "steel_plate": arcade.load_texture("sprites/icons/steel_plate.png"),
            "graphite": arcade.load_texture("sprites/icons/graphite_plate.png")
        }

        building_textures = {
            "conveyor": arcade.load_texture("sprites/buildings/conveyor.png"),
            "copper_drill": arcade.load_texture("sprites/buildings/copper_drill.png"),
            "steel_drill": arcade.load_texture("sprites/buildings/steel_drill.png"),
            "lazer_drill": arcade.load_texture("sprites/buildings/lazer_drill.png"),
            "copper_wall": arcade.load_texture("sprites/buildings/copper_wall.png"),
            "steel_wall": arcade.load_texture("sprites/buildings/steel_drill.png"),
            "titanium_wall": arcade.load_texture("sprites/buildings/titanium_wall.png"),
            "iron_wall": arcade.load_texture("sprites/buildings/iron_wall.png"),
            "core": arcade.load_texture("sprites/buildings/core.png"),
            "smelter": arcade.load_texture("sprites/buildings/smelter.png"),
            "concentrator": arcade.load_texture("sprites/buildings/concentrator.png"),
            "press": arcade.load_texture("sprites/buildings/press.png"),
            "core": arcade.load_texture("sprites/buildings/core.png")
        }
        self.textures = {**world_textures, **item_textures, **building_textures}

    def load_world(self):
        for (x, y), item in self.map.items():
            texture = self.textures.get(item, self.textures["stone"])
            tile = arcade.Sprite(
                texture,
                1 / 160 * self.tile_size,
                x + self.tile_size // 2,
                y + self.tile_size // 2
            )

            if item == "mountains" or item == "water" or item == "endworld":
                self.collisions.append(tile)
            else:
                self.world_list.append(tile)

    def create_gui(self):
        self.cv_anchor = UIAnchorLayout()
        self.cv_anchor.default_anchor_y = "top"
        self.cv_layout = UIBoxLayout(vertical=False, space_between=10)

        self.wave_label = CustomButton(
            self.width * 0.15, self.height * 0.075,
            f"WAVE - {self.wave}",
            size_letter=self.width * 0.00019,
            size_space=self.width * 0.00019,
            texture_normal=self.window.textures['button_n'],
            change_text=False
        )

        self.button_skip = CustomButton(
            self.width * 0.045, self.height * 0.075,
            texture_normal=self.window.textures['skip_n'],
            texture_active=self.window.textures['skip_a'],
            texture_triggered=self.window.textures['skip_t']
        )

        self.cv_layout.add(self.wave_label)
        self.cv_layout.add(self.button_skip)
        self.cv_anchor.add(self.cv_layout)
        self.manager.add(self.cv_anchor)

        self.button_skip.on_click = lambda event: self.start_wave()

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.world_list.draw()
            self.collisions.draw()

            if self.building:
                self.building_list.draw()

            if self.data.get('obj'):
                for sprite_list in self.data['obj'].values():
                    sprite_list.draw()

            # Draw enemies
            self.entity_list.draw()

        super().on_draw()

    def on_update(self, dt=1/60):
        if self.pause:
            return

        if self.building and not self.building in self.building_list:
            self.building_list = arcade.SpriteList()
            self.building_list.append(self.building)

        thread1 = threading.Thread(target=self.build_collide())
        thread2 = threading.Thread(target=self.check_camera())
        thread1.start()
        thread2.start()
        self.update_game_objects(dt)

        self.wave_label.load_text(f"WAVE - {self.wave}")
        thread1.join()
        thread2.join()

    def build_collide(self):
        if self.building:
            if not self.building.collides_with_list(self.collisions):
                for i in self.data['obj'].values():
                    if self.building.collides_with_list(i):
                        self.building.color = (255, 0, 0, 150)
                        break
                else:
                    self.building.color = (0, 255, 0, 150)
            else:
                self.building.color = (255, 0, 0, 150)

    def update_game_objects(self, dt):
        # Update "Conveyor", "Drill", "Factory"
        threads = []
        for i in ["Conveyor", "Drill", "Factory"]:
            t = threading.Thread(target=self.log_obj(i))
            threads.append(t)
            t.start()
            t.join()

        for key, value in self.data["resources"].items():
            self.data["resources"][key] = self.data['obj']['Base'][0].storage.get(key, 0)

        for turret in self.data['obj']['Turret']:
            if self.entity_list:
                nearest_enemy = min(
                    self.entity_list,
                    key=lambda e: ((e.center_x - turret.center_x) ** 2 + (e.center_y - turret.center_y) ** 2) ** 0.5
                )
                distance = ((nearest_enemy.center_x - turret.center_x) ** 2 +
                            (nearest_enemy.center_y - turret.center_y) ** 2) ** 0.5

                if distance < 100:
                    nearest_enemy.hp -= 10 * dt
                    if nearest_enemy.hp <= 0:
                        nearest_enemy.remove_from_sprite_lists()

    def log_obj(self, obj_type):
        for obj in self.data['obj'][obj_type]:
            if obj.hp <= 0:
                obj.remove_from_sprite_lists()
                self.dash.remove(obj)
            else:
                obj.logic(self.dash, self.tile_size)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == arcade.MOUSE_BUTTON_RIGHT:
            self.camera_pos[0] -= dx / self.camera_zoom
            self.camera_pos[1] -= dy / self.camera_zoom

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        zoom_factor = 1.1
        if scroll_y > 0:
            if self.camera_zoom * zoom_factor < 4.0:
                self.camera_zoom *= zoom_factor
        elif scroll_y < 0:
            if self.camera_zoom / zoom_factor > 1.5:
                self.camera_zoom /= zoom_factor

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if self.building:
                self.building_list = arcade.SpriteList()
                self.building = None
                return

            self.pause = True
            if self.pause:
                self.window.show_view(self.window.pause_view)

        elif key == arcade.key.TAB:
            print(self.data['obj']['Base'][0].storage)
            self.tab_view.exit_triggered()
            self.building_list = arcade.SpriteList()
            self.building = None
            self.window.show_view(self.tab_view)

        elif key == arcade.key.SPACE:
            self.start_wave()

        elif key == arcade.key.R:
            if isinstance(self.building, Conveyor):
                l = [(1, 0), (0, -1), (-1, 0), (0, 1)]
                self.building.direction = l[(l.index(self.building.direction) + 1) % 4]
                self.building.angle += 90

    def on_mouse_motion(self, x, y, dx, dy):
        if self.building:
            wx, wy = self.bind_coords(*self.screen_to_world(x, y), self.building.multiplier)
            self.building.center_x = wx
            self.building.center_y = wy

    def on_mouse_press(self, x, y, button, modifiers):
        if self.building and button == arcade.MOUSE_BUTTON_LEFT:
            if not self.building.collides_with_list(self.collisions):
                for i in self.data['obj'].values():
                    if self.building.collides_with_list(i):
                        return
                building_type = self.building.__class__.__name__
                if building_type in self.data['obj']:
                    self.building.color = (255, 255, 255, 255)
                    wx, wy = self.bind_coords(*self.screen_to_world(x, y), self.building.multiplier)
                    self.building.x = wx - self.tile_size // 2 if self.building.multiplier % 2 == 1 else wx - self.tile_size
                    self.building.y = wy - self.tile_size // 2 if self.building.multiplier % 2 == 1 else wy - self.tile_size
                    print(self.building.x, self.building.y, wx, wy)
                    if isinstance(self.building, Drill):
                        self.building.setup()
                    self.data['obj'][building_type].append(self.building)
                    for i in range(self.building.multiplier):
                        for j in range(self.building.multiplier):
                            self.dash[(self.building.x + self.tile_size * i, self.building.y + self.tile_size * j)] = self.building
                    if isinstance(self.building, Conveyor):
                        self.tab_view.item_triggered(texture=self.building.texture, direction=self.building.direction)
                    else:
                        self.tab_view.item_triggered(texture=self.building.texture, type=self.building.building_type)

    def check_camera(self):
        zoom = self.camera.zoom
        half_viewport_width = (self.width / 2) / zoom
        half_viewport_height = (self.height / 2) / zoom

        min_x = half_viewport_width
        max_x = (self.cols * self.tile_size) - half_viewport_width
        min_y = half_viewport_height
        max_y = (self.rows * self.tile_size) - half_viewport_height

        self.camera_pos[0] = max(min_x, min(self.camera_pos[0], max_x))
        self.camera_pos[1] = max(min_y, min(self.camera_pos[1], max_y))

        self.camera.position = self.camera_pos
        self.camera.zoom = self.camera_zoom

    def screen_to_world(self, screen_x, screen_y):
        world_x = self.camera.position[0] + (screen_x - self.camera.viewport_width / 2) / self.camera.zoom
        world_y = self.camera.position[1] + (screen_y - self.camera.viewport_height / 2) / self.camera.zoom
        return world_x, world_y

    def bind_coords(self, x, y, multiplier=1):
        normalization = self.tile_size // 2 if multiplier % 2 == 1 else 0
        bind_x = x - x % self.tile_size + normalization
        bind_y = y - y % self.tile_size + normalization
        return bind_x, bind_y

    def save(self):
        self.data['date'] = str(date.today())
        savedata = self.data.copy()
        savedata["obj"] = {}
        for group in ["Base", "Factory", "Drill", "Conveyor", "Wall", "Turret"]:
            savedata["obj"][group] = []
        with open(f"saves/{self.data.get('name')}.json", "w", encoding="utf-8") as js:
            for group in self.data['obj'].keys():
                for obj in self.data['obj'][group]:
                    if group == "Factory" or group == "Drill":
                        savedata['obj'][group].append((obj.center_x, obj.center_y, obj.hp, obj.building_type))
                    elif group == "Wall":
                        savedata['obj'][group].append((obj.center_x, obj.center_y, obj.building_type))
                    elif group == "Base":
                        savedata['obj'][group].append((obj.center_x, obj.center_y, obj.hp))
                    elif group == "Conveyor":
                        savedata['obj'][group].append((obj.center_x, obj.center_y, obj.hp, obj.direction))

            json.dump(savedata, js, indent=4, ensure_ascii=False)
