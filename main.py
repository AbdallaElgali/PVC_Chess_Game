from kivy.app import App
from chess_view import Manager, MainScreen, Chess, CustomButton
from kivy.config import Config
from kivy.core.window import Window
from chess_model import ChessModel
from kivy.lang import Builder
import threading
import playsound
from kivy.uix.screenmanager import ScreenManager, Screen

Window.size = (800, 800)

path = r'C:\Users\scorp\Desktop\Programmin\ChessGames\ChessMVC_PVC_Trial_1\ChessLayout.kv'
class ChessApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_player = None

    def build(self):
        Config.set('graphics', 'resizable', '0')
        Config.write()

        Window.borderless = False

        view = Chess(name='Chess', chess_model=ChessModel())

        sm = Manager()
        sm.add_widget(MainScreen(name='MainScreen'))
        sm.add_widget(view)

        return sm

    def set_selected_player(self, player):
        self.selected_player = player

    def get_selected_player(self):
        return self.selected_player


if __name__ != '__main__':
    pass
else:
    Builder.load_file(path)

    ChessApp().run()
