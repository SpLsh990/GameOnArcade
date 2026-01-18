import arcade


class BackgroundView(arcade.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.enabled = True
        self.textures = []
        self.scale_x = width / 640
        self.scale_y = height / 480
        self.center_x = width // 2
        self.center_y = height // 2
        for i in range(60):
            texture = arcade.load_texture(f'sprites/menu/{i}.png')
            self.textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.03

    def update_animation(self, delta_time: float = 1 / 60):
        if self.enabled:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.textures):
                    self.current_texture = 0
                self.texture = self.textures[self.current_texture]

    def resize(self, width, height):
        self.scale_x = width / 640
        self.scale_y = height / 480
        self.center_x = width // 2
        self.center_y = height // 2

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False