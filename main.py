import os
from argparse import ArgumentParser
from tic_tac_toe import TicTacToe, TicTacToeException


DUMP_FILE = 'tic_tac_toe.dat'


if __name__ == '__main__':
    parser = ArgumentParser(description='TicTacToe game')
    parser.add_argument('-n', type=int, choices=range(1, 10), help='the first size')
    parser.add_argument('-m', type=int, choices=range(1, 10), help='the second size')
    args = parser.parse_args()

    # create or load the game board
    board = None
    if os.path.exists(DUMP_FILE):
        while True:
            answer = input('You have got the saved game. Do you want to continue it? Type y or n: ')
            answer = answer.strip().lower()

            if answer not in ('y', 'n'):
                continue

            if answer == 'y':
                board = TicTacToe.load_game(DUMP_FILE)

            os.remove(DUMP_FILE)
            break

    if board is None:
        board = TicTacToe(args.n, args.m)
    board.print_board()

    # game loop
    while True:

        # player step
        user_step = input('Your next step: ').lower().replace(' ', '')
        if user_step == 'save':
            board.save_game(DUMP_FILE)
            print('The current game was saved')
            break

        row, column = user_step[:1], user_step[1:]
        if not row.isalpha():
            print('The row should be the letter')
            continue

        if not column.isdigit():
            print('The column should be the number')
            continue
        column = int(column)

        try:
            board.player_step(row, column)
        except TicTacToeException as e:
            print(e)
            continue
        board.print_board()

        # check the finish
        if board.check_user_win():
            print('You win!')
            break
        elif board.check_draw():
            print('Draw!')
            break

        # computer step
        computer_step = board.computer_step()
        print(f'Computer step: {computer_step}')
        board.print_board()

        # check the finish
        if board.check_computer_win():
            print('You lose!')
            break
        elif board.check_draw():
            print('Draw!')
            break
