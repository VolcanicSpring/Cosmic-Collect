import random
import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Ellipse, Color, Line
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
# --- KivyMD UI imports ---
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image

from kivy.properties import StringProperty, NumericProperty

class Food_icon(MDCard):
    food_text = StringProperty("")

class Level_icon(MDCard):
    level_text = StringProperty("")
    exp_value = NumericProperty(0)
    exp_max = NumericProperty(100)

# --- KivyMD custom icons ---
KV = '''
<Food_icon>:
    orientation: "horizontal"
    size_hint: None, None
    size: "100dp", "44dp"
    radius: [22,]
    md_bg_color: [1, 0.93, 0.76, 1]
    elevation: 7
    padding: "0dp"
    spacing: "7dp"
    Image:
        source: "Food_icon.png"
        size_hint: None, None
        size: "50dp", "50dp"
    MDLabel:
        id: food_label
        text: root.food_text
        font_style: "Title"
        bold: True
        halign: "center"
        theme_text_color: "Custom"
        text_color: 0.55, 0.23, 0.10, 1

<Level_icon>:
    orientation: "horizontal"
    size_hint: None, None
    size: "420dp", "44dp"
    radius: [22,]
    md_bg_color: [0.93, 0.84, 1, 1]
    elevation: 7
    padding: "1dp"
    spacing: "7dp"
    Image:
        source: "Level_icon.png"
        size_hint_x: None
        width: self.height
        size_hint_y: 1
        size: "50dp", "50dp"
    MDLabel:
        id: lvl
        text: "Lv " + root.level_text
        font_style: "Title"
        bold: True
        halign: "center"
        size_hint_x: 0.18
        theme_text_color: "Custom"
        text_color: 0.98, 0.78, 0, 1
    BoxLayout:
        orientation: "vertical"
        size_hint_x: 0.6
        padding: 0
        spacing: 0
        Widget:
            size_hint_y: 0.23
        Widget:
            size_hint_y: None
            height: "22dp"
            canvas.before:
                Color:
                    rgba: 0.9, 0.8, 1, 1  # background bar color
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [8,]
                Color:
                    rgba: 0.78, 0.4, 1, 1  # progress color
                RoundedRectangle:
                    pos: self.x, self.y
                    size: self.width * (root.exp_value / (root.exp_max if root.exp_max else 1)), self.height
                    radius: [8,]
        Widget:
            size_hint_y: 0.23
        Widget:
            size_hint_y: 0.23

    MDLabel:
        text: f"{int(root.exp_value)}/{int(root.exp_max)}"
        font_style: "Body"
        halign: "center"
        size_hint_x: 0.18
        theme_text_color: "Custom"
        text_color: 0.3, 0.12, 0.12, 1
'''

Builder.load_string(KV)

