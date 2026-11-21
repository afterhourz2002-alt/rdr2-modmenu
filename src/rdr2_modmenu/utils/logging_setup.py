"""Rotating file logger used by cli.main when --log is passed."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_file_log(path: str | Path = "logs/modmenu.log", level: int = logging.DEBUG) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(p, maxBytes=2_000_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
    root = logging.getLogger("rdr2_modmenu")
    root.setLevel(level)
    root.addHandler(handler)