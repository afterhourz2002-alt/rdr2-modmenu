"""Thin wrapper around pymem for RDR2.exe — offsets are version-gated by game build."""

from __future__ import annotations

import logging
from dataclasses import dataclass

log = logging.getLogger("rdr2_modmenu.bridge")

try:
    import pymem  # type: ignore
    import pymem.process  # type: ignore
except ImportError:  # pragma: no cover
    pymem = None


OFFSETS = {
    "1491.50": {"player": 0x03F2A1C8, "health": 0x2B8, "coords": 0x30, "wanted": 0x4A0},
    "1491.16": {"player": 0x03F2A0F0, "health": 0x2B8, "coords": 0x30, "wanted": 0x4A0},
    "1436.28": {"player": 0x03E1B9A0, "health": 0x2B0, "coords": 0x28, "wanted": 0x498},
}


@dataclass
class PlayerSnapshot:
    health: float
    x: float
    y: float
    z: float
    wanted: int


class RDR2ProcessBridge:
    def __init__(self, process_name: str = "RDR2.exe", build: str = "1491.50") -> None:
        self.process_name = process_name
        self.build = build
        self._pm = None
        self._base = 0
        self._off = OFFSETS.get(build)
        if self._off is None:
            log.warning("unknown build %s — offsets may be stale", build)

    def attach(self) -> bool:
        if pymem is None:
            log.warning("pymem not installed; dry-run only")
            return False
        try:
            self._pm = pymem.Pymem(self.process_name)
            self._base = pymem.process.module_from_name(
                self._pm.process_handle, self.process_name
            ).lpBaseOfDll
            log.info("attached to %s @ 0x%X", self.process_name, self._base)
            return True
        except Exception as exc:
            log.error("attach failed: %s", exc)
            return False

    def _read(self, addr: int, size: int) -> bytes | None:
        if self._pm is None:
            return None
        try:
            return self._pm.read_bytes(addr, size)
        except Exception:
            return None

    def read_player_state(self) -> dict | None:
        if not self._off or self._pm is None:
            return None
        base = self._base + self._off["player"]
        raw = self._read(base, 0x500)
        if raw is None:
            return None
        import struct
        health = struct.unpack_from("<f", raw, self._off["health"])[0]
        x, y, z = struct.unpack_from("<fff", raw, self._off["coords"])
        wanted = struct.unpack_from("<i", raw, self._off["wanted"])[0]
        return {"health": health, "x": x, "y": y, "z": z, "wanted": wanted}

    def read_command_queue(self) -> list[dict]:
        # populated by the script hook via a named pipe
        return []

    def write_health_lock(self, enabled: bool) -> None: ...
    def write_collision(self, enabled: bool) -> None: ...
    def spawn_pickup(self, kind: str, **kw) -> None: ...
    def spawn_vehicle(self, model: str) -> None: ...