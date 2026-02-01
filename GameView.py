import threading
from random import randint
import arcade
from baseView import BaseView
from classes import *
from world import World


class GameView(BaseView):
    def __init__(self, window, rows=100, cols=100, tile_size=10, data=None):
        super().__init__(window)
        self.window = window
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size

        self.data = data
        self.sprites = {
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
        self.spriteList = arcade.SpriteList()

        self.pause = False

        self.data['seed'] = data['seed'] if data['seed'] else randint(1, 100000000)
        self.data['obj'] = {"Base": [Base()]} #TODO x, y, hp базы игрока

        self.world = World(self.data['seed'], self.rows, self.cols, self.tile_size)
        self.world.create_world()

        self.map, self.collisions = self.world.get_world()

        self.camera = arcade.camera.Camera2D()
        self.camera_pos = [self.cols // 2 * self.tile_size, self.rows // 2 * self.tile_size]
        self.camera_zoom = 3.0

        for (x, y), item in self.map.items():
            tile = arcade.Sprite(self.sprites[item], 1 / 160 * self.tile_size, x + self.tile_size // 2,
                                 y + self.tile_size // 2)
            self.spriteList.append(tile)

        # self.phys_engine = arcade.PhysicsEngineSimple(self.data['entity'], self.collisions)

    def on_draw(self, delta_time=30):
        self.clear()
        with self.camera.activate():
            self.spriteList.draw()
            for spriteList in self.data['obj'].values():
                spriteList.draw()

    def on_update(self, delta_time=30):
        if self.pause:
            return
        self.check_camera()
        self.camera.position = self.camera_pos
        self.camera.zoom = self.camera_zoom
        """thread1 = threading.Thread(target=self.log_ent(), args=())
        thread2 = threading.Thread(target=self.log_obj(), args=("Drill"))
        thread3 = threading.Thread(target=self.log_obj(), args=("Factory"))
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()"""
        for i in ["Conveyor", "Drill", "Factory"]:
            t = threading.Thread(target=self.log_obj(), args=(i))
            threads.append(t)
            t.start()
            t.join()



        # self.phys_engine.update()
    def log_obj(self, obj_type):
        #TODO Сделать инициализацию логики для пуль
        """if obj_type == "Bullet":
            for obj in self.data['obj'][obj_type]:
                for spriteList in []
                if arcade.check_for_collision_with_list(obj, self.spriteList):"""
        for obj in self.data['obj'][obj_type]:
            if obj.gp <= 0:
                obj.remove_from_sprite_lists()
                self.entity.remove(ent)
            else:
                obj.logic(self.tile_size, path)

    """def log_ent(self, delta_time=30):
        for x in range(self.cols):
            for y in range(self.rows):
                grid[x * self.tile_size, y * self.tile_size] = 1
        for i in self.collisions():
            grid[i] = 0
        for i in self.world[obj].items():
            for (x, y), item in i.items():
                if isinstance(item, Wall):
                    grid[(x, y)] = 5
                elif not isinstance(item, Conveyor):
                    grid[(x, y)] = 2
        astra = AStar2D(grid)
        path = astra.find_path(self.spawn, (self.data['obj']['Base'].x, self.data['obj']['Base'].y))
        for ent in self.entity:
            if ent.gp <= 0:
                ent.remove_from_sprite_lists()
                self.entity.remove(ent)
            else:
                ent.logic(self.tile_size, path)"""

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == arcade.MOUSE_BUTTON_LEFT:
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
            self.pause = True
            if self.pause:
                self.window.show_view(self.window.pause_view)

    # Ограничение камеры в пределах игрового мира
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
