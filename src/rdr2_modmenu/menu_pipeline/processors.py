"""Processors — each one implements a mod feature (godmode, noclip, money drop, vehicle spawn)."""

from __future__ import annotations

import logging

from ..memory_bridge.rdr2_bridge import RDR2ProcessBridge
from .ingest import MenuEvent

log = logging.getLogger("rdr2_modmenu.processors")


class BaseProcessor:
    feature = "base"

    def __init__(self, bridge: RDR2ProcessBridge) -> None:
        self.bridge = bridge
        self.enabled = False

    def handle(self, event: MenuEvent) -> None:
        raise NotImplementedError


class GodModeProcessor(BaseProcessor):
    feature = "godmode"

    def handle(self, event: MenuEvent) -> None:
        self.enabled = bool(event.payload.get("enabled", True))
        self.bridge.write_health_lock(self.enabled)
        log.info("godmode=%s", self.enabled)


class NoclipProcessor(BaseProcessor):
    feature = "noclip"

    def handle(self, event: MenuEvent) -> None:
        self.enabled = bool(event.payload.get("enabled", True))
        self.bridge.write_collision(self.enabled)
        log.info("noclip=%s", self.enabled)


class MoneyDropProcessor(BaseProcessor):
    feature = "money_drop"

    def handle(self, event: MenuEvent) -> None:
        amount = int(event.payload.get("amount", 500))
        self.bridge.spawn_pickup("money", amount=amount)
        log.info("money_drop amount=%d", amount)


class VehicleSpawnProcessor(BaseProcessor):
    feature = "vehicle_spawn"

    def handle(self, event: MenuEvent) -> None:
        model = event.payload.get("model", "arabian_black")
        self.bridge.spawn_vehicle(model)
        log.info("vehicle_spawn model=%s", model)