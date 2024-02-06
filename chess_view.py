from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import os
import copy
from kivy.app import App
import subprocess
import threading
from playsound import playsound
from threading import Thread

first_img_list = []

class MainScreen(Screen):
    pass
class Manager(ScreenManager):
    pass

class NextButton(Button):
    def __init__(self, **kwargs):  # Defining the initial state of a button as selected = False
        super(NextButton, self).__init__(**kwargs)
        self.player = ''


    def on_release(self):
        file_path = r"C:\Users\scorp\Desktop\Programmin\ChessGames\ChessMVC_PVC_Trial_1\Sound_Files\board-start.mp3"

        subprocess.run(["start", "wmplayer", file_path], shell=True)
        App.get_running_app().set_selected_player(self.player)

class CustomImage(Image):
    image_id = NumericProperty(None)
    empty_picture = StringProperty(None)

class CustomButton(Button):

    def __init__(self, **kwargs):  # Defining the initial state of a button as selected = False
        super(CustomButton, self).__init__(**kwargs)
        self.selected = False
        self.is_released = True
        self.moved = False


    def get_src(self):

        img_src = ''
        # To get the image id

        for child in self.children:
            if isinstance(child, CustomImage):
                img_src = child.source

        return img_src

    def get_id(self):
        img_id = None
        # To get the image id

        for child in self.children:
            if isinstance(child, CustomImage):
                img_id = child.image_id
                break
        return img_id


    def on_release(self):

        Button_list, _ = self.parent.parent.all_buttons()

        if self.is_released:  # debounce strategy to get around multiple clicks
            self.is_released = False

            select_count = 0  # Check if any button is selected
            for button in Button_list:
                if button.selected:
                    select_count = 1
                else:
                    continue


            if not self.selected:
                if select_count == 0:  # Case: First button to be selected
                    self.select()
                    self.parent.parent.chess_model.select_position(self.get_id())  # send the start_position to the model
                    print('From: ', self.get_id())
                    first_img_list.append(self.get_src())
                    first_img_list.append(self)

                elif select_count == 1:  # Case: Second button is now to be selected
                    self.parent.parent.chess_model.select_position(self.get_id())  # send the end_position to the model
                    self.parent.parent.update()
                    self.deselect()
                    self.parent.parent.chess_model.reset_positions()
                    print('To: ', self.get_id())
                    first_img_list.pop(0)
                    first_img_list.pop(0)


            elif self.selected and select_count == 1:  # Case: First button is Pressed again
                self.deselect()
                self.parent.parent.chess_model.reset_positions()

            Clock.schedule_once(self.reset_clock, .5)



    def fire_after_release(self, dt):
        # Call the fire function here
        self.parent.parent.fire()
    def reset_clock(self, dt):
        self.is_released = True

    def select(self):
        self.selected = True
        print('selected')

    def deselect(self):

        Button_list, _ = self.parent.parent.all_buttons()

        if not self.selected:  # Deselect all buttons
            for button in Button_list:
                if button.selected:
                    button.selected = False
                    print('button deselected')
                else:
                    continue

        else:
            self.selected = False
            print('deselected')

