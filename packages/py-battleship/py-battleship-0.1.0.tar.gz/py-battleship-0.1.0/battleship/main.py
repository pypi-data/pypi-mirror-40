import os

from .battleship import Game


def print_board(board, points, shots, time_elapsed):
    os.system('clear')
    print('\nPoints: ', points, end="     ")
    print('Shots Available: ', shots, end="     ")
    print('Time elapsed: {} sec'.format(int(time_elapsed)), end="\n")
    for row in board.matrix:
        print('| ', end='')
        for col in row:
            if col['shooted']:
                if not col['ship']:
                    print('O ', end=" | ")
                else:
                    print(col['ship'].initials, end=" | ")
            else:
                print('. ', end=" | ")

        print()

    print('-' * 85)
    for ship in board.ships:
        print('{}: size: {} | initials: {} \t|'.format(
            ship.name.title(),
            ship.length,
            ship.initials,
        ))

    print('-' * 85)


def print_ship_hit(ship_hit, points, shots, time_elapsed):
    os.system('clear')
    print('\nPoints: ', points, end="     ")
    print('Shots Available: ', shots, end="     ")
    print('Time elapsed: {} sec'.format(int(time_elapsed)), end="\n")
    print('-' * 85)
    print('\n\n\n\n')
    if ship_hit.sink:
        print('\t\t\t You Destroy a {}'.format(ship_hit.name.title()))
    else:
        print('\t\t\t You Hit a {}'.format(ship_hit.name.title()))

    print('\n\n\n\n')
    input("Press Enter to continue...")


def print_status(board, points, shots, time_elapsed):
    os.system('clear')
    print('\nPoints: ', points, end="     ")
    print('Shots Available: ', shots, end="     ")
    print('Time elapsed: {} sec'.format(int(time_elapsed)), end="\n")
    print('-' * 85)
    print('Sunken Ships: ', board.sunken_ships, end="     ")
    print('Missing Ships: ', board.total_ships - board.sunken_ships, end="\n")
    print('-' * 85)
    for s in board.ships:
        print('{}: sunk: {} \t|'.format(
            s.name.title(),
            'yes' if s.sink else 'no',
        ))

    print('-' * 85)


def main():
    game = Game()
    print_board(game.board, game.points, game.shots, game.time_elapsed)
    while True:
        while True:
            try:
                result = input('\ncoordinates: ').strip()
                if ',' in result:
                    splitter = ','
                elif ' ' in result:
                    splitter = ' '
                else:
                    splitter = ''
                x, y = [int(c) for c in result.split(splitter)]

                is_valid, ship = game.play(x, y)
                if is_valid:
                    print_ship_hit(ship, game.points, game.shots, game.time_elapsed)
                    break
                print_board(game.board, game.points, game.shots, game.time_elapsed)
            except ValueError:
                os.system('clear')
                input('\n\n\n\t\t\tYou can only use numbers or you miss one coordinate')
                print_board(game.board, game.points, game.shots, game.time_elapsed)

        print_board(game.board, game.points, game.shots, game.time_elapsed)
        if game.end_game():
            break

    print_status(game.board, game.points, game.shots, game.time_elapsed)
