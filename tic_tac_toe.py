import pickle
import random
import string


PLAYER_SIGN = 'x'
COMPUTER_SIGN = 'o'


class TicTacToeException(Exception):
    pass


class TicTacToeWrongIndexError(TicTacToeException):
    pass


class TicTacToeNonFreeCellError(TicTacToeException):
    pass


class TicTacToe:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.win_size = min(self.n, self.m)
        self.field = [[' '] * self.m for _ in range(self.n)]

        self.letters = string.ascii_letters[:self.n]
        self.numbers = ' ' + ''.join(map(str, range(1, self.m + 1)))
        self.letter_to_idx = {
            letter: idx
            for idx, letter in enumerate(self.letters)
        }
        self.idx_to_letter = {v: k for k, v in self.letter_to_idx.items()}

    def print_board(self):
        print(self.numbers)
        for letter, line in zip(self.letters, self.field):
            print(letter + ''.join(line))

    def _get_free_places(self):
        free_places = []
        for idx in range(self.n):
            for jdx in range(self.m):
                if self.field[idx][jdx] == ' ':
                    free_places.append((idx, jdx))
        return free_places

    def player_step(self, row, column):
        if row not in self.letter_to_idx:
            raise TicTacToeWrongIndexError('Wrong row letter')

        if column < 1 or column > self.m:
            raise TicTacToeWrongIndexError('Wrong column index')

        idx = self.letter_to_idx[row]
        jdx = column - 1

        if self.field[idx][jdx] != ' ':
            raise TicTacToeNonFreeCellError("Cell isn't free")
        self.field[idx][jdx] = PLAYER_SIGN

    def computer_step(self):
        # choose step
        free_places = self._get_free_places()
        idx, jdx = random.choice(free_places)

        # make step
        self.field[idx][jdx] = COMPUTER_SIGN

        # return step
        row, column = self.idx_to_letter[idx], jdx + 1
        return f'{row}{column}'

    def _check_win(self, check_sign):
        # horizontal line
        for idx in range(self.n):
            for jdx in range(self.m - self.win_size + 1):
                for k in range(self.win_size):
                    if self.field[idx][jdx + k] != check_sign:
                        break
                else:
                    return True

        # vertical line
        for jdx in range(self.m):
            for idx in range(self.n - self.win_size + 1):
                for k in range(self.win_size):
                    if self.field[idx + k][jdx] != check_sign:
                        break
                else:
                    return True

        # left bottom - right top
        for idx in range(self.win_size - 1, self.n):
            for jdx in range(self.m - self.win_size + 1):
                for k in range(self.win_size):
                    if self.field[idx - k][jdx + k] != check_sign:
                        break
                else:
                    return True

        # left top - right bottom
        for idx in range(self.n - self.win_size + 1):
            for jdx in range(self.m - self.win_size + 1):
                for k in range(self.win_size):
                    if self.field[idx + k][jdx + k] != check_sign:
                        break
                else:
                    return True

        return False

    def check_user_win(self):
        return self._check_win(PLAYER_SIGN)

    def check_computer_win(self):
        return self._check_win(COMPUTER_SIGN)

    def check_draw(self):
        return len(self._get_free_places()) == 0

    def save_game(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load_game(cls, filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)
