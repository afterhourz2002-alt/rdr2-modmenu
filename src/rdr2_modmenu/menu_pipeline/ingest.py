"""Ingest handlers — turn hotkeys, script hooks and memory reads into pipeline events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from ..memory_bridge.rdr2_bridge import RDR2ProcessBridge


@dataclass(slots=True)
class MenuEvent:
    feature: str
    payload: dict
    ts: float


class IngestHandler(Protocol):
    def poll(self) -> Iterable[MenuEvent]: ...


class ScriptIngestHandler:
    """Pulls commands queued by the in-game script hook (rdr2_modmenu.lua)."""

    def __init__(self, bridge: RDR2ProcessBridge) -> None:
        self.bridge = bridge

    def poll(self) -> Iterable[MenuEvent]:
        for raw in self.bridge.read_command_queue():
            yield MenuEvent(feature=raw["feature"], payload=raw["args"], ts=raw["ts"])


class MemoryIngestHandler:
    """Polls the player struct for state (health, position, wanted level)."""

    def __init__(self, bridge: RDR2ProcessBridge, poll_hz: int = 30) -> None:
        self.bridge = bridge
        self.poll_hz = poll_hz
        self._last = 0.0

    def poll(self) -> Iterable[MenuEvent]:
        import time
        now = time.monotonic()
        if now - self._last < 1.0 / self.poll_hz:
            return
        self._last = now
        snap = self.bridge.read_player_state()
        if snap:
            yield MenuEvent(feature="state_sync", payload=snap, ts=now)