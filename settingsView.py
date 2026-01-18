import arcade
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout, UISpace, UIMessageBox

from baseView import BaseView


class SettingsView(BaseView):
    def __init__(self, window):
        super().__init__(window)
        self.create_widget()

    def create_widget(self):
        self.anchor = UIAnchorLayout()
        self.anchor.default_anchor_x = 'left'
        self.anchor.default_anchor_y = 'bottom'

        self.vert_layout = UIBoxLayout(vertical=True, space_between=10)
        self.hor_layout = UIBoxLayout(vertical=False, space_between=10)

        vert_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))
        hor_space = UISpace(width=25, height=25, color=(0, 0, 0, 0))

        back_normal = arcade.load_texture("sprites/button_back/button_back_normal.png")
        back_active = arcade.load_texture("sprites/button_back/button_back_active.png")
        back_triggered = arcade.load_texture("sprites/button_back/button_back_triggered.png")

        button_back = UITextureButton(texture=back_normal,
                                      texture_hovered=back_active,
                                      texture_pressed=back_triggered, scale=0.1)

        self.vert_layout.add(button_back)
        self.vert_layout.add(vert_space)

        self.hor_layout.add(hor_space)
        self.hor_layout.add(self.vert_layout)

        self.anchor.add(self.hor_layout)

        self.manager.add(self.anchor)

        button_back.on_click = self.back_triggered

    def back_triggered(self, arg):
        self.window.show_view(self.window.menu_view)