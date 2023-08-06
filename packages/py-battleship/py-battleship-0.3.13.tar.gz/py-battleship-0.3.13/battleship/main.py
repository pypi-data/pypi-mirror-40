#!/usr/bin/env python
# encoding: utf-8
import os
import sys

from .battleship import Game
from .constants import NUMBERS
from .exceptions import InvalidCoordinate, InvalidFormat
from .language import language

_ = language.gettext

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


def print_error_message(message):
    os.system('clear')
    print(dash)
    print('\n\n\n\n')

    print('{:^88}'.format(message), end='\n')

    print('\n\n\n\n')
    print(dash)
    input(_("Press Enter to continue..."))



def print_status(game, win=False):
    os.system('clear')
    print(_('\nPoints: '), game.points, end="     ")
    print(_('Lost Shots: '), game.lost_shot, end="     ")
    print(_('Right Shots: '), game.right_shot, end="     ")
    print(_('Shots Missing: '), game.shots, end="\n")
    print(dash)

    if win:
        message = _('You WIN !!!!!')
    else:
        message = _('You Lost !!!!!')

    print('\n\n\n{:^90}'.format(message), end='\n\n\n')
    print(dash)
    print(_('Sunken Ships: '), game.sunken_ships, end="     ")
    print(_('Missing Ships: '), game.total_ships - game.sunken_ships, end="   ")
    print(_('Time elapsed: {} sec').format(int(game.time_elapsed)), end="\n")

    for i, ship in enumerate(game.ships):
        data_ship = (
            _(ship.name.title()),
            ship.hits,
            _('yes') if ship.sink else _('no')
        )
        if i == 0:
            print(dash)
            label_header = (_('Ship'), _('Hits'), _('sunk'))
            print('{:<13}{:^8}{:^10}'.format(*label_header))
            print(dash)
            print('{:<13}{:^8}{:^10}'.format(*data_ship))
        else:
            print('{:<13}{:^8}{:^10}'.format(*data_ship))

    print(dash)


def main():
    game = Game()
    print_board(game)

    try:
        while True:
            while True:
                print(_('Press CTRL+C to exit ...'))
                result = input(_('Choose your coordinate using one LETTER from A to Q and one NUMBER from 0 to 16. \n'
                                 'Ex: a1, b15, c10 and etc... \n\nCoordinate: ')).strip()

                x, y = result[0], result[1:]
                try:
                    is_valid, ship = game.play(x, y)
                except (InvalidFormat, InvalidCoordinate) as exc:
                    os.system('clear')
                    print_error_message(_(str(exc)))
                    print_board(game)
                    break

                if is_valid:
                    print_ship_hit(ship, game)
                    break

                print_board(game)
                if game.is_finished():
                    sys.exit(print_status(game, win=True))

                if game.end_game():
                    sys.exit(print_status(game))

            print_board(game)

    except KeyboardInterrupt:
        sys.exit(print_status(game))
