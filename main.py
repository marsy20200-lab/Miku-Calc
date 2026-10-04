from kivy.app import App
from kivy.core.window import Window
import config
from gui import MikuMobileCalculator

# Настраиваем размеры окна из конфига
Window.size = (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

class MicuCalcApp(App):
    def build(self):
        self.title = "Micu Calc 🎧"
        return MikuMobileCalculator()

if __name__ == '__main__':
    MicuCalcApp().run()
