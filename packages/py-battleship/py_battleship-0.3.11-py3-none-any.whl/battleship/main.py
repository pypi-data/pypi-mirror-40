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

dash = '-' * 90


def print_statistics(game):
    print(_('\nPoints: '), game.points, end="     ")
    print(_('Shots Available: '), game.shots, end="     ")
    print(_('Time elapsed: '), '{} sec'.format(int(game.time_elapsed)), end="\n")
    print(dash)


def print_board(game):
    os.system('clear')
    print_statistics(game)

    # Table Header
    print('|', end='')
    print('{:^3}'.format('-'), end='|')
    for i in range(game.COLS):
        print('{:^4}'.format(i), end='|')

    print()
    print(dash)

    # Table Body
    for i, row in enumerate(game.matrix):
        print('|', end='')
        print('{:^3}'.format(NUMBERS[i].upper()), end="|")
        for col in row:
            if col['shooted']:
                if not col['ship']:
                    print('{:^4}'.format('O'), end="|")
                else:
                    print('{:^4}'.format(col['ship'].initials), end="|")
            else:
                print('{:^4}'.format('.'), end="|")

        print()

    print(dash)
    print()
    print(_('Labels'))
    for i, ship in enumerate(game.ships):
        data_ship = (
            _(ship.name.title()),
            ship.initials,
            ship.length,
            ship.hits,
            _('yes') if ship.sink else _('no')
        )
        if i == 0:
            print(dash)
            label_header = (_('Ship'), _('Initials'), _('Size'), _('Hits'), _('sunk'))
            print('{:<13}{:^11}{:^8}{:^8}{:^10}'.format(*label_header))
            print(dash)
            print('{:<13}{:^11}{:^8}{:^8}{:^10}'.format(*data_ship))
        else:
            print('{:<13}{:^11}{:^8}{:^8}{:^10}'.format(*data_ship))

    print()
    print(dash)


def print_ship_hit(ship_hit, game):
    os.system('clear')
    print_statistics(game)

    print('\n\n\n\n')
    if ship_hit.sink:
        message = _('You Destroy a {}').format(ship_hit.name.title())
    else:
        message = _('You Hit a {}').format(ship_hit.name.title())

    print('{:^88}'.format(message), end='\n')

    print('\n\n\n\n')
    input(_("Press Enter to continue..."))


def print_status(game, win=False):
    os.system('clear')
    print(_('\nPoints: '), game.points, end="     ")
    print(_('Lost Shots: '), game.lost_shot, end="     ")
    print(_('Right Shots: '), game.right_shot, end="     ")
    print(_('Shots Missing: '), game.shots, end="\n")
    print(dash)
    print(_('Sunken Ships: '), game.sunken_ships, end="     ")
    print(_('Missing Ships: '), game.total_ships - game.sunken_ships, end="   ")
    print(_('Time elapsed: {} sec').format(int(game.time_elapsed)), end="\n")
    print(dash)

    if win:
        print('{:^88}'.format(_('You WIN !!!!!')), end='\n')
    else:
        print('{:^88}'.format(_('You Lost !!!!!')), end='\n')

    print(dash)
    for s in game.ships:
        print(_('<{}> \t Sunk: {} \t| Hits: {}').format(
            s.name.title(),
            _('yes') if s.sink else _('no'),
            s.hits
        ))

    print(dash)


def main():
    game = Game()
    print_board(game)

    while True:
        while True:
            try:
                print(_('Press CTRL+C to exit ...'))
                result = input(_('Choose your coordinate using one LETTER from A to Q and one NUMBER from 0 to 16. \n'
                                 'Ex: a1, b15, c10 and etc... \n\nCoordinates: ')).strip()

                x = int(LETTERS[result[0].lower()])
                y = int(result[1:].strip())

                if (x > 16 and x < 0) or (y > 16 and y < 0):
                    raise InvalidPosition()

                is_valid, ship = game.play(x, y)
                if is_valid:
                    print_ship_hit(ship, game)
                    break

                print_board(game)
                if game.is_finished():
                    sys.exit(print_status(game, win=True))

                if game.end_game():
                    sys.exit(print_status(game))
            except Exception as exc:
                os.system('clear')
                input(_('\n\n\n\t\t\tYou can only use letters with numbers. Ex: a1, c10, etc...'))
                print_board(game)
            except KeyboardInterrupt:
                sys.exit(print_status(game))

        print_board(game)