class Entity(Widget):
    """Base class for all entities (food, atom, etc). Handles rendering and state."""
    def render_graphics(self):
        with self.canvas:
            Color(0.2, 0.6, 1, 1)  # Blue Proton Color
            self.ellipse = Ellipse(pos=self.pos, size=self.size)
            Color(1, 1, 1, 1)  # White + symbol
            plus_size = self.radius * 0.6
            self.h_line = Line(points=[], width=1.5)
            self.v_line = Line(points=[], width=1.5)
        self.update_graphics()
    def become_atom(self):
        self.radius *= 1.8
        self.size = (self.radius * 2, self.radius * 2)
        self.pos = (self.center[0] - self.radius, self.center[1] - self.radius)
        self.canvas.clear()
        with self.canvas:
            Color(0.8, 0.3, 0.3, 1)  # reddish nucleus
            nucleus_radius = self.radius * 0.5
            Ellipse(pos=(self.center_x - nucleus_radius, self.center_y - nucleus_radius), size=(nucleus_radius * 2, nucleus_radius * 2))
            Color(1, 1, 1, 0.3)
            Line(circle=(self.center_x, self.center_y, self.radius * 0.8), width=1)
            for angle in [45, 225]:
                ex = self.center_x + self.radius * 0.8 * math.cos(math.radians(angle)) - dp(3)
                ey = self.center_y + self.radius * 0.8 * math.sin(math.radians(angle)) - dp(3)
                Color(0.2, 0.6, 1, 1)
                Ellipse(pos=(ex, ey), size=(dp(6), dp(6)))
    def __init__(self, color, radius=None, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius if radius is not None else min(Window.width, Window.height) * 0.012
        self.size = (self.radius * 2, self.radius * 2)
        top_ui_height = dp(70)
        bottom_ui_height = dp(60)
        self.center = (
            random.randint(int(self.radius), int(Window.width - self.radius)),
            random.randint(int(self.radius + bottom_ui_height), int(Window.height - self.radius - top_ui_height))
        )
        self.pos = (self.center[0] - self.radius, self.center[1] - self.radius)
        
            
        self.render_graphics()
        

    def update_graphics(self):
        self.ellipse.pos = self.pos
        self.ellipse.size = self.size
        center_x = self.pos[0] + self.radius
        center_y = self.pos[1] + self.radius
        plus_size = self.radius * 0.6
        self.h_line.points = [center_x - plus_size, center_y, center_x + plus_size, center_y]
        self.v_line.points = [center_x, center_y - plus_size, center_x, center_y + plus_size]

class Player(Entity):
    """Player controlled by the user. Has electrons and responds to joystick input."""
    def __init__(self, **kwargs):
        super().__init__((0.2, 0.8, 1), **kwargs)
        self.radius = min(Window.width, Window.height) * 0.025  # original size (2.5% of min dimension)
        self.size = (self.radius * 2, self.radius * 2)
        self.center = (Window.width // 2, Window.height // 2)
        self.dragging = False
        self.joystick_vector = (0, 0)

        with self.canvas:
            Color(0, 1, 0, 1)  # Green nucleus
            nucleus_radius = self.radius * 0.6
            self.nucleus = Ellipse(pos=(self.center[0] - nucleus_radius, self.center[1] - nucleus_radius), size=(nucleus_radius * 2, nucleus_radius * 2))
            Color(1, 1, 1, 0.5)  # Orbit lines
            self.orbit1 = Line(circle=(self.center_x, self.center_y, self.radius * 1.0, 0, 360), width=1)
            self.orbit2 = Line(circle=(self.center_x, self.center_y, self.radius * 1.2, 45, 405), width=1)
            self.orbit3 = Line(circle=(self.center_x, self.center_y, self.radius * 1.4, 90, 450), width=1)
        self.electrons = []
        electron_size = dp(6)
        for angle in [0, 90, 180, 270]:
            er = self.radius * 1.2
            ex = self.center_x + er * math.cos(math.radians(angle)) - electron_size / 2
            ey = self.center_y + er * math.sin(math.radians(angle)) - electron_size / 2
            with self.canvas:
                Color(0.2, 0.6, 1, 1)
                e = Ellipse(pos=(ex, ey), size=(electron_size, electron_size))
                self.electrons.append([e, angle, er])
        self.update_graphics = self.update_atom_graphics

    def update_atom_graphics(self, dt=0):
        nucleus_radius = self.radius * 0.8
        self.nucleus.pos = (self.center_x - nucleus_radius, self.center_y - nucleus_radius)
        self.nucleus.size = (nucleus_radius * 2, nucleus_radius * 2)
        cx, cy = self.center
        self.orbit1.circle = (cx, cy, self.radius * 1.0, 0, 360)
        self.orbit2.circle = (cx, cy, self.radius * 1.2, 45, 405)
        self.orbit3.circle = (cx, cy, self.radius * 1.4, 90, 450)
        electron_size = dp(6)
        for i, (e, angle, r) in enumerate(self.electrons):
            angle += 60 * dt  # 60 degrees per second
            angle %= 360
            self.electrons[i][1] = angle
            ex = cx + r * math.cos(math.radians(angle)) - electron_size / 2
            ey = cy + r * math.sin(math.radians(angle)) - electron_size / 2
            e.pos = (ex, ey)

    def move(self, dt):
        speed = dp(2.5)
        speed *= getattr(self, 'move_speed_multiplier', 1.0)
        dx = self.joystick_vector[0] * speed
        dy = self.joystick_vector[1] * speed
        new_x = self.center_x + dx
        new_y = self.center_y + dy
        top_ui_height = dp(70)
        bottom_ui_height = dp(60)
        self.center = (
            max(self.radius, min(Window.width - self.radius, new_x)),
            max(self.radius + bottom_ui_height, min(Window.height - self.radius - top_ui_height, new_y))
        )
        self.pos = (self.center[0] - self.radius, self.center[1] - self.radius)
        self.update_graphics()

class Joystick(Widget):
    """Touch joystick controller for player movement."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visible = False
        self.radius = Window.width * 0.07
        self.knob_radius = Window.width * 0.035
        self.knob_center = (0, 0)
        with self.canvas:
            self.outer_color = Color(1, 1, 1, 0.3)
            self.outer_circle = Line(circle=(0, 0, self.radius), width=1)
            self.inner_color = Color(1, 1, 1, 0.5)
            self.inner_circle = Ellipse(size=(self.knob_radius*2, self.knob_radius*2))

    def show(self, pos):
        self.visible = True
        self.center = pos
        self.knob_center = pos
        self.update_graphics()

    def move_knob(self, pos):
        dx = pos[0] - self.center[0]
        dy = pos[1] - self.center[1]
        dist = math.sqrt(dx*dx + dy*dy)
        max_dist = self.radius
        if dist > max_dist:
            scale = max_dist / dist
            dx *= scale
            dy *= scale
        self.knob_center = (self.center[0] + dx, self.center[1] + dy)
        self.update_graphics()
        return (dx / max_dist, dy / max_dist)

    def hide(self):
        self.visible = False
        self.update_graphics()

    def update_graphics(self):
        self.outer_circle.circle = (self.center[0], self.center[1], self.radius)
        self.inner_circle.pos = (self.knob_center[0] - self.knob_radius, self.knob_center[1] - self.knob_radius)

class Molecule(Player):
    """Evolved player (after evolve button). Has branches and a red core."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas.clear()
        with self.canvas:
            

            self.branches = []
            self.sticks = []
            Color(0.7, 0.7, 0.7, 1)  # Stick color
            branch_info = [
            (50, 0.5),
            (180, 0.8),
            (300, 1.0),
        ]
            branch_colors = [
                (0.8, 1, 0.8, 1),  # light green
                (0.4, 0.7, 1, 1),  # blue
                (0.6, 1, 0.6, 1),  # green
            ]
            for i, (angle, scale) in enumerate(branch_info):
                offset = self.radius * 1.8
                bx = self.center_x + offset * math.cos(math.radians(angle))
                by = self.center_y + offset * math.sin(math.radians(angle))
                size = self.radius * scale
                stick = Line(points=[self.center_x, self.center_y, bx, by], width=dp(2))
                self.sticks.append(stick)
                Color(*branch_colors[i])
                branch = Ellipse(pos=(bx - size / 2, by - size / 2), size=(size, size))
                self.branches.append((branch, angle, scale))
        with self.canvas:
            Color(1, 0.4, 0.4, 1)  # Central atom (red)
            self.core = Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius), size=(self.radius * 2, self.radius * 2))
        self.update_graphics = self.update_molecule_graphics

    def update_molecule_graphics(self, dt=0):
        cx, cy = self.center
        r = self.radius
        self.core.pos = (cx - r, cy - r)
        self.core.size = (r * 2, r * 2)
        branch_info = [
            (150, 0.5),
            (30, 0.8),
            (270, 1.0),
        ]
        for i, (branch, angle, scale) in enumerate(self.branches):
            offset = r * 1.8
            bx = cx + offset * math.cos(math.radians(angle))
            by = cy + offset * math.sin(math.radians(angle))
            size = r * scale
            branch.pos = (bx - size / 2, by - size / 2)
            branch.size = (size, size)
            self.sticks[i].points = [cx, cy, bx, by]

