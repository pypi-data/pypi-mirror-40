from datetime import datetime
import random
from copy import deepcopy


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
    def positions(self):
        return len(self.hit_positions)

    def add_location(self, x, y, hit):
        self.hit_positions.append({
            'x': x,
            'y': y,
            'hit': hit
        })

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
        {'name': 'carrier', 'length': 5, 'points': 250, 'initials': 'CA'},
        {'name': 'battleship', 'length': 4, 'points': 200, 'initials': 'BT'},
        {'name': 'cruiser', 'length': 3, 'points': 150, 'initials': 'CR'},
        {'name': 'destroyer', 'length': 3, 'points': 150, 'initials': 'DT'},
        {'name': 'submarine', 'length': 2, 'points': 100, 'initials': 'SB'},
        {'name': 'frigate', 'length': 2, 'points': 100, 'initials': 'FR'},
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
        return len([ship for ship in self.ships if ship.positions])

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

    def _is_destoyed(self, ship):
        results = []
        for position in ship.hit_positions:
            results.append(
                self.matrix[position['x']][position['y']]['shooted']
            )
        return all(results)

    def is_finished(self):
        results = []
        for ship in self.ships:
            for position in ship.hit_positions:
                results.append(
                    self.matrix[position['x']][position['y']]['shooted']
                )
        return all(results)

    def _remove_ship(self, ship):
        for position in ship.hit_positions:
            self.matrix[position['x']][position['y']] = deepcopy(self.DEFAULT_VALUE)

    def add_ship(self, ship):
        if not self._add_ship(ship):
            self._remove_ship(ship)
            return self.add_ship(ship)
        return self._add_ship(ship)

    def build_fleet(self):
        for ship in self.ships:
            self.add_ship(ship)

    def clear_board(self):
        default_value = deepcopy(self.DEFAULT_VALUE)
        return [[default_value for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def is_available(self, x, y):
        return self.matrix[x][y] == deepcopy(self.DEFAULT_VALUE)

    def shot(self, x, y):
        position = deepcopy(self.matrix[x][y])

        if position['shooted']:
            return False, None

        position['shooted'] = True
        if not position['ship']:
            self.matrix[x][y] = position
            return False, None

        self.total_hits += 1

        if self._is_destoyed(position['ship']):
            self.sunken_ships += 1
            position['ship'].sink = True

        self.matrix[x][y] = position
        return True, position['ship']


class Game:
    def __init__(self):
        self.start_time = datetime.now()
        self.shots = 50
        self.points = 0

        board = Board()
        board.build_fleet()
        self.board = board

    @property
    def time_elapsed(self):
        end_time = datetime.now()
        return (end_time - self.start_time).total_seconds()

    def play(self, x, y):

        if self.board.matrix[x][y]['shooted']:
            return False, None
        else:
            self.shots -= 1

            hit, ship = self.board.shot(x, y)

            if not hit:
                return False, None

            self.points += ship.points

            if self.board.is_finished() or self.shots == 0:
                raise Exception('Acabou')

            return True, ship

    def end_game(self):
        if self.board.is_finished() or self.shots == 0:
            return True
        return False
