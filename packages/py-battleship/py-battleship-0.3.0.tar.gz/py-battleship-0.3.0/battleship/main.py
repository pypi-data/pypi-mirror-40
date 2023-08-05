#!/usr/bin/env python
# encoding: utf-8
import os
import sys
from string import ascii_lowercase

from .battleship import Game
from .exceptions import InvalidPosition
from . import language

_ = language.gettext

LETTERS = {letter: str(index) for index, letter in enumerate(ascii_lowercase, start=0)}
NUMBERS = {index: letter for index, letter in enumerate(ascii_lowercase, start=0)}


def print_board(game):
    os.system('clear')
    print(_('\nPoints: '), game.points, end="     ")
    print(_('Shots Available: '), game.shots, end="     ")
    print(_('Time elapsed: '), '{} sec'.format(int(game.time_elapsed)), end="\n")
    print('-' * 90)
    # Table Header
    print('| ', end='')
    print('{:<3}'.format('-'), end='')
    for i in range(game.COLS):
        print('| ', end='')
        print('{:<3}'.format(i), end='')
    print('| ', end='\n')
    print('-' * 90)
    # Table Body
    for i, row in enumerate(game.matrix):
        print('| ', end='')
        print('{:<2}'.format(NUMBERS[i]), end=" | ")
        for col in row:
            if col['shooted']:
                if not col['ship']:
                    print('{:<2}'.format('O'), end=" | ")
                else:
                    print('{:<2}'.format(col['ship'].initials), end=" | ")
            else:
                print('{:<2}'.format('.'), end=" | ")

        print()

    print('-' * 90)
    print(_('Labels'))
    print('-' * 7)
    for ship in game.ships:
        text = _('<{}> \t Initials: {} \t| Size: {} \t| Hits: {} | sunk: {}')
        print(text.format(
            ship.name.title(),
            ship.initials,
            ship.length,
            ship.hits,
            'yes' if ship.sink else 'no'
        ))

    print()
    print('-' * 90)


def print_ship_hit(ship_hit, points, shots, time_elapsed):
    os.system('clear')
    print(_('\nPoints: '), points, end="     ")
    print(_('Shots Available: '), shots, end="     ")
    print(_('Time elapsed: '), '{} sec'.format(int(time_elapsed)), end="\n")
    print('-' * 90)
    print('\n\n\n\n')
    if ship_hit.sink:
        print(_('\t\t\t You Destroy a {}').format(ship_hit.name.title()))
    else:
        print(_('\t\t\t You Hit a {}').format(ship_hit.name.title()))

    print('\n\n\n\n')
    input(_("Press Enter to continue..."))


def print_status(game):
    os.system('clear')
    print('\nPoints: ', game.points, end="     ")
    print('Lost Shots: ', game.lost_shot, end="     ")
    print('Right Shots: ', game.lost_shot, end="     ")
    print('Shots Missing: ', game.shots, end="\n")
    print('-' * 90)
    print('Sunken Ships: ', game.sunken_ships, end="     ")
    print('Missing Ships: ', game.total_ships - game.sunken_ships, end="   ")
    print('Time elapsed: {} sec'.format(int(game.time_elapsed)), end="\n")
    print('-' * 90)
    for s in game.ships:
        print('<{}> \t Sunk: {} \t| Hits: {}'.format(
            s.name.title(),
            'yes' if s.sink else 'no',
            s.hits
        ))

    print('-' * 90)


def main():
    game = Game()
    print_board(game)

    while True:
        while True:
            try:
                print(_('Press CTRL+C to exit ...'))
                result = input(_('Choose your coordinates. Ex: a1, b15: c10 \n\nCoordinates: ')).strip()

                x = int(LETTERS[result[0].lower()])
                y = int(result[1:].strip())

                if (x > 16 and x < 0) or (y > 16 and y < 0):
                    raise InvalidPosition()

                is_valid, ship = game.play(x, y)
                if is_valid:
                    print_ship_hit(ship, game.points, game.shots, game.time_elapsed)
                    break

                print_board(game)

                if game.end_game():
                    sys.exit(print_status(game))

            except Exception as exc:
                os.system('clear')
                print(str(exc))
                input(_('\n\n\n\t\t\tYou can only use letters with numbers. Ex: a1, c10, etc...'))
                print_board(game)
            except KeyboardInterrupt:
                sys.exit(print_status(game))

        print_board(game)

main()
