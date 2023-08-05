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

    Points:  0     Shots Available:  50     Time elapsed:  0 sec
    ------------------------------------------------------------------------------------------
    | -  | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
    ------------------------------------------------------------------------------------------
    | A  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | B  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | C  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | D  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | E  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | F  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | G  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | H  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | I  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | J  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | K  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | L  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | M  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | N  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | O  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | P  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    | Q  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  | .  |
    ------------------------------------------------------------------------------------------
    Labels
    -------
    <Carrier>     Initials: CA  | Size: 5  | Hits: 0 | sunk: no
    <Battleship>  Initials: BT  | Size: 4  | Hits: 0 | sunk: no
    <Cruiser>     Initials: CR  | Size: 3  | Hits: 0 | sunk: no
    <Destroyer>   Initials: DT  | Size: 3  | Hits: 0 | sunk: no
    <Submarine>   Initials: SB  | Size: 2  | Hits: 0 | sunk: no
    <Frigate>     Initials: FR  | Size: 2  | Hits: 0 | sunk: no

    ------------------------------------------------------------------------------------------
    Press CTRL+C to exit ...
    Choose your coordinate using one LETTER from A to Q and one NUMBER from 0 to 16.
    Ex: a1, b15, c10 and etc...

    Coordinates: f5

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
