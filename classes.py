import heapq
import math
import arcade
import time


class BaseObject(arcade.Sprite):
    def __init__(self, sprite, x, y, hp, scale):
        super().__init__(sprite, center_x=x, center_y=y, scale=scale)
        self.x = x
        self.y = y
        self.hp = hp

class Wall(BaseObject):
    def __init__(self, sprite, x, y, material="", tile_size=10):
        scale = 1 / 160 * tile_size
        self.multiplier = 1
        if material == "copper":
            hp = 50
        elif material == "iron":
            hp = 200
        elif material == "titanium":
            hp = 400
        elif material == "steel":
            hp = 700
        super().__init__(sprite, x, y, hp, scale)
        self.material = material

    def logic(self, dash, tile_size):
        pass


class Base(BaseObject):
    def __init__(self, sprite, x, y, hp, tile_size):
        scale = 1 / 160 * tile_size
        self.multiplier = 1
        super().__init__(sprite, x, y, hp, scale)
        self.storage = {}
        self.storage_max = 8000

    def logic(self, dash, tile_size):
        pass


class Factory(BaseObject):
    def __init__(self, sprite, x, y, hp, building_type, tile_size):
        self.building_type = building_type
        self.storage_inp = 0
        self.storage_out = 0
        self.energy = 0
        self.storage_max = 10
        self.working = False
        self.multiplier = 2
        scale = 1 / 160 * tile_size
        """Задается тип постройки"""
        if building_type == "smelter":
            self.energy_cost = 15
            self.inp = ["iron", 1.5]  # предмет на вход и нужное количество
            self.out = ["steel", 1]  # предмет на выход и его количество в секунду
        elif building_type == "concentrator":
            self.energy_cost = 20
            self.inp = ["uranium", 2]
            self.out = ["enriched_uranium", 0.5]
        elif building_type == "press":
            self.energy_cost = 10
            self.inp = ["coal", 1]
            self.out = ["graphite", 0.5]
        super().__init__(sprite, x, y, hp, scale)

    def logic(self, dash, tile_size):
        self.working = self.storage_inp >= self.inp[1]  # and self.energy > 0
        if self.working:
            self.storage_inp -= self.inp[1] / 20
            # self.energy -= self.energy_cost / 20
            if self.storage_out >= 1:
                output_find(self, dash, tile_size)


class Conveyor(BaseObject):
    def __init__(self, sprite, x, y, hp, direction: tuple, tile_size):
        scale = 1 / 160 * tile_size
        self.storage_max = 5
        self.storage = 0
        self.multiplier = 1
        self.type = ''
        self.direction = direction
        super().__init__(sprite, x, y, hp, scale)

    def logic(self, dash, tile_size):
        if self.storage >= 1:
            a = dash[self.x + self.direction[0] * tile_size, self.y + self.direction[1] * tile_size]
            if a:
                if a.storage < self.storage_max:
                    if isinstance(a, Conveyor):
                        a.storage = 1 if a.storage < 1 and a.type != self.type else (a.storage + 1)
                        self.storage -= 1
                        a.type = self.type
                    elif isinstance(a, Base):
                        a.storage[self.type] = a.storage.get(self.type, 0) + 1
                        self.storage -= 10 / 20
                    elif isinstance(a, Factory) or isinstance(a, Powerstation):
                        if a.inp[0] == self.type:
                            a.storage_inp = a.storage_inp + 10 / 20
                            self.storage -= 10 / 20


"""class Powerstation(BaseObject):
    def __init__(self, x, y, hp):
        self.storage_max = 10
        self.storage = 0
        self.generating = False
        if type == "coal":
            self.sprite = ""
            self.inp = ["coal", 1]
            self.size = 2
            self.energy_generating = 20
        elif type == "uranium":
            self.sprite = ""
            self.size = 4
            self.inp = ["uranium", 1]
            self.energy_generating = 100
        super().__init__(self.sprite, x, y, hp)

    def logic(self, dash, tile_size):
        self.generating = self.storage >= 1
        if self.generating:
            self.storage -= self.inp[1] / 20"""

"""class PowerLine(BaseObject):
    def __init__(self, x, y, hp):
        super().__init__(self.sprite, x, y, hp)
"""


class Drill(BaseObject):
    def __init__(self, sprite, x, y, hp, building_type, world, tile_size):
        self.building_type = building_type
        self.storage_max = 10
        self.storage = 0
        self.multiplier = 2
        scale = 1 / 160 * tile_size
        self.out = []
        if building_type == "copper":
            self.can_mining = ["copper", "iron", "coal", "lithium"]
            self.mining_speed = 0.5
        elif building_type == "steel":
            self.can_mining = ["copper", "iron", "coal", "titanium", "lithium"]
            self.mining_speed = 1
        elif building_type == "lazer":
            self.can_mining = ["copper", "iron", "coal", "titanium", "lithium", "uranium"]
            self.mining_speed = 2
        l = []
        way = [(1, 0), (0, 1), (1, 1), (0, 0)]
        for i in way:
            nx, ny = x + 10 * i[0], y + 10 * i[1]
            l.append(world[nx, ny])
            l.sort(reverse=True, key=lambda x: l.count(x))
        for i in l:
            if i in self.can_mining:
                self.mining_speed *= l.count(i) / 4
                self.out = [i]
                break
        super().__init__(sprite, x, y, hp, scale)

    def logic(self, dash, tile_size):
        self.storage = self.mining_speed / 20
        if self.storage >= 1:
            output_find(self, dash, tile_size)


"""class Enemy(BaseObject):
    def __init__(self, x, y, hp):
        self.count = 0
        self.fram = 0
        self.speed = 30
        self.dir = (0, 0)
        self.sprite = ""
        super().__init__(self.sprite, x, y, hp)

    def logic(self, tile_size, path, obj):
        dx, dy = self.x - path[self.count][0] * tile_size, self.y - path[self.count][1] * tile_size
        if math.sign(dx) != self.dir[0] or math.sign(dy) != self.dir[1]:
            self.count += 1
        self.dir = (math.sign(dx), math.sign(dy))
        if abs(dir[0]) == abs(dir[1]):
            self.x = self.x + dir[0] * tile_size * self.speed * 0.5
            self.y = self.y + dir[1] * tile_size * self.speed * 0.5
        else:
            self.x = self.x + dir[0] * tile_size * self.speed
            self.y = self.y + dir[1] * tile_size * self.speed
        self.fram += 1
        if self.fram == 30:
            self.fram = 0
            nearest = []
            for i in obj.values():
                nearest.append(min(i, key=lambda p: (p.x - self.x) ** 2 + (p.y - self.y) ** 2))
            nearest = min(nearest, key=lambda p: (p.x - self.x) ** 2 + (p.y - self.y) ** 2)
            angle = math.atan2(self.y - nearest[1], self.x - nearest[0])
            bullet = Bullet(self.x, self.y, angle)"""

"""class Bullet(arcade.Sprite):
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 30
        self.angle = angle
        super().__init__(self.sprite)

    def logic(self):
        self.x = self.x + self.speed * math.cos(self.angle)
        self.y = self.y + self.speed * math.sin(self.angle)
"""


def output_find(self, dash, tile_size):
    """поиск конвейера на выход"""
    way = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for w in way:
        dx, dy = w
        if dx == 0:
            dy *= self.size
            for i in range(self.size):
                dx += i
                a = dash[(self.x + dx * tile_size, self.y + dy * tile_size)]
                if isinstance(a, Conveyor):
                    if a.direction != way[way.index(w) + 2 % 4] and a.storage_max > a.storage:
                        a.storage = a.storage + 1
                        self.storage_inp -= 1
                        a.type = self.out[0]
        else:
            dx *= self.size
            for i in range(self.size):
                dy += i
                a = dash[(self.x + dx * tile_size, self.y + dy * tile_size)]
                if isinstance(a, Conveyor):
                    if a.direction != way[way.index(w) + 2 % 4] and a.storage_max > a.storage:
                        a.storage = a.storage + 1
                        self.storage -= 1
                        a.type = self.out[0]


