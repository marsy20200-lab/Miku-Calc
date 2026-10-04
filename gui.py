from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.animation import Animation

import config
import logic
from widgets import AnimatedButton, BorderedDisplay

class MikuMobileCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 12
        self.spacing = 8
        self.history_list = []
        
        with self.canvas.before:
            Color(*config.COLOR_BG)
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.miku_speech = Label(
            text=config.TXT_START,
            font_size=14, color=config.COLOR_TEXT, bold=True, halign='center', size_hint=(1, 0.06)
        )
        self.add_widget(self.miku_speech)
        
        history_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.18))
        history_header = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))
        history_title = Label(text=" История:", font_size=12, color=config.COLOR_TEXT, halign='left', valign='middle')
        history_title.bind(size=history_title.setter('text_size'))
        
        clear_history_btn = AnimatedButton(text="Очистить историю", font_size=11, size_hint=(0.4, 1), background_color=config.COLOR_DARK_BLUE)
        clear_history_btn.bind(on_press=self.clear_history)
        
        history_header.add_widget(history_title)
        history_header.add_widget(clear_history_btn)
        history_layout.add_widget(history_header)
        
        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.history_label = Label(text=config.TXT_EMPTY_HISTORY, font_size=14, color=(0.2, 0.35, 0.5, 1), halign='left', valign='top', size_hint_y=None, padding=(5, 5))
        self.history_label.bind(size=self.history_label.setter('text_size'), texture_size=self.history_label.setter('size'))
        self.scroll_view.add_widget(self.history_label)
        history_layout.add_widget(self.scroll_view)
        self.add_widget(history_layout)
        
        self.display = BorderedDisplay(size_hint=(1, 0.14))
        self.add_widget(self.display)
        
        keyboard_container = FloatLayout(size_hint=(1, 0.56))
        self.bg_image = Image(source=config.BACKGROUND_IMAGE, allow_stretch=True, keep_ratio=False, size_hint=(1.06, 1.05), pos_hint={'x': -0.03, 'y': -0.02})
        keyboard_container.add_widget(self.bg_image)
        
        grid = GridLayout(cols=4, spacing=6, size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        
        # Обновленный список кнопок без багов шрифта и пустых зон
        buttons = [
            'C', '<-', '√', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '.', '0', '%', '='
        ]
        
        for btn_text in buttons:
            bg_color = config.COLOR_DARK_BLUE if btn_text in ['C', '<-', '√', '/', '*', '-', '+', '%'] else (config.COLOR_ACCENT if btn_text == '=' else config.COLOR_BUTTON)
            button = AnimatedButton(text=btn_text, font_size=24, bold=True, background_color=bg_color, color=(1, 1, 1, 1))
            button.bind(on_press=self.on_button_click)
            grid.add_widget(button)
            
        keyboard_container.add_widget(grid)
        self.add_widget(keyboard_container)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def change_miku_text(self, new_text):
        def refresh_text(*args):
            self.miku_speech.text = new_text
            Animation(opacity=1.0, duration=0.18).start(self.miku_speech)
        fade_out = Animation(opacity=0.0, duration=0.12)
        fade_out.bind(on_complete=refresh_text)
        fade_out.start(self.miku_speech)

    def clear_history(self, instance):
        self.history_list = []
        self.history_label.text = config.TXT_EMPTY_HISTORY
        self.change_miku_text(config.TXT_HISTORY_CLEARED)

    def on_button_click(self, instance):
        current_text = self.display.text
        button_text = instance.text
        
        self.display.flash_border()
        
        if button_text == 'C':
            self.display.text = ""
            self.change_miku_text(config.TXT_RESET)
        elif button_text == '<-':
            if current_text:
                self.display.text = current_text[:-1]
        elif button_text == '√':
            res, speech = logic.calculate_sqrt(current_text)
            self.change_miku_text(speech)
            if res is not None:
                self.history_list.append(f"√({current_text}) = {res}")
                self.history_label.text = "\n".join(self.history_list[-4:])
                self.display.text = str(res)
        elif button_text == '%':
            if not current_text: return
            res, speech = logic.calculate_percent(current_text)
            self.change_miku_text(speech)
            if res is not None:
                self.history_list.append(f"{current_text}% = {res}")
                self.history_label.text = "\n".join(self.history_list[-4:])
                self.display.text = str(res)
        elif button_text == '=':
            if not current_text: return
            res, speech = logic.calculate_expression(current_text)
            self.change_miku_text(speech)
            if res is not None:
                if res == "zero_division":
                    self.display.text = ""
                else:
                    self.history_list.append(f"{current_text} = {res}")
                    self.history_label.text = "\n".join(self.history_list[-4:])
                    self.display.text = str(res)
        else:
            if not current_text and button_text in ['+', '-', '*', '/', '.']: return
            if current_text and current_text[-1] in ['+', '-', '*', '/', '.'] and button_text in ['+', '-', '*', '/', '.']: return
            
            if len(current_text) >= config.CHAR_LIMIT:
                self.change_miku_text(config.TXT_LIMIT_ERROR)
                return
                
            self.display.text += button_text
