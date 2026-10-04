from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Line
from kivy.animation import Animation
import config

class AnimatedButton(Button):
    """Кнопка, плавно реагирующая на нажатия через прозрачность"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        
    def on_press(self):
        Animation(opacity=0.35, duration=0.08).start(self)
        
    def on_release(self):
        Animation(opacity=1.0, duration=0.15).start(self)

class BorderedDisplay(Label):
    """Экранчик вычислений со вспыхивающей неоновой рамкой"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 38
        self.color = config.COLOR_TEXT
        self.bold = True
        self.halign = 'right'
        self.valign = 'middle'
        self.padding = (15, 10)
        
        with self.canvas.after:
            self.border_color = Color(*config.COLOR_DARK_BLUE)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=2)
            
        self.bind(size=self._update_border, pos=self._update_border)

    def _update_border(self, instance, value):
        self.text_size = instance.size
        offset = 2
        self.border.rectangle = (instance.x + offset, instance.y + offset, instance.width - offset*2, instance.height - offset*2)

    def flash_border(self):
        """Плавная анимация изменения цвета рамки при вводе"""
        anim = Animation(rgba=(0.15, 0.45, 0.65, 0.9), duration=0.1) + Animation(rgba=config.COLOR_DARK_BLUE, duration=0.2)
        anim.start(self.border_color)
