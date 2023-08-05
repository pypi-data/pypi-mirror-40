=================
Battleship Python
=================

|PyPI latest| |PyPI Version| |PyPI License|


This is a simple, but super cool Battleship game. Lets Play!!!


Installation
------------

.. code-block:: bash

   $ pip install py-battleship

Or, you can download the source and

.. code-block:: bash

   $ git clone git@github.com:rhenter/battleship-python.git
   $ cd battleship-python
   $ python setup.py install

Add sudo in the beginning if you met problem.


How to Use
----------

To play use py-battleship or python -m battlefield

.. code-block:: bash

    $ py-battleship

    Points:  1900     Shots Available:  31     Time elapsed:  178 sec
    ------------------------------------------------------------------------------------------
    | - | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
    ------------------------------------------------------------------------------------------
    | A | CA | CA | CA | CA | CA | O  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | B | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | C | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | D | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | E | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | F | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | G | .  | .  | .  | .  | .  | O  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | H | O  | .  | .  | .  | .  | .  | .  | CR | O  | O  | .  | .  | .  | .  | .  | .  | .  |
    | I | .  | .  | .  | .  | .  | .  | .  | CR | FR | .  | .  | .  | .  | .  | .  | .  | .  |
    | J | .  | .  | .  | .  | .  | .  | O  | CR | FR | .  | .  | .  | .  | .  | .  | .  | .  |
    | K | .  | .  | .  | .  | .  | .  | .  | .  | O  | .  | .  | .  | .  | .  | .  | .  | .  |
    | L | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | M | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | O  | .  |
    | N | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | O | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | P | .  | .  | .  | .  | .  | .  | .  | .  | .  | O  | .  | .  | .  | .  | .  | .  | .  |
    | Q | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    ------------------------------------------------------------------------------------------

    Labels
    ------------------------------------------------------------------------------------------
    Ship          Initials    Size    Hits     sunk
    ------------------------------------------------------------------------------------------
    Carrier          CA        5       5       yes
    Battleship       BT        4       0        no
    Cruiser          CR        3       3       yes
    Destroyer        DT        3       0        no
    Submarine        SB        2       0        no
    Frigate          FR        2       2       yes

    ------------------------------------------------------------------------------------------
    Press CTRL+C to exit ...
    Choose your coordinate using one LETTER from A to Q and one NUMBER from 0 to 16.
    Ex: a1, b15, c10 and etc...

    Coordinates:


Documentation
-------------

    In progress


Contributing
------------

Please send pull requests, very much appreciated.


1. Fork the `repository <https://github.com/rhenter/battleship-python>`_ on GitHub.
2. Make a branch off of master and commit your changes to it.
3. Install requirements. ``pip install -r requirements-dev.txt``
4. Install pre-commit. ``pre-commit install``
5. Create a Pull Request with your contribution



.. |PyPI Version| image:: https://img.shields.io/pypi/pyversions/py-battleship.svg?maxAge=360
   :target: https://pypi.python.org/pypi/py-battleship
.. |PyPI License| image:: https://img.shields.io/pypi/l/py-battleship.svg?maxAge=360
   :target: https://github.com/rhenter/battleship-python/blob/master/LICENSE
.. |PyPI latest| image:: https://img.shields.io/pypi/v/py-battleship.svg?maxAge=360
   :target: https://pypi.python.org/pypi/py-battleship
