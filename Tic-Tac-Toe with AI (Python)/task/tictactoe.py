import random
from itertools import chain
import copy


class Move:
    def __init__(self, score=None, x=None, y=None):
        self.score = score
        self.x = x
        self.y = y


class TicTacToe:
    player_options = ['easy', 'medium', 'hard', 'user']

    def __init__(self, player1, player2):
        functions = {'easy': self.get_coord_ai_easy,
                     'medium': self.get_coord_ai_medium,
                     'hard': self.get_coord_ai_hard,
                     'user': self.get_coord}

        self._board = [[' '] * 3 for _ in range(3)]
        self._marker = 'X'
        self._player1 = functions[player1]
        self._player2 = functions[player2]
        self._play_func = self._player1

    def place_marker(self, y, x):
        self._board[y][x] = self._marker
        if self._marker == 'O':
            self._marker = 'X'
            self._play_func = self._player1
            return 'O'
        else:
            self._marker = 'O'
            self._play_func = self._player2
            return 'X'

    def print_board(self):
        print('---------')
        for y in range(3):
            print('|', ' '.join(self._board[y]), '|')
        print('---------')

    def check_game(self, marker):
        if TicTacToe.is_winning(self._board, marker):
            return f'{marker} wins'

        # look for any remaining empty spaces
        if len(TicTacToe.find_empty_spaces(self._board)) == 0:
            return 'Draw'
        print('Game not finished')
        return None

    def get_coord(self):
        while True:
            try:
                y, x = [int(v) for v in input('Enter the coordinates:').split(' ')]
                if not (0 < y < 4 and 0 < x < 4):
                    print('Coordinates should be from 1 to 3!')
                elif self._board[y - 1][x - 1] != ' ':
                    print('This cell is occupied! Choose another one!')
                else:
                    return y - 1, x - 1
            except ValueError:
                print('You should enter numbers!')

    def find_random(self):
        empty_spaces = TicTacToe.find_empty_spaces(self._board)
        return random.choice(empty_spaces)

    def find_winning_move(self, marker):
        all_directions = TicTacToe.get_all_directions(self._board, marker, 2)
        if len(all_directions) > 0:
            empty_spaces = list(filter(lambda c: c[2] == ' ', all_directions[0]))
            if len(empty_spaces) > 0:
                y, x, _ = empty_spaces[0]
                return y, x
        return None

    def get_coord_ai_easy(self):
        print('Making move level "easy"')
        return self.find_random()

    def get_coord_ai_medium(self):
        print('Making move level "medium"')
        return self.find_winning_move(self._marker) or self.find_winning_move(
            TicTacToe.opposite_marker(self._marker)) or self.find_random()

    def get_coord_ai_hard(self):
        print('Making move level "hard"')
        move = TicTacToe.minimax(self._board, self._marker, self._marker)
        return move.y, move.x

    def play_game(self):
        try:
            game_result = ''
            self.print_board()
            while not game_result:
                y, x = self._play_func()
                marker = self.place_marker(y, x)
                self.print_board()
                game_result = self.check_game(marker)
            print(game_result)
        except Exception as e:
            print(e)

    @staticmethod
    def opposite_marker(marker):
        return 'O' if marker == 'X' else 'X'

    @staticmethod
    def get_all_directions(board, marker, count):
        # rows
        all_directions = [[(y, x, board[y][x]) for x in range(3)] for y in range(3)]
        # columns
        all_directions.extend([[(y, x, board[y][x]) for y in range(3)] for x in range(3)])
        # diagonals
        all_directions.append([(1, 1, board[1][1]), (0, 0, board[0][0]), (2, 2, board[2][2])])
        all_directions.append([(1, 1, board[1][1]), (0, 2, board[0][2]), (2, 0, board[2][0])])
        return list(filter(lambda d: [c[2] for c in d].count(marker) == count, all_directions))

    @staticmethod
    def is_winning(board, marker):
        all_directions = TicTacToe.get_all_directions(board, marker, 3)
        return len(all_directions) > 0

    @staticmethod
    def find_empty_spaces(board):
        return list(
            chain.from_iterable([[(y, x) for y in range(3) if board[y][x] == ' '] for x in range(3)]))

    @staticmethod
    def minimax(board, player_marker, current_player):
        available_spots = TicTacToe.find_empty_spaces(board)  # List((y,x))

        # checks for the terminal states such as win, lose, and tie and returning a value accordingly
        if TicTacToe.is_winning(board, TicTacToe.opposite_marker(player_marker)):
            return Move(-10)
        elif TicTacToe.is_winning(board, player_marker):
            return Move(10)
        elif len(available_spots) == 0:
            return Move(0)

        moves = []

        best_score = 10 if current_player == player_marker else -10
        # loop through available spots
        for (y, x) in available_spots:
            # create an object for each spot and store the coords of that spot
            move = Move(x=x, y=y)

            # set the empty spot to the current player
            new_board = copy.deepcopy(board)
            new_board[y][x] = current_player

            # recursively call minimax to see if that move results in a win
            move.score = TicTacToe.minimax(new_board, player_marker, TicTacToe.opposite_marker(current_player)).score
            # short circuit if we find a winning move
            if move.score == best_score:
                return move
            moves.append(move)

        # if it is players turn, loop over the moves and choose the move with the highest score
        if current_player == player_marker:
            best_move = Move(-10000)
            for move in moves:
                if move.score > best_move.score:
                    best_move = move

        else:  # else loop over the moves and choose the move with the lowest score
            best_move = Move(10000)
            for move in moves:
                if move.score < best_move.score:
                    best_move = move

        # return the chosen move (object) from the array to the higher depth
        return best_move


def main():
    cmd = input('Input command:')
    while cmd != 'exit':
        try:
            start, player1, player2 = cmd.split(' ')
            assert start == 'start'
            assert player1 in TicTacToe.player_options
            assert player2 in TicTacToe.player_options
            TicTacToe(player1, player2).play_game()
        except (ValueError, AssertionError):
            print('Bad parameters!')
        cmd = input('Input command:')


if __name__ == '__main__':
    main()