class Chess(Screen):
    chess_model = ObjectProperty(None)
    empty_picture = StringProperty(None)

    def __int__(self, chess_model, **kwargs):
        super(Chess, self).__init__(**kwargs)
        self.chess_model = chess_model

    def __init__(self, **kw):
        super().__init__(**kw)
        self.chess_board = {
            1: 'black_rook', 2: 'black_knight', 3: 'black_bishop', 4: 'black_queen',
            5: 'black_king', 6: 'black_bishop', 7: 'black_knight', 8: 'black_rook',
            9: 'black_pawn', 10: 'black_pawn', 11: 'black_pawn', 12: 'black_pawn',
            13: 'black_pawn', 14: 'black_pawn', 15: 'black_pawn', 16: 'black_pawn',
            17: '', 18: '', 19: '', 20: '', 21: '', 22: '', 23: '', 24: '',
            25: '', 26: '', 27: '', 28: '', 29: '', 30: '', 31: '', 32: '',
            33: '', 34: '', 35: '', 36: '', 37: '', 38: '', 39: '', 40: '',
            41: '', 42: '', 43: '', 44: '', 45: '', 46: '', 47: '', 48: '',
            49: 'white_pawn', 50: 'white_pawn', 51: 'white_pawn', 52: 'white_pawn',
            53: 'white_pawn', 54: 'white_pawn', 55: 'white_pawn', 56: 'white_pawn',
            57: 'white_rook', 58: 'white_knight', 59: 'white_bishop', 60: 'white_queen',
            61: 'white_king', 62: 'white_bishop', 63: 'white_knight', 64: 'white_rook',
        }
    def all_buttons(self):

        Button_list = []
        Image_list = []
        color_list = []
        for row in self.children:
            for id in row.children:
                if isinstance(id, CustomButton) and id is not None and id != '':
                    Button_list.append(id)
                for small_child in id.children:
                    if isinstance(small_child,
                                  CustomImage) and small_child.source != self.empty_picture and not '' or None:
                        Image_list.append(small_child.image_id)
        for r in self.children:
            for i in r.children:
                if isinstance(i, CustomButton) and i is not None and i != '':
                    color = i.background_color
                    color_list.append(color)

        # Remove any duplicates
        temp = list()
        temp_dict = dict()
        count = 0
        for image_id in Image_list:
            temp_dict[image_id] = count
            count += 1

        for key, ids in temp_dict.items():
            temp.append(key)

        temp_b = list()
        temp_dict_b = dict()
        count_b = 0
        for button_id in Button_list:
            temp_dict_b[button_id] = count_b
            count_b += 1

        for key, ids in temp_dict_b.items():
            temp_b.append(key)

        Button_list = temp_b
        Image_list = temp
        return Button_list, Image_list

    def find_button(self, image_id):
        for row in self.children:
            for id in row.children:
                for widget in id.children:
                    if isinstance(widget, CustomImage) and widget.image_id == image_id:
                        parent_button = widget.parent
                        return parent_button
        return None

    def move(self, start_id, end_id):
        move_identifier = False
        eat_identifier = True

        original_source = ''
        for child in self.children:
            if isinstance(child, GridLayout):  # Assuming the chess grid is a GridLayout
                # Iterate over the buttons in the grid
                for button in child.children:
                    if isinstance(button, CustomButton):
                        # Check if the button corresponds to the start_id
                        if button.get_id() == start_id:
                            # Iterate over the children of the CustomButton
                            for c in button.children:
                                if isinstance(c, CustomImage):
                                    original_source = copy.deepcopy(button.get_src())
                                    c.source = r'C:\Users\scorp\Desktop\Programmin\Chess Game\images\Nothing.png'
        for child in self.children:
            if isinstance(child, GridLayout):  # Assuming the chess grid is a GridLayout
                # Iterate over the buttons in the grid
                for button in child.children:
                    if isinstance(button, CustomButton):
                        # Check if the button corresponds to the end_id
                        if button.get_id() == end_id:

                            src = button.get_src()
                            print(src)
                            if ('Nothing' in src) or (src is None):
                                eat_identifier = False
                            else:
                                eat_identifier = True

                            # Iterate over the children of the CustomButton
                            for c in button.children:
                                if isinstance(c, CustomImage):
                                    c.source = original_source


        if eat_identifier:
            file_path = r"C:\Users\scorp\Desktop\Programmin\ChessGames\ChessMVC_PVC_Trial_1\Sound_Files\capture.mp3"
            subprocess.run(["start", "wmplayer", file_path], shell=True)
        else:
            file_path = r"C:\Users\scorp\Desktop\Programmin\ChessGames\ChessMVC_PVC_Trial_1\Sound_Files\move-self.mp3"
            subprocess.run(["start", "wmplayer", file_path], shell=True)

        Clock.schedule_once(self.fire, 0.01)  # Adjust the delay as needed



    def update(self):
        player = App.get_running_app().selected_player
        new_chess_board, False_movement = self.chess_model.action(player)  # Will set the move in action and return the new state of the chess_board
        self.chess_board = new_chess_board
        print('False Movement: ', False_movement)
        if (not False_movement) and (not None):
            start_id, end_id = self.chess_model.get_id_move()
            self.move(start_id, end_id)



    def fire(self, dt):

        move_identifier = False
        eat_identifier = False

        player = App.get_running_app().selected_player
        if player == 'white':
            ai_player = 'black'
        else:
            ai_player = 'white'
        new_chess_board = self.chess_model.ai(ai_player, self.chess_board)
        self.chess_board = new_chess_board

        start_id, end_id = self.chess_model.get_id_move()
        print(start_id, end_id)
        original_source = ''
        for child in self.children:
            if isinstance(child, GridLayout):  # Assuming the chess grid is a GridLayout
                # Iterate over the buttons in the grid
                for button in child.children:
                    if isinstance(button, CustomButton):
                        # Check if the button corresponds to the start_id
                        if button.get_id() == start_id:
                            # Iterate over the children of the CustomButton
                            for c in button.children:
                                if isinstance(c, CustomImage):
                                    original_source = copy.deepcopy(button.get_src())
                                    c.source = r'C:\Users\scorp\Desktop\Programmin\Chess Game\images\Nothing.png'
        for child in self.children:
            if isinstance(child, GridLayout):  # Assuming the chess grid is a GridLayout
                # Iterate over the buttons in the grid
                for button in child.children:
                    if isinstance(button, CustomButton):
                        if button.get_id() == end_id:
                            # Iterate over the children of the CustomButton

                            # Check if the button corresponds to the end_id
                            src = button.get_src()

                            if ('Nothing.png' in src) or (src is None) or (src == ''):
                                eat_identifier = False

                            else:
                                eat_identifier = True

                            for c in button.children:
                                if isinstance(c, CustomImage):
                                    c.source = original_source
        if eat_identifier:
            file_path = r"C:\Users\scorp\Desktop\Programmin\ChessGames\ChessMVC_PVC_Trial_1\Sound_Files\capture.mp3"
            subprocess.run(["start", "wmplayer", file_path], shell=True)
        else:
            file_path = r"C:\Users\scorp\Desktop\Programmin\ChessGames\ChessMVC_PVC_Trial_1\Sound_Files\move-self.mp3"
            subprocess.run(["start", "wmplayer", file_path], shell=True)




