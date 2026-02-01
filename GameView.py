import arcade
from arcade.gui import UIAnchorLayout, UIBoxLayout

from world import World
from random import randint
from baseView import BaseView
from pauseView import PauseView
from TabView import TabView
from CustomButton import CustomButton


class GameView(BaseView):
    def __init__(self, window, rows=150, cols=150, tile_size=10, data=None):
        super().__init__(window)
        self.window = window
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size

        self.data = data

        self.textures = {}
        self.load_textures()

        self.worldList = arcade.SpriteList()

        self.create_GUI()

        self.pause = False

        self.data['seed'] = data['seed'] if data['seed'] else randint(1, 100000000)
        self.world = World(self.data['seed'], self.rows, self.cols, self.tile_size)
        self.world.create_world()
        self.map, self.mountains, self.water = self.world.get_world()
        self.collisions = arcade.SpriteList()

        self.camera = arcade.camera.Camera2D()
        self.camera_pos = [self.cols // 2 * self.tile_size, self.rows // 2 * self.tile_size]
        self.camera_zoom = 3.0

        self.load_world()
        self.dash = {}
        self.tab_view = TabView(self, self.window)

        self.building = None
        self.buildingList = arcade.SpriteList()
        # self.phys_engine = arcade.PhysicsEngineSimple(self.data['entity'], self.collisions)

    def load_textures(self):
        self.textures["coal"] = arcade.load_texture("sprites/world/coal.png")
        self.textures["copper"] = arcade.load_texture("sprites/world/copper.png")
        self.textures["endworld"] = arcade.load_texture("sprites/world/endworld.png")
        self.textures["iron"] = arcade.load_texture("sprites/world/iron.png")
        self.textures["lithium"] = arcade.load_texture("sprites/world/lithium.png")
        self.textures["mountains"] = arcade.load_texture("sprites/world/mountain.png")
        self.textures["stone"] = arcade.load_texture("sprites/world/stone.png")
        self.textures["uranium"] = arcade.load_texture("sprites/world/uranium.png")
        self.textures["water"] = arcade.load_texture("sprites/world/water.png")
        self.textures["titanium"] = arcade.load_texture("sprites/world/titanium.png")
        self.textures["coal_item"] = arcade.load_texture("sprites/icons/coal_icon.png")
        self.textures["copper_item"] = arcade.load_texture("sprites/icons/copper_icon.png")
        self.textures["iron_item"] = arcade.load_texture("sprites/icons/iron_icon.png")
        self.textures["lithium_item"] = arcade.load_texture("sprites/icons/lithium_icon.png")
        self.textures["titanium_item"] = arcade.load_texture("sprites/icons/titanium_icon.png")
        self.textures["uranium_item"] = arcade.load_texture("sprites/icons/uranium_icon.png")
        self.textures["water_item"] = arcade.load_texture("sprites/icons/water_icon.png")
        self.textures["energy"] = arcade.load_texture("sprites/icons/energy_icon.png")

    def load_world(self):
        for (x, y), item in self.map.items():
            tile = arcade.Sprite(self.textures[item], 1 / 160 * self.tile_size, x + self.tile_size // 2,
                                 y + self.tile_size // 2)
            if item == "mountains" or item == "water":
                self.collisions.append(tile)
            else:
                self.worldList.append(tile)

    def create_GUI(self):
        self.cv_anchor = UIAnchorLayout()
        self.cv_anchor.default_anchor_y = "top"
        self.cv_layout = UIBoxLayout(vertical=False, space_between=10)
        self.wave_label = CustomButton(self.width * 0.15, self.height * 0.075, f"WAVE - {self.data.get('wave', 0)}",
                                       size_letter=self.width * 0.00019, size_space=self.width * 0.00019,
                                       texture_normal=self.window.textures['button_n'], change_text=False)
        self.button_skip = CustomButton(self.width * 0.045, self.height * 0.075,
                                        texture_normal=self.window.textures['skip_n'],
                                        texture_active=self.window.textures['skip_a'],
                                        texture_triggered=self.window.textures['skip_t'])

        self.cv_layout.add(self.wave_label)
        self.cv_layout.add(self.button_skip)
        self.cv_anchor.add(self.cv_layout)
        self.manager.add(self.cv_anchor)

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.worldList.draw()
            self.collisions.draw()
            if self.building:
                self.buildingList.draw()
            for spriteList in self.data['obj'].values():
                spriteList.draw()
        super().on_draw()

    def on_update(self, dt):
        if self.pause:
            return
        if self.building and self.building not in self.buildingList:
            self.buildingList.append(self.building)
        if self.building:
            if self.building.collides_with_list(self.collisions):
                self.building.color = (255, 0, 0, 150)
            else:
                self.building.color = (0, 255, 0, 150)
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
        self.check_camera()
        self.camera.position = self.camera_pos
        self.camera.zoom = self.camera_zoom
        # self.phys_engine.update()

    def log_obj(self, obj_type):
        # TODO Сделать инициализацию логики для пуль
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
                self.buildingList.remove(self.building)
                self.building = None
                return
            self.pause = True
            if self.pause:
                self.window.show_view(self.window.pause_view)
        elif key == arcade.key.TAB:
            self.window.show_view(self.tab_view)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.building:
            wx, wy = self.bind_coords(*self.screen_to_world(x, y))
            self.building.center_x = wx
            self.building.center_y = wy

    def on_mouse_press(self, x, y, button, modifiers):
        pass

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

    def screen_to_world(self, screen_x, screen_y):
        world_x = self.camera.x + (screen_x - self.camera.viewport_width / 2) / self.camera.zoom
        world_y = self.camera.y + (screen_y - self.camera.viewport_height / 2) / self.camera.zoom
        return world_x, world_y

    def bind_coords(self, x, y):
        bind_x = x - x % self.tile_size + self.tile_size // 2
        bind_y = y - y % self.tile_size + self.tile_size // 2
        return bind_x, bind_y
