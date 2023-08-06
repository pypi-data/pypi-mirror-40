#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime
import random
from copy import deepcopy

from .constants import LETTERS
from .exceptions import InvalidLocation, InvalidCoordinate, InvalidFormat
from .language import language

_ = language.gettext

MESSAGE_ERROR = _(
    'You need to choose a letter from A to Q \n'
    'and one NUMBER from 0 to 16.'
)


class Ship:
    def __init__(self, name, length, points, initials):
        self.direction = ''
        self.hit_positions = []
        self.initials = initials
        self.length = length
        self.name = name
        self.sink = False
        self.points = points

    @property
    def hits(self):
        return len([x['hit'] for x in self.hit_positions if x['hit']])

    @property
    def is_destroyed(self):
        results = []
        for position in self.hit_positions:
            results.append(
                position['hit']
            )
        return all(results)

    @property
    def total_positions(self):
        return len(self.hit_positions)

    def add_location(self, x, y, hit):
        if len(self.hit_positions) + 1 > self.length:
            text = 'Ship has more hit positions {} than Lenght: {}'.format(
                len(self.hit_positions) + 1,
                self.length
            )
            raise InvalidLocation(text)

        self.hit_positions.append({
            'x': x,
            'y': y,
            'hit': hit
        })

    def hit(self, x, y):
        for pos in self.hit_positions:
            if (x, y) == (pos['x'], pos['y']):
                pos['hit'] = True

    def __str__(self):
        return self.name.title()

    def __repr__(self):
        return "<Ship: {}>".format(self.__str__())


class Board:
    COLS = 17
    ROWS = 17
    DEFAULT_VALUE = {
        'ship': None,
        'shooted': False,
    }
    SHIP_TYPES = [
        {'name': _('carrier'), 'length': 5, 'points': 250, 'initials': 'CA'},
        {'name': _('battleship'), 'length': 4, 'points': 200, 'initials': 'BT'},
        {'name': _('cruiser'), 'length': 3, 'points': 150, 'initials': 'CR'},
        {'name': _('destroyer'), 'length': 3, 'points': 150, 'initials': 'DT'},
        {'name': _('submarine'), 'length': 2, 'points': 100, 'initials': 'SB'},
        {'name': _('frigate'), 'length': 2, 'points': 100, 'initials': 'FR'},
    ]

    def __init__(self):
        self.matrix = self.clear_board()
        self.sunken_ships = 0
        self.ships = []
        self.total_hits = 0
        self._init_ships()

    @property
    def total_available_ships(self):
        return len(self.ships)

    @property
    def total_ships(self):
        return len([ship for ship in self.ships if ship.total_positions])

    def _init_ships(self):
        for _, ship_type in enumerate(self.SHIP_TYPES):
            self.ships.append(Ship(**ship_type))

    def _add_ship(self, ship):
        direction = random.choice(['v', 'h'])
        ship.direction = direction
        length = ship.length

        if direction == 'h':
            x = random.randint(0, self.COLS - length)
            end_position = (x + length)

            for col in range(x, end_position):
                if not self.is_available(x, col):
                    return False

                ship.add_location(x, col, False)

                value = deepcopy(self.DEFAULT_VALUE)
                value['ship'] = ship
                self.matrix[x][col] = value
        else:
            y = random.randint(0, self.ROWS - length)
            end_position = (y + length)

            for row in range(y, end_position):
                if not self.is_available(row, y):
                    return False

                ship.add_location(row, y, False)
                value = deepcopy(self.DEFAULT_VALUE)
                value['ship'] = ship
                self.matrix[row][y] = value

        return True

    def is_finished(self):
        results = []
        for ship in self.ships:
            results.append(
                ship.is_destroyed
            )
        return all(results)

    def _remove_ship(self, ship):
        for position in ship.hit_positions:
            self.matrix[position['x']][position['y']] = deepcopy(self.DEFAULT_VALUE)

    def add_ship(self, ship):
        added = self._add_ship(ship)
        if not added:
            self._remove_ship(ship)
            return self.add_ship(ship)
        return added

    def build_fleet(self):
        for ship in self.ships:
            self.add_ship(ship)

    def clear_board(self):
        default_value = deepcopy(self.DEFAULT_VALUE)
        return [[default_value for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def is_available(self, x, y):
        return self.matrix[x][y] == deepcopy(self.DEFAULT_VALUE)

    def shot(self, x, y):
        position = self.matrix[x][y].copy()

        if position['shooted']:
            return False, None

        position.update(shooted=True)
        if not position['ship']:
            self.matrix[x][y] = position
            return False, None

        position['ship'].hit(x, y)

        self.total_hits += 1
        if position['ship'].is_destroyed:
            self.sunken_ships += 1
            position['ship'].sink = True

        self.matrix[x][y] = position
        return True, position['ship']


class Game(Board):
    def __init__(self):
        super().__init__()
        self.start_time = datetime.now()
        self.shots = 50
        self.points = 0
        self.lost_shot = 0
        self.right_shot = 0

        # Building Fleet
        self.build_fleet()

    @property
    def time_elapsed(self):
        end_time = datetime.now()
        return (end_time - self.start_time).total_seconds()

    def play(self, raw_x, raw_y):


        try:
            x = int(LETTERS[raw_x.lower()])
            y = int(raw_y.strip())
        except ValueError:
            msg = _('Invalid Format. {}. Coordinate: {}{}').format(MESSAGE_ERROR, raw_x, raw_y)
            raise InvalidFormat(msg)

        if x not in range(17) or y not in range(17):
            msg = _('Invalid Coordinate. {}. Coordinate: {}{}').format(MESSAGE_ERROR, raw_x, raw_y)
            raise InvalidCoordinate(msg)

        if self.matrix[x][y]['shooted']:
            return False, None
        else:
            self.shots -= 1

            hit, ship = self.shot(x, y)

            if not hit:
                self.lost_shot += 1
                return False, None

            self.right_shot += 1
            self.points += ship.points
            return True, ship

    def end_game(self):
        if self.is_finished() or self.shots == 0:
            return True
        return False
