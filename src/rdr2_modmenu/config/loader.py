"""TOML config loader — reads config/menu.toml into typed dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


@dataclass
class OverlayConfig:
    font: str = "consolas"
    scale: float = 1.0
    toggle_key: str = "F5"


@dataclass
class MenuConfig:
    process_name: str = "RDR2.exe"
    game_build: str = "1491.50"
    poll_hz: int = 30
    features: list[str] = field(default_factory=lambda: ["godmode", "noclip", "money_drop"])
    overlay: OverlayConfig = field(default_factory=OverlayConfig)


def load_config(path: str | Path) -> MenuConfig:
    p = Path(path)
    if not p.exists():
        return MenuConfig()
    with p.open("rb") as fh:
        data = tomllib.load(fh)
    return MenuConfig(
        process_name=data.get("process_name", "RDR2.exe"),
        game_build=data.get("game_build", "1491.50"),
        poll_hz=int(data.get("poll_hz", 30)),
        features=list(data.get("features", [])),
        overlay=OverlayConfig(**data.get("overlay", {})),
    )