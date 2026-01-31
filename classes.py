class BaseObject:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp


class Wall(BaseObject):
    def __init__(self, x, y, material=""):
        if material == "copper":
            hp = 50
        elif material == "iron":
            hp = 200
        elif material == "titanium":
            hp = 400
        elif material == "steel":
            hp = 700
        super().__init__(x, y, hp)
        self.material = material

    def logic(self, dash, tile_size):
        pass


class Base(BaseObject):
    def __init__(self, x, y, hp):
        super().__init__(x, y, hp)
        self.storage = {}
        self.storage_max = 8000

    def logic(self, dash, tile_size):
        pass


class Factory(BaseObject):
    def __init__(self, x, y, hp, type):
        super().__init__(x, y, hp)
        self.type = type
        self.storage_inp = 0
        self.storage_out = 0
        self.energy = 0
        self.storage_max = 10
        self.working = False
        """Задается тип постройки"""
        if type == "smelter":
            self.energy_cost = 15
            self.inp = ["iron", 1.5]  # предмет на вход и нужное количество
            self.size = 2  # размер в клетках
            self.sprite = ""
            self.out = ["steel", 1]  # предмет на выход и его количество в секунду
        elif type == "concentrator":
            self.energy_cost = 20
            self.inp = ["uranium", 2]
            self.size = 2
            self.sprite = ""
            self.out = ["enriched_uranium", 0.5]
        elif type == "press":
            self.energy_cost = 10
            self.inp = ["coal", 1]
            self.size = 2
            self.sprite = ""
            self.out = ["graphite", 0.5]

    def logic(self, dash, tile_size):
        self.working = self.storage_inp == self.inp[1] and self.energy > 0
        if self.working:
            output_find(self, dash, tile_size)


class Conveyor(BaseObject):
    def __init__(self, x, y, hp, direction: tuple):
        super().__init__(x, y, hp)
        self.storage_max = 5
        self.storage = 0
        self.type = ''
        self.direction = direction

    def logic(self, dash, tile_size):
        if self.storage >= 1:
            a = dash[self.x + self.direction[0] * tile_size, self.y + self.direction[1] * tile_size]
            if a:
                if a.storage < self.storage_max:
                    if isinstance(a, Conveyor):
                        a.storage = 10 / 20 if a.storage < 1 and a.type != self.type else (a.storage + 10 / 20)
                        self.storage -= 10 / 20
                        a.type = self.type
                    elif isinstance(a, Base):
                        a.storage[self.type] = a.storage.get(self.type, 0) + 10 / 20
                        self.storage -= 10 / 20
                    elif isinstance(a, Factory) or isinstance(a, Powerstation):
                        if a.inp[0] == self.type:
                            a.storage_inp = a.storage_inp + 10 / 20
                            self.storage -= 10 / 20


class Powerstation(BaseObject):
    def __init__(self, x, y, hp):
        super().__init__(x, y, hp)
        self.storage_max = 10
        self.storage = 0
        self.generating = False
        if type == "coal":
            self.inp = ["coal", 1]
            self.energy_generating = 20
        elif type == "uranium":
            self.inp = ["uranium", 1]
            self.energy_generating = 100

    def logic(self, dash, tile_size):
        self.generating = self.storage >= 1
        if self.generating:
            self.storage -= 1 / 20


class PowerLine(BaseObject):
    def __init__(self, x, y, hp):
        super().__init__(x, y, hp)


class Drill(BaseObject):
    def __init__(self, x, y, hp, type, world):
        self.storage_max = 10
        self.storage = 0
        self.size = 2
        self.energy_cost = 0
        self.energy = 0
        if type == "copper":
            self.can_mining = ["copper", "iron", "coal", "lithium"]
            self.mining_speed = 0.5
        elif type == "steel":
            self.can_mining = ["copper", "iron", "coal", "titanium", "lithium", ]
            self.mining_speed = 1
        elif type == "lazer":
            self.energy_cost = 15
            self.can_mining = ["copper", "iron", "coal", "titanium", "lithium", "uranium"]
            self.mining_speed = 2
        way = [(1, 0), (0, 1), (1, 1)]
        for i in way:
            nx, ny = x + 10 * i[0], y + 10 * i[1]
            l.append(world[x, y])
            l.sort(reverse=True)
        for i in l:
            if i in self.can_mining:
                self.mining_speed *= l.count(i) / 4
                break
        super().__init__(x, y, hp)

    def logic(self, dash, tile_size):
        output_find(self, dash, tile_size)


class Enemy(BaseObject):
    def __init__(self, x, y, hp):
        super().__init__(x, y, hp)


def output_find(self, dash, tile_size, inpc, outc):
    """поиск конвейера на выход"""
    way = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for w in way:
        dx, dy = w
        if dx == 0:
            dy *= self.size
            for i in range(self.size):
                dx += i
                a = dash[self.x + dx * tile_size, self.y + dy * tile_size]
                if isinstance(a, Conveyor):
                    if a.direction != way[way.index(w) + 2 % 4] and self.storage_out >= self.out[1]:
                        a.storage = (a.storage + self.out[1] / 20) % (a.storage_max + 1)
                        self.energy -= self.energy_cost / 20
                        self.storage_inp -= self.inp[1] / 20
                        a.type = self.out[0]
        else:
            dx *= self.size
            for i in range(self.size):
                dy += i
                a = dash[self.x + dx * tile_size, self.y + dy * tile_size]
                if isinstance(a, Conveyor):
                    if a.direction != way[way.index(w) + 2 % 4] and a.storage >= self.inp[1]:
                        a.storage = (a.storage + self.out[1] / 20) % (a.storage_max + 1)
                        self.energy -= self.energy_cost / 20
                        self.storage -= self.inpc
                        a.type = self.out[0]
