"""DirectX overlay renderer for the in-game menu (uses imgui bindings)."""

from __future__ import annotations

import logging

log = logging.getLogger("rdr2_modmenu.overlay")

try:
    import imgui  # type: ignore
except ImportError:  # pragma: no cover
    imgui = None


class OverlayRenderer:
    def __init__(self, font: str = "consolas", scale: float = 1.0, toggle_key: str = "F5") -> None:
        self.font = font
        self.scale = scale
        self.toggle_key = toggle_key
        self.visible = False
        self._ctx = None

    def _ensure_ctx(self) -> None:
        if imgui is None:
            return
        if self._ctx is None:
            self._ctx = imgui.create_context()
            io = imgui.get_io()
            io.font_global_scale = self.scale

    def render(self, processors: dict) -> None:
        if imgui is None:
            return
        self._ensure_ctx()
        if not self.visible:
            return
        imgui.new_frame()
        imgui.begin("RDR2 ModMenu", True)
        for name, proc in processors.items():
            changed, value = imgui.checkbox(name, getattr(proc, "enabled", False))
            if changed:
                proc.enabled = value
                log.debug("toggle %s -> %s", name, value)
        imgui.end()
        imgui.render()

    def shutdown(self) -> None:
        if imgui is not None and self._ctx is not None:
            imgui.destroy_context(self._ctx)
            self._ctx = None