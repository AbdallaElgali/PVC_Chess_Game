
class ChessModel:


    def __init__(self):
        self.log = []
        self.player = ''
        self.board = [[x for x in range(1, 9)],  # Row 1,2...8 respectively
             [x for x in range(9, 17)],
             [x for x in range(17, 25)],
             [x for x in range(25, 33)],
             [x for x in range(33, 41)],
             [x for x in range(41, 49)],
             [x for x in range(49, 57)],
             [x for x in range(57, 65)]]
        self.position_dict = {(i, j): str((i * 8) + j + 1) for i in range(8) for j in range(8)}
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

        self.Possible_moves = []  # List to get all possible moves, in case of checkmate
        self.checkmate_bol = False
        self.Terminal = False
        self.check_log = []
        self.selected_positions = []
        self.check = (False, '')

    def terminal(self, current_board):

        self.check_for_check(current_board)
        if self.check[0]:
            self.find_all_possible_moves(current_board)
            if len(self.Possible_moves) == 0:
                return True, self.check[1]
        elif not self.check[0]:
            self.reset_possible_moves()
            return False, ''

        return False, ''
    def reset_possible_moves(self):
        self.Possible_moves = []

    def select_position(self, position):
        self.selected_positions.append(position)

    def reset_positions(self):
        self.selected_positions = []

    def find_index(self, number):  # Function which returns a tuple representing the position of the piece in a hypothetical 2D 8x8 board

        for row_index, row in enumerate(self.board):
            if number in row:
                col_index = row.index(number)
                return row_index, col_index  # NOTE: the index is always 1 degree lower, hence 7 is actually 8 and so on
        return None

    def reverse_index(self, index, board):
        r, c = index

        for i, row in enumerate(board):
            if r == i:
                return row[c]

    def get_id_by_piece(self, piece, board):

        if not board:
            board = self.chess_board

        for key, value in board.items():
            if value == piece:
                return key
        return None  # Return None if the target value is not found in the dictionary

    def find_possible_moves_by_piece(self, piece_src, id):
        possible_moves = []
        possible_threats = []
        pos = self.find_index(id)

        for (src, curr_id, move) in self.Possible_moves:
            if (src == piece_src) and (id == curr_id):
                if 'pawn' in src:
                    all_moves = self.pawn_moves(pos, piece_src, id, self.chess_board)
                    all_threats = self.pawn_threats(pos, piece_src, self.chess_board, id)
                    if move in all_moves:
                        possible_moves.append(move)
                    elif move in all_threats:
                        possible_threats.append(move)
                else:
                    possible_moves.append(move)
        return possible_moves, possible_threats
    def fake_move(self, curr_pos, end_pos, board):
        current_board = dict(board)

        piece_pos = curr_pos

        for id, piece in current_board.items():
            if id == curr_pos:
                current_board[id] = ''
                piece_pos = piece
        for id, piece in current_board.items():
            if id == end_pos:
                current_board[id] = piece_pos

        return current_board
    def make_move(self, False_movement, curr_pos, end_pos, current_chess_board):

        piece_pos = curr_pos

        if False_movement:
            print('False Movement')
            return None

        for id, piece in current_chess_board.items():
            if id == curr_pos:
                current_chess_board[id] = ''
                piece_pos = piece
        for id, piece in current_chess_board.items():
            if id == end_pos:
                current_chess_board[id] = piece_pos

        self.check_for_check(current_chess_board)
        if self.check[0]:
            print(self.check)

        self.log.append((curr_pos, end_pos))

        if self.terminal(current_chess_board)[0]:
            if self.terminal(current_chess_board)[1] == 'black_king':
                print('WHITE WON!!!')
            else:
                print('BLACK WON!!!')

        return current_chess_board

    def moves_filter(self, id, moves, piece):  # Filters out false moves such as when a piece is pinned
        for move in moves:
            new_chess_board = self.fake_move(id, move, self.chess_board)
            self.check_for_check(new_chess_board)
            if self.check[0]:
                if 'white' in piece and 'white' in self.check[1]:
                    moves.remove(move)
                elif 'black' in piece and 'black' in self.check[1]:
                    moves.remove(move)
                self.check = (False, '')

        return moves
    def pawn_moves(self, pos, piece, curr_pos, current_board):  # (Position, piece_src, current_id_of_piece)

        pawn_id_list = [9, 10, 11, 12, 13, 14, 15, 16, 49, 50, 51, 52, 53, 54, 55, 56]

        temp = []
        indicies = []
        moves = []
        final = []

        id_position_list = []
        id_list = []
        for id, place in current_board.items():
            if place != '':
                id_list.append(id)

        row, col = pos

        black_move = (row + 1, col + 0)
        black_first_move = (row + 2, col)
        white_first_move = (row - 2, col)
        white_move = (row - 1, col)

        # Add all the ids from the id_list in tuple/board form
        for i, r in enumerate(self.board):
            for n, c in enumerate(r):
                if c in id_list:
                    id_position_list.append((i, n))

        for i, r in enumerate(self.board):
            for n, c in enumerate(r):
                if (i, n) == (row, col):

                    if ('white' in piece) and (white_move not in id_position_list):
                        moves.append(white_move)
                        if (curr_pos in pawn_id_list) and (white_first_move not in id_position_list):
                            moves.append(white_first_move)
                    elif ('black' in piece) and (black_move not in id_position_list):
                        moves.append(black_move)
                        if (curr_pos in pawn_id_list) and (black_first_move not in id_position_list):
                            moves.append(black_first_move)


        for i, r in enumerate(self.board):  # get a tuple of the position using the index of each block on the board
            for n, c in enumerate(r):
                indicies.append((i, n))

        for move in moves:
            if move in indicies:
                temp.append(move)

        for z, x in enumerate(self.board):
            for w, y in enumerate(x):
                if (z, w) in temp:
                    final.append(y)



        return final

    def pawn_threats(self, pos, piece, current_board, curr_pos):
        final = []
        temp = []
        indicies = []
        moves = []

        white_ids = []
        black_ids = []

        row, col = pos

        white_move = (row + 1, col + 1)
        white_move2 = (row + 1, col - 1)
        black_move = (row - 1, col - 1)
        black_move2 = (row - 1, col + 1)

        id_list = []
        src_list = []
        for id, place in current_board.items():
            if place != '':
                id_list.append(id)
                src_list.append(place)

        # Add all the ids from the id_list in tuple/board form
        for i, r in enumerate(self.board):
            for n, c in enumerate(r):
                if c in id_list:
                    c_index = id_list.index(c)
                    c_src = src_list[c_index]
                    if 'white' in c_src:
                        white_ids.append((i, n))
                    elif 'black' in c_src:
                        black_ids.append((i, n))

        # Find the row, col attributes of the end_pos

        for i, r in enumerate(self.board):
            for n, c in enumerate(r):
                if (i, n) == (row, col):
                    if 'white' in piece:
                        if black_move in black_ids:
                            #move = self.position_dict.get(black_move)
                            #new_chess_board = self.fake_move(curr_pos, move)
                            #check = self.check_for_check_by_king('white', new_chess_board)
                            #if not check:
                            moves.append(black_move)


                        elif black_move2 in black_ids:
                            moves.append(black_move2)


                    elif 'black' in piece:
                        if white_move in white_ids:
                            moves.append(white_move)
                        elif white_move2 in white_ids:
                            moves.append(white_move2)

        for i, r in enumerate(self.board):  # get a tuple of the position using the index of each block on the board
            for n, c in enumerate(r):
                indicies.append((i, n))

        for move in moves:
            if move in indicies:
                temp.append(move)

        for z, x in enumerate(self.board):
            for w, y in enumerate(x):
                if (z, w) in temp:
                    final.append(y)

        return final

    def horse_moves(self, position, curr_pos, piece, current_board):
        final = list()
        row, col = position
        indicies = []
        temp = []

        moves = [(row + 2, col + 1), (row - 2, col - 1), (row + 2, col - 1), (row - 2, col + 1), (row + 1, col - 2),
                 (row - 1, col - 2), (row + 1, col + 2), (row - 1, col + 2)]



        for i, r in enumerate(self.board):  # get a tuple of the position using the index of each block on the board
            for n, c in enumerate(r):
                indicies.append((i, n))

        for move in moves:
            if move in indicies:
                temp.append(move)

        for z, x in enumerate(self.board):
            for w, y in enumerate(x):
                if (z, w) in temp:
                    final.append(y)

        for move in final:
            if 'white' in piece and 'white' in current_board.get(move):
                final.remove(move)
            elif 'black' in piece and 'black' in current_board.get(move):
                final.remove(move)

        return final

    def appending_condition(self, id, first_img_src, current_board):

        src = current_board.get(id)

        if ('white' in src and 'black' in first_img_src) or ('white' in first_img_src and 'black' in src):
            return True, True
        elif ('white' in src and 'white' in first_img_src) or ('black' in src and 'black' in first_img_src):
            return False, True

        return True, False

    def bishop_moves(self, position, curr_pos, first_img_src, current_board):

        row, col = position
        moves = []
        board_indexes = []

        id_list = []
        for id, place in current_board.items():
            if place != '':
                id_list.append(id)

        for num in range(64):  # Loop to get all the indexes of the board
            board_index = self.find_index(num + 1)
            board_indexes.append(board_index)



        # Get all the moves possible for a bishop

        i0 = 1
        i1 = 1
        i2 = 1
        i3 = 1  # initializing the first value to be one

        for n in range(7):
            if (row + i0, col - i0) in board_indexes:
                id = self.reverse_index((row + i0, col - i0), self.board)
                moves.append(id)
                if id in id_list:
                    append, break_it = self.appending_condition(id, first_img_src, current_board)
                    if not append:
                        moves.remove(id)
                    if break_it is True:
                        break

                i0 += 1
        for n in range(7):
            if (row - i1, col + i1) in board_indexes:
                id = self.reverse_index((row - i1, col + i1), self.board)
                moves.append(id)

                if id in id_list:
                    append, break_it = self.appending_condition(id, first_img_src, current_board)
                    if not append:
                        moves.remove(id)
                    if break_it is True:
                        break

                i1 += 1
        for n in range(7):
            if (row + i2, col + i2) in board_indexes:
                id = self.reverse_index((row + i2, col + i2), self.board)
                moves.append(id)

                if id in id_list:
                    append, break_it = self.appending_condition(id, first_img_src, current_board)
                    if not append:
                        moves.remove(id)
                    if break_it is True:
                        break

                i2 += 1
        for n in range(7):
            if (row - i3, col - i3) in board_indexes:
                id = self.reverse_index((row - i3, col - i3), self.board)
                moves.append(id)

                if id in id_list:
                    append, break_it = self.appending_condition(id, first_img_src, current_board)
                    if not append:
                        moves.remove(id)
                    if break_it is True:
                        break

                i3 += 1


        return moves

    def castle_moves(self, curr_pos, position, first_img_src, current_board):
        final = []
        row, col = position

        id_list = []
        for id, place in current_board.items():
            if place != '':
                id_list.append(id)


        for row_index, inner_list in enumerate(self.board):  # Horizontal possible moves
            if row_index == row:
                if col > 0:
                    for x in range(col - 1, -1, -1):  # Left
                        append, break_it = self.appending_condition(inner_list[x], first_img_src, current_board)
                        final.append(inner_list[x])
                        if inner_list[x] in id_list:
                            if not append:
                                final.remove(inner_list[x])
                            if break_it:
                                break

                for y in range(col + 1, len(inner_list)):  # Right
                    append, break_it = self.appending_condition(inner_list[y], first_img_src, current_board)
                    final.append(inner_list[y])
                    if inner_list[y] in id_list:
                        if not append:
                            final.remove(inner_list[y])
                        if break_it:
                            break

        vertical_list = []

        for i in self.board:
            vertical_list.append(i[col])


        new_index = vertical_list.index(int(curr_pos))

        for x in range(new_index - 1, -1, -1):  # Up
            if vertical_list[x] in final:
                continue
            append, break_it = self.appending_condition(vertical_list[x], first_img_src, current_board)
            final.append(vertical_list[x])
            if vertical_list[x] in id_list:
                if not append:
                    final.remove(vertical_list[x])
                if break_it:
                    break

        for x in range(new_index + 1, len(vertical_list)):  # Down
            if vertical_list[x] in final:
                continue
            append, break_it = self.appending_condition(vertical_list[x], first_img_src, current_board)
            final.append(vertical_list[x])
            if vertical_list[x] in id_list:
                if not append:
                    final.remove(vertical_list[x])
                if break_it:
                    break



        return final

    def king_moves(self, pos, curr_pos, first_img_src, current_board):
        list = []
        temp = []
        indicies = []

        row, col = pos
        moves = [(row + 0, col + 1), (row + 0, col - 1), (row + 1, col + 0), (row - 1, col + 0), (row + 1, col + 1),
                 (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1)]

        for i, r in enumerate(self.board):  # get a tuple of the position using the index of each block on the board
            for n, c in enumerate(r):
                indicies.append((i, n))

        for move in moves:
            if move in indicies:
                temp.append(move)

        for z, x in enumerate(self.board):
            for w, y in enumerate(x):
                if (z, w) in temp:
                    append, _ = self.appending_condition(y, first_img_src, current_board)
                    if append:
                        list.append(y)


        return list

    def pawn(self, curr_pos, end_pos, piece, second_piece):


        pos = self.find_index(curr_pos)

        if not self.check[0]:
            moves = self.pawn_moves(pos, piece, curr_pos, self.chess_board)
            threats = self.pawn_threats(pos, piece, self.chess_board, curr_pos)
        else:
            moves, threats = self.find_possible_moves_by_piece(piece, curr_pos)

        moves = self.moves_filter(curr_pos, moves, piece)

        print('before: ', len(threats))
        threats = self.moves_filter(curr_pos, threats, piece)
        print('after: ', len(threats))

        if end_pos in moves:
            self.make_move(False, curr_pos, end_pos, self.chess_board)
            return False
        elif end_pos in threats:
            if ('white' in piece and 'black' in second_piece) or ('black' in piece and 'white' in second_piece):
                self.make_move(False, curr_pos, end_pos, self.chess_board)
                return False
            else:
                self.make_move(True, curr_pos, end_pos, self.chess_board)
                return True
        else:
            self.make_move(True, curr_pos, end_pos, self.chess_board)
            return True

    def horse(self, curr_pos, end_pos, piece, second_piece):

        if not self.check[0]:
            pos = self.find_index(curr_pos)
            moves = self.horse_moves(pos, curr_pos, piece, self.chess_board)
        else:
            moves, _ = self.find_possible_moves_by_piece(piece, curr_pos)

        moves = self.moves_filter(curr_pos, moves, piece)

        if end_pos in moves:
            if ('white' in piece and 'white' in second_piece) or ('black' in piece and 'black' in second_piece):
                self.make_move(True, curr_pos, end_pos, self.chess_board)
                return True
            else:
                self.make_move(False, curr_pos, end_pos, self.chess_board)
                return False
        else:
            self.make_move(True, curr_pos, end_pos, self.chess_board)
            return True


    def bishop(self, curr_pos, end_pos, piece, second_piece):

        if not self.check[0]:
            pos = self.find_index(curr_pos)
            moves = self.bishop_moves(pos, curr_pos, piece, self.chess_board)
        else:
            moves, _ = self.find_possible_moves_by_piece(piece, curr_pos)

        moves = self.moves_filter(curr_pos, moves, piece)

        if end_pos in moves:
            if ('white' in piece and 'white' in second_piece) or ('black' in piece and 'black' in second_piece):
                self.make_move(True, curr_pos, end_pos, self.chess_board)
                return True
            else:
                self.make_move(False, curr_pos, end_pos, self.chess_board)
                return False
        else:
            self.make_move(True, curr_pos, end_pos, self.chess_board)
            return True

    def castle(self, curr_pos, end_pos, piece, second_piece):

        if not self.check[0]:
            pos = self.find_index(curr_pos)
            moves = self.castle_moves(curr_pos, pos, piece, self.chess_board)
        else:
            moves, _ = self.find_possible_moves_by_piece(piece, curr_pos)

        moves = self.moves_filter(curr_pos, moves, piece)

        if end_pos in moves:
            if ('white' in piece and 'white' in second_piece) or ('black' in piece and 'black' in second_piece):
                self.make_move(True, curr_pos, end_pos, self.chess_board)
                return True
            else:
                self.make_move(False, curr_pos, end_pos, self.chess_board)
                return False
        else:
            self.make_move(True, curr_pos, end_pos, self.chess_board)
            return True


    def queen(self, curr_pos, end_pos, piece, second_piece):

        all_moves = []
        moves0 = []
        moves1 = []
        moves = []
        pos = self.find_index(curr_pos)

        if not self.check[0]:
            moves0 = self.castle_moves(curr_pos, pos, piece, self.chess_board)
            moves1 = self.bishop_moves(pos, curr_pos, piece, self.chess_board)
        else:
            moves, _ = self.find_possible_moves_by_piece(piece, curr_pos)

        for move in moves0:
            all_moves.append(move)
        for move in moves1:
            all_moves.append(move)

        all_moves = self.moves_filter(curr_pos, all_moves, piece)

        if not self.check[0]:
            if end_pos in all_moves:
                if ('white' in piece and 'white' in second_piece) or ('black' in piece and 'black' in second_piece):
                    self.make_move(True, curr_pos, end_pos, self.chess_board)
                    return True
                else:
                    self.make_move(False, curr_pos, end_pos, self.chess_board)
                    return False
            else:
                self.make_move(True, curr_pos, end_pos, self.chess_board)
                return True
        else:
            if end_pos in moves:
                if ('white' in piece and 'white' in second_piece) or ('black' in piece and 'black' in second_piece):
                    self.make_move(True, curr_pos, end_pos, self.chess_board)
                    return True
                else:
                    self.make_move(False, curr_pos, end_pos, self.chess_board)
                    return False
            else:
                self.make_move(True, curr_pos, end_pos, self.chess_board)
                return True
    def king(self, curr_pos, end_pos, piece, second_piece):

        pos = self.find_index(curr_pos)
        if not self.check[0]:
            moves = self.king_moves(pos, curr_pos, piece, self.chess_board)
        else:
            moves, _ = self.find_possible_moves_by_piece(piece, curr_pos)

        moves = self.moves_filter(curr_pos, moves, piece)

        if end_pos in moves:
            if ('white' in piece and 'white' in second_piece) or ('black' in piece and 'black' in second_piece):
                self.make_move(True, curr_pos, end_pos, self.chess_board)
                return True
            else:
                self.make_move(False, curr_pos, end_pos, self.chess_board)
                return False
        else:
            self.make_move(True, curr_pos, end_pos, self.chess_board)
            return True

    def get_all_moves(self, id, piece, current_board):

        moves = []
        start_id_and_moves = []  # A list of tuples, the id to move, the move itself and the source (src,id,move)
        pos = self.find_index(id)

        if 'pawn' in piece:

            normal_moves = self.pawn_moves(pos, piece, id, current_board)
            threat_moves = self.pawn_threats(pos, piece, current_board, id)
            moves = normal_moves + threat_moves
            for move in moves:
                start_id_and_moves.append((id, move))

        elif 'knight' in piece:
            moves = self.horse_moves(pos, id, piece, current_board)
            for move in moves:
                start_id_and_moves.append((id, move))

        elif 'bishop' in piece:
            moves = self.bishop_moves(pos, id, piece, current_board)
            for move in moves:
                start_id_and_moves.append((id, move))

        elif 'rook' in piece:
            moves = self.castle_moves(id, pos, piece, current_board)
            for move in moves:
                start_id_and_moves.append((id, move))

        elif 'queen' in piece:
            moves = self.castle_moves(id, pos, piece, current_board) + self.bishop_moves(pos, id, piece, current_board)
            for move in moves:
                start_id_and_moves.append((id, move))

        elif 'king' in piece:
            moves = self.king_moves(pos, id, piece, current_board)
            for move in moves:
                start_id_and_moves.append((id, move))

        return moves, start_id_and_moves

    def action(self, player):

        self.player = player
        self.check_for_check(self.chess_board)
        if self.check[0]:
            self.find_all_possible_moves(self.chess_board)

        last_piece = ''
        if self.log:
            last_move = self.log[-1]  # Check the last move
            last_piece = self.chess_board.get(last_move[1])


        curr_pos = self.selected_positions[0]
        end_pos = self.selected_positions[1]

        piece = self.chess_board.get(curr_pos)
        second_piece = self.chess_board.get(end_pos)

        if 'white' in last_piece and 'white' in piece:  # Make sure that no player does two moves in a row
            return self.chess_board, True
        elif 'black' in last_piece and 'black' in piece:
            return self.chess_board, True
        elif 'white' in player and 'black' in piece:
            return self.chess_board, True
        elif 'black' in player and 'white' in piece:
            return self.chess_board, True

        False_movement = True  # Initialize to true

        if piece is None:
            print('invalid move')
        elif 'pawn' in piece:
            False_movement = self.pawn(curr_pos, end_pos, piece, second_piece)
        elif 'knight' in piece:
            False_movement = self.horse(curr_pos, end_pos, piece, second_piece)
        elif 'bishop' in piece:
            False_movement = self.bishop(curr_pos, end_pos, piece, second_piece)
        elif 'rook' in piece:
            False_movement = self.castle(curr_pos, end_pos, piece, second_piece)
        elif 'queen' in piece:
            False_movement = self.queen(curr_pos, end_pos, piece, second_piece)
        elif 'king' in piece:
            False_movement = self.king(curr_pos, end_pos, piece, second_piece)

        return self.chess_board, False_movement

    def get_id_move(self):
        curr_pos = self.log[-1][0]
        end_pos = self.log[-1][1]

        return curr_pos, end_pos
    def gather_all_moves(self, player, current_board):
        """ Gathers all the position moves for a certain player (black or white) """

        all_moves = []
        start_id_moves = []
        if 'white' in player:
            for id, src in current_board.items():
                if 'white' in src:
                    _, start_id_moves = self.get_all_moves(id, src, current_board)
                for id_move_tup in start_id_moves:
                    all_moves.append(id_move_tup)
            return all_moves

        elif 'black' in player:
            for id, src in current_board.items():
                if 'black' in src:
                    _, start_id_moves = self.get_all_moves(id, src, current_board)
                for id_move_tup in start_id_moves:
                    all_moves.append(id_move_tup)
            return all_moves

    def ai_moves_filter(self, moves, player, board):  # Filters out false moves such as when a piece is pinned
        Filtered_list = []
        for id_move in moves:
            id = id_move[0]
            move = id_move[1]
            new_chess_board = self.fake_move(id, move, board)
            self.check_for_check(new_chess_board)
            if not self.check[0]:
                Filtered_list.append(id_move)
            else:
                if 'white' in player and 'black' in self.check[1]:
                    Filtered_list.append(id_move)
                elif 'black' in player and 'white' in self.check[1]:
                    Filtered_list.append(id_move)
                self.check = (False, '')

        return Filtered_list

    def eval(self, current_board, player):

        material_values = {
            'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 0  # Piece values
        }

        white_material = 0
        black_material = 0

        for piece in current_board.values():
            if 'white' in piece:  # White piece
                white_material += material_values.get(piece.split('_')[1], 0)
            elif 'black' in piece:  # Black piece
                black_material += material_values.get(piece.split('_')[1], 0)

        if 'black' in player:
            return black_material - white_material
        else:
            return white_material - black_material
    def minimax(self, current_board, depth, alpha, beta, max_player, player):

        if depth == 0 or self.terminal(current_board)[0]:
            return self.eval(current_board, player), None



        if 'black' in player:
            min_player = 'white'
        else:
            min_player = 'black'

        if max_player:
            best_val = float('-inf')
            best_move = None
            """ Get and filter all the moves """
            all_moves = []

            if not self.check[0]:
                all_moves = self.gather_all_moves(player, current_board)
                all_moves = self.ai_moves_filter(all_moves, player, current_board)

            elif self.check[0]:
                self.find_black_possible_moves(current_board)  # Considering black player
                for src, id, move in self.Possible_moves:
                    all_moves.append((id, move))

            unique_moves = list(set(all_moves))
            print("ALL_MOVES: ", unique_moves)
            """ Go through each move """

            for id_move in unique_moves:

                new_state = self.fake_move(id_move[0], id_move[1], current_board)
                evaluation, _ = self.minimax(new_state, depth - 1, alpha, beta, False, player)

                if evaluation > best_val:
                    best_val = evaluation
                    best_move = id_move

                best_val = max(best_val, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

            return best_val, best_move

        else:
            worst_val = float('inf')
            worst_move = None
            """ Get and filter all the moves """

            all_moves = []

            if not self.check[0]:
                all_moves = self.gather_all_moves(min_player, current_board)  # ASSUMING that the max_player is always black
                all_moves = self.ai_moves_filter(all_moves, min_player, current_board)

            elif self.check[0]:
                if min_player == 'white':
                    self.find_white_possible_moves(current_board)
                else:
                    self.find_black_possible_moves(current_board)

                for src, id, move in self.Possible_moves:
                    all_moves.append((id, move))

            unique_moves = list(set(all_moves))

            """ Go through each move """

            for id_move in unique_moves:
                new_state = self.fake_move(id_move[0], id_move[1], current_board)
                evaluation, _ = self.minimax(new_state, depth - 1, alpha, beta, True, player)
                worst_val = min(worst_val, evaluation)

                if evaluation < worst_val:
                    worst_val = evaluation
                    worst_move = id_move

                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

            return worst_val, worst_move




    def ai(self, player, current_board):

        if self.terminal(current_board)[0]:
            if player not in self.check[1]:
                print("YOU WON DADDY!!!")
        original_state = dict(current_board)
        best_eval, id_move = self.minimax(original_state, 2, float('-inf'), float('inf'), True, player)


        new_chess_board = self.make_move(False, id_move[0], id_move[1], current_board)
        return new_chess_board

    def find_white_possible_moves(self, current_chess_board):
        all_moves = []
        for id, src in current_chess_board.items():
            if 'white' in src:
                moves, _ = self.get_all_moves(id, src, current_chess_board)
                for move in moves:
                    current_board = self.fake_move(id, move, current_chess_board)
                    self.check_for_check(current_board)
                    if not self.check[0]:
                        all_moves.append((src, id, move))  # all_moves.append((src, id, move))
        self.Possible_moves = all_moves
    def find_black_possible_moves(self, current_chess_board):
        all_moves = []
        for id, src in current_chess_board.items():
            if 'black' in src:
                moves, _ = self.get_all_moves(id, src, current_chess_board)
                for move in moves:
                    current_board = self.fake_move(id, move, current_chess_board)
                    self.check_for_check(current_board)
                    if not self.check[0]:
                        all_moves.append((src, id, move))

        self.Possible_moves = all_moves

    def find_all_possible_moves(self, current_chess_board):
        """ Implement a function which gets a list of tuples (piece_src, curr_id, end_id) with all possible moves which can take the king out of the check """

        _, checked_king = self.check

        if 'white' in checked_king:
            self.find_white_possible_moves(current_chess_board)
        elif 'black' in checked_king:
            self.find_black_possible_moves(current_chess_board)

        print(self.Possible_moves)

    def find_threats(self, id, piece, current_board):
        threats = []
        pos = self.find_index(id)

        if 'pawn' in piece:
            threats = self.pawn_threats(pos, piece, current_board, id)

        elif 'knight' in piece:
            threats = self.horse_moves(pos, id, piece, current_board)

        elif 'bishop' in piece:
            threats = self.bishop_moves(pos, id, piece, current_board)

        elif 'rook' in piece:
            threats = self.castle_moves(id, pos, piece, current_board)

        elif 'queen' in piece:
            threats = self.castle_moves(id, pos, piece, current_board) + self.bishop_moves(pos, id, piece, current_board)

        elif 'king' in piece:
            threats = self.king_moves(pos, id, piece, current_board)

        return threats

    def all_threats(self, board, player):

        if not board:
            board = self.chess_board

        all_white_threats = []
        all_black_threats = []

        if player == 'white':
            for id, piece in board.items():
                if 'white' in piece:
                    piece_threats = self.find_threats(id, piece, board)
                    for threat in piece_threats:
                        all_white_threats.append(threat)
        elif player == 'black':
            for id, piece in board.items():
                if 'black' in piece:
                    piece_threats = self.find_threats(id, piece, board)
                    for threat in piece_threats:
                        all_black_threats.append(threat)
        else:
            for id, piece in board.items():
                if 'white' in piece:
                    piece_threats = self.find_threats(id, piece, board)
                    for threat in piece_threats:
                        all_white_threats.append(threat)
                if 'black' in piece:
                    piece_threats = self.find_threats(id, piece, board)
                    for threat in piece_threats:
                        all_black_threats.append(threat)

        return all_white_threats, all_black_threats

    def check_for_check(self, board):

        white_threats, black_threats = self.all_threats(board, '')

        white_king_id = self.get_id_by_piece('white_king', board)
        black_king_id = self.get_id_by_piece('black_king', board)

        if black_king_id in white_threats:
            self.check = True, 'black_king'
        elif white_king_id in black_threats:
            self.check = True, 'white_king'
        else:
            self.check = False, ''

    def check_for_check_by_king(self, king, board):

        if 'white' in king:
            white_king_id = self.get_id_by_piece('white_king', board)
            _, black_threats = self.all_threats(board, 'black')
            if white_king_id in black_threats:
                return True
            else:
                return False
        elif 'black' in king:
            black_king_id = self.get_id_by_piece('black_king', board)
            white_threats, _ = self.all_threats(board, 'white')
            if black_king_id in white_threats:
                return True
            else:
                return False
