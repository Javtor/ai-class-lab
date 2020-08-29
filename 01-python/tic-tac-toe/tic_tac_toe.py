import re
from random import randint

_PLAYER = "player"
_MACHINE = "machine"

_PLAYER_SYMBOL = "x"
_MACHINE_SYMBOL = "o"


class TicTacToeGame():
    def __init__(self):
        self.board = [None] * 9
        self.turn = _PLAYER
        self.is_game_over = False
        self.winner = None

    def is_over(self):  # TODO: Finish this function by adding checks for a winning game (rows, columns, diagonals)
        over = False
        winning_symbol = ""
        def check_winning(
            x, y, z): return self.board[x] is not None and self.board[x] == self.board[y] == self.board[z]
        def get_winning(idx, ws=winning_symbol,
                        over=over): return self.board[idx] if ws == '' and over else ws

        jump_down = 3
        jump_right = 1

        # Diagonals
        over = over or check_winning(
            0, 0+jump_down+jump_right, 0+jump_down*2+jump_right*2)
        winning_symbol = get_winning(0, winning_symbol, over)

        over = over or check_winning(
            2, 2+jump_down+jump_right*-1, 2+jump_down*2+jump_right*(-2))
        winning_symbol = get_winning(2, winning_symbol, over)

        # Rows and columns
        for row in range(3):
            i = row*3
            over = over or check_winning(i, i+jump_right, i+jump_right*2)
            winning_symbol = get_winning(i, winning_symbol, over)

        for i in range(3):
            over = over or check_winning(i, i+jump_down, i+jump_down*2)
            winning_symbol = get_winning(i, winning_symbol, over)

        if over:
            self.winner = _MACHINE if winning_symbol == _MACHINE_SYMBOL else _PLAYER

        return over or self.board.count(None) == 0

    def play(self):
        if self.turn == _PLAYER:
            self.player_turn()
            self.turn = _MACHINE
        else:
            self.machine_turn()
            self.turn = _PLAYER

    def player_choose_cell(self):
        print("Input empty cell bewtween 0 and 8")

        player_cell = input().strip()
        match = re.search("\d", player_cell)

        if not match:
            print("Input is not a number, please try again")

            return self.player_choose_cell()

        player_cell = int(player_cell)

        if self.board[player_cell] is not None:
            print("Cell is already taken, try again")

            return self.player_choose_cell()

        return player_cell

    def player_turn(self):
        chosen_cell = self.player_choose_cell()

        self.board[chosen_cell] = _PLAYER_SYMBOL

    def machine_turn(self):
        # The result of this function should be that self.board now has one more random cell occupied
        valid_cells = [i for i, cell in enumerate(self.board) if cell is None]
        if(len(valid_cells)):
            idx = randint(0, len(valid_cells)-1)
            self.board[valid_cells[idx]] = _MACHINE_SYMBOL

    def format_board(self):
        board = ''
        for i in range(9):
            car = ' '
            if self.board[i] is not None:
                car = self.board[i]
            board += car
            if i % 3 == 2:
                if i != 8:
                    board += '\n'
            else:
                board += '|'
        return board

    def print(self):
        print("Player turn:" if self.turn == _MACHINE else "Machine turn:")
        print(self.format_board())
        print()

    def print_result(self):
        # TODO: Implement this function in order to print the result based on the self.winner
        if(self.winner is not None):
            print(f"The winner is {self.winner}")
        else:
            print("It's a draw")
        pass
