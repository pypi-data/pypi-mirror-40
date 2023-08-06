#!/usr/bin/env python
# encoding: utf-8
import gettext
from pathlib import Path

BASE_DIR = Path(__file__).parent
LOCALE_DIR = BASE_DIR / "locale"

if LOCALE_DIR.exists():
    language = gettext.translation('battleship', localedir=str(LOCALE_DIR), languages=['en', 'pt_BR'])
    language.install()
else:
    language = gettext
