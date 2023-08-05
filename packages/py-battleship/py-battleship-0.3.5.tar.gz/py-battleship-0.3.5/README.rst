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

   $ python setup.py install

Add sudo in the beginning if you met problem.


How to Use
----------

To play use `py-battleship` or `python -m battlefield`

.. code-block:: bash

    $ py-battleship

    Points:  0     Shots Available:  47     Time elapsed: 21 sec
    ------------------------------------------------------------------------------------------
    | -  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
    ------------------------------------------------------------------------------------------
    | a  | .  | O  | .  | .  | O  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | O  |
    | b  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | c  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | d  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | e  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | f  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | g  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | h  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | i  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | j  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | k  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | l  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | m  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | n  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | o  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | p  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | q  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    ------------------------------------------------------------------------------------------
    Labels
    -------
    <Carrier>    length: 5  | initials: CA  | Hits: 0 | sunk: no
    <Battleship> length: 4  | initials: BT  | Hits: 0 | sunk: no
    <Cruiser>    length: 3  | initials: CR  | Hits: 0 | sunk: no
    <Destroyer>  length: 3  | initials: DT  | Hits: 0 | sunk: no
    <Submarine>  length: 2  | initials: SB  | Hits: 0 | sunk: no
    <Frigate>    length: 2  | initials: FR  | Hits: 0 | sunk: no

    ------------------------------------------------------------------------------------------
    Choose your coordinates. Ex: a1, b15: c10

    Coordinates: q10

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
