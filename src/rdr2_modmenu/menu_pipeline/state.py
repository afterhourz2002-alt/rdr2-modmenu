"""Live menu state shared between processors and overlay."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MenuState:
    active_tab: str = "player"
    godmode: bool = False
    noclip: bool = False
    money_drop_amount: int = 500
    vehicle_model: str = "arabian_black"
    player: dict = field(default_factory=dict)

    def update_player(self, snap: dict) -> None:
        self.player.update(snap)