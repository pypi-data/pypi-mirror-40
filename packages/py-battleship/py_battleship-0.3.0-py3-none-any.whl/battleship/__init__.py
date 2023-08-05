#!/usr/bin/env python
# encoding: utf-8
import gettext
from pathlib import Path

from .battleship import Game, Board, Ship  # noqa
from .version import __version__  # noqa


BASE_DIR = Path(__file__).absolute().parents[1]
LOCALE_DIR = BASE_DIR / "locale"

language = gettext.translation('battleship', localedir=str(LOCALE_DIR), languages=['pt_BR', 'en'])
language.install()


__all__ = ['Game', 'Board', 'Ship', '__version__', 'language', 'BASE_DIR']