class AStar2D:
    def __init__(self, grid):
        """
        :param grid: Словарь, где:
            - ключ: (x, y) координаты клетки
            - значение: стоимость прохода (> 0 - проходимо, <= 0 - препятствие)
        """
        self.grid = grid
        self.execution_time = 0.0
        self.nodes_explored = 0

        # Находим границы сетки из ключей словаря
        if grid:
            self.min_x = min(x for x, _ in grid.keys())
            self.max_x = max(x for x, _ in grid.keys())
            self.min_y = min(y for _, y in grid.keys())
            self.max_y = max(y for _, y in grid.keys())
        else:
            self.min_x = self.max_x = self.min_y = self.max_y = 0

    def find_path(self, start, end, allow_diagonal_corner_cutting=False):
        """
        :param start: (x, y) стартовой точки
        :param end: (x, y) конечной точки
        :param allow_diagonal_corner_cutting: разрешить движение по диагонали через углы
        :return: (путь, общая стоимость) или None если путь не найден
        """

        self.nodes_explored = 0
        start_time = time.perf_counter()

        # Проверка валидности точек
        if start not in self.grid or end not in self.grid:
            self.execution_time = time.perf_counter() - start_time
            return None

        if self.grid[start] <= 0 or self.grid[end] <= 0:
            self.execution_time = time.perf_counter() - start_time
            return None

        open_set = []
        counter = 0

        g_score = {}
        f_score = {}
        came_from = {}
        in_open_set = set()
        in_closed_set = set()

        sx, sy = start
        g_score[start] = 0
        f_score[start] = self._octile_heuristic(start, end)

        heapq.heappush(open_set, (f_score[start], counter, start))
        in_open_set.add(start)
        counter += 1
        # (dx, dy, move_cost)
        straight_cost = 1.0
        diagonal_cost = math.sqrt(2)
        neighbors = [
            (0, -1, straight_cost),
            (0, 1, straight_cost),
            (-1, 0, straight_cost),
            (1, 0, straight_cost),
            (-1, -1, diagonal_cost),
            (1, -1, diagonal_cost),
            (-1, 1, diagonal_cost),
            (1, 1, diagonal_cost)
        ]

        while open_set:
            current_f, _, (x, y) = heapq.heappop(open_set)
            current = (x, y)
            self.nodes_explored += 1

            if current == end:
                path = self._reconstruct_path(came_from, start, end)
                self.execution_time = time.perf_counter() - start_time
                return path

            try:
                in_open_set.remove(current)
            except KeyError:
                pass
            in_closed_set.add(current)

            for dx, dy, move_cost in neighbors:
                neighbor = (x + dx, y + dy)

                if neighbor not in self.grid or self.grid[neighbor] <= 0:
                    continue

                if neighbor in in_closed_set:
                    continue

                if abs(dx) == 1 and abs(dy) == 1:
                    if not allow_diagonal_corner_cutting:
                        side1 = (x + dx, y)
                        side2 = (x, y + dy)

                        if (side1 not in self.grid or self.grid[side1] <= 0 or
                                side2 not in self.grid or self.grid[side2] <= 0):
                            continue

                cell_cost = self.grid[neighbor]
                tentative_g = g_score[current] + (move_cost * cell_cost)

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._octile_heuristic(neighbor, end)

                    if neighbor not in in_open_set:
                        heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
                        in_open_set.add(neighbor)
                        counter += 1
                    else:
                        heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
                        counter += 1

        return None

    def _octile_heuristic(self, a, b):
        """Октильная эвристика для 8 направлений"""
        x1, y1 = a
        x2, y2 = b

        dx = abs(x1 - x2)
        dy = abs(y1 - y2)

        D = 1.0
        D2 = math.sqrt(2)

        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

    def _reconstruct_path(self, came_from, start, end):
        """Восстановление пути от end к start"""
        path = []
        current = end

        while current != start:
            path.append(current)
            current = came_from.get(current)
            if current is None:
                return []

        path.append(start)
        path.reverse()
        return path