class UpgradeMenu(BoxLayout):
    """Bottom menu for upgrades: FOV, evolve, and atom-food."""
    def __init__(self, game_widget, **kwargs):
        self.fov_cost = 5
        self.new_food_cost = 10
        super().__init__(orientation='horizontal', size_hint=(1, 0.1), **kwargs)
        self.game_widget = game_widget
        self.fov_btn = Button(text=f"Upgrade FOV\n({self.fov_cost} food)", font_size=dp(18), size_hint_x=0.5)
        self.fov_btn.bind(on_release=self.upgrade_fov)
        self.add_widget(self.fov_btn)
        self.evolve_btn = Button(text=f"Evolve(10 food)", font_size=dp(18), size_hint_x=0.33)
        self.evolve_btn.bind(on_release=self.evolve)
        self.add_widget(self.evolve_btn)
        self.new_food_btn = Button(text=f"New Food({self.new_food_cost} food)", font_size=dp(18), size_hint_x=0.34)
        self.new_food_btn.bind(on_release=self.upgrade_food)
        self.add_widget(self.new_food_btn)

    def upgrade_fov(self, instance):
        if self.game_widget.food >= self.fov_cost:
            self.game_widget.player.move_speed_multiplier = getattr(self.game_widget.player, 'move_speed_multiplier', 1.0) * 1.03
            self.game_widget.food -= self.fov_cost
            self.game_widget.fov_multiplier *= 1.1

            for entity in self.game_widget.entities:
                entity.radius *= 0.9
                entity.size = (entity.radius * 2, entity.radius * 2)
                entity.pos = (entity.center[0] - entity.radius, entity.center[1] - entity.radius)
                entity.update_graphics()

            self.game_widget.player.radius *= 1.1
            self.game_widget.player.size = (self.game_widget.player.radius * 2, self.game_widget.player.radius * 2)
            for i in range(len(self.game_widget.player.electrons)):
                self.game_widget.player.electrons[i][2] *= 1.1
            self.game_widget.player.update_graphics(1/60)
            for e, _, _ in self.game_widget.player.electrons:
                e.size = (dp(6) * self.game_widget.fov_multiplier, dp(6) * self.game_widget.fov_multiplier)

            self.game_widget.food_icon.food_text = str(self.game_widget.food)
            self.fov_cost = int(self.fov_cost * 1.3)
            self.fov_btn.text = f"Upgrade FOV({self.fov_cost} food)"

            # Increase food density by 5%
            new_count = max(1, int(len(self.game_widget.entities) * 0.15))
            for _ in range(new_count):
                self.game_widget.spawn_entity()

    def evolve(self, instance):
        if self.game_widget.food >= 10:
            self.game_widget.food -= 10
            self.game_widget.remove_widget(self.game_widget.player)
            self.game_widget.player = Molecule()
            self.game_widget.add_widget(self.game_widget.player)
            Clock.schedule_interval(self.game_widget.player.move, 1/60)
            self.game_widget.food_icon.food_text = str(self.game_widget.food)

    def upgrade_food(self, instance):
        if self.game_widget.food >= self.new_food_cost:
            self.game_widget.food -= self.new_food_cost
            for entity in self.game_widget.entities:
                entity.become_atom()
                entity.atom_mode = True
            self.game_widget.food_icon.food_text = str(self.game_widget.food)
            # Ensure future spawns are atoms
            Entity.atom_mode = True

class GameWidget(Widget):
    """Main game logic, manages player, food, exp, top and bottom UIs."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.food = 0
        self.exp = 0
        self.level = 1
        self.exp_required = 5
        self.fov_multiplier = 1.0

        # --- Background Image ---
        self.background = Image(source="Background1.png", allow_stretch=True, keep_ratio=False)
        self.background.size = Window.size
        self.background.pos = (0, 0)
        self.add_widget(self.background, index=0)

        self.player = Player()
        self.add_widget(self.player)
        self.entities = []

        # --- New KivyMD UI (top row) ---
        self.top_ui = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(55), padding=(dp(12), dp(6)), spacing=dp(16), pos=(0, Window.height-dp(55)))
        from kivy.factory import Factory
        self.food_icon = Factory.Food_icon(food_text=str(self.food))
        self.level_icon = Factory.Level_icon(level_text=str(self.level), exp_value=self.exp, exp_max=self.exp_required)
        self.top_ui.add_widget(self.food_icon)
        self.top_ui.add_widget(Widget())  # Spacer
        self.top_ui.add_widget(self.level_icon)
        self.add_widget(self.top_ui)

        self.joystick = Joystick()
        self.add_widget(self.joystick)
        self.spawn_entities()
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.player.move, 1/60)

    def update_icons(self):
        """Update food and level KivyMD icons to match current game state."""
        self.food_icon.food_text = str(self.food)
        self.level_icon.level_text = str(self.level)
        self.level_icon.exp_value = self.exp
        self.level_icon.exp_max = self.exp_required

    def spawn_entity(self):
        color = (random.random(), random.random(), random.random())
        radius = min(Window.width, Window.height) * 0.012 / self.fov_multiplier
        entity = Entity(color, radius=radius)
        if hasattr(entity, 'atom_mode') and entity.atom_mode:
            entity.become_atom()
        self.entities.append(entity)
        self.add_widget(entity)

    def spawn_entities(self):
        for _ in range(150):
            self.spawn_entity()

    def update(self, dt):
        to_remove = []
        for entity in self.entities:
            dx = self.player.center_x - entity.center_x
            dy = self.player.center_y - entity.center_y
            dist = math.hypot(dx, dy)
            if dist < self.player.radius and entity.radius < self.player.radius:
                to_remove.append(entity)
                self.food += 1
                self.exp += 1
                if self.exp >= self.exp_required:
                    self.level += 1
                    self.exp = 0
                    self.exp_required *= 4
                # --- UPDATE the new KivyMD widgets ---
                self.update_icons()
        for entity in to_remove:
            self.remove_widget(entity)
            self.entities.remove(entity)
            self.spawn_entity()

    def on_touch_down(self, touch):
        self.joystick.show(touch.pos)
        self.player.joystick_vector = self.joystick.move_knob(touch.pos)

    def on_touch_move(self, touch):
        self.player.joystick_vector = self.joystick.move_knob(touch.pos)

    def on_touch_up(self, touch):
        self.joystick.hide()
        self.player.joystick_vector = (0, 0)

class MainApp(MDApp):
    """Main application entrypoint."""
    def build(self):
        root = BoxLayout(orientation='vertical')
        self.game = GameWidget()
        self.upgrade_menu = UpgradeMenu(self.game)
        root.add_widget(self.game)
        root.add_widget(self.upgrade_menu)
        return root

if __name__ == '__main__':
    MainApp().run()
