"""Core job pipeline: pulls events from ingest handlers, dispatches to processors, renders via overlay."""

from __future__ import annotations

import logging
import threading
import time
from collections import deque
from typing import Callable

from ..menu_pipeline.ingest import IngestHandler
from ..menu_pipeline.processors import BaseProcessor
from ..overlay_core.overlay import OverlayRenderer

log = logging.getLogger("rdr2_modmenu.pipeline")


class ModMenuPipeline:
    def __init__(self, overlay: OverlayRenderer, tick_ms: int = 16) -> None:
        self.overlay = overlay
        self.tick_ms = tick_ms
        self._ingest: list[IngestHandler] = []
        self._processors: dict[str, BaseProcessor] = {}
        self._queue: deque = deque(maxlen=512)
        self._stop = threading.Event()

    def register_ingest(self, handler: IngestHandler) -> None:
        self._ingest.append(handler)

    def register_processor(self, name: str, proc: BaseProcessor) -> None:
        self._processors[name] = proc

    def _drain(self) -> None:
        for handler in self._ingest:
            for event in handler.poll():
                self._queue.append(event)

    def _dispatch(self) -> None:
        while self._queue:
            event = self._queue.popleft()
            proc: Callable | None = self._processors.get(event.feature)
            if proc is None:
                log.debug("no processor for feature=%s", event.feature)
                continue
            try:
                proc.handle(event)
            except Exception as exc:
                log.exception("processor %s failed: %s", event.feature, exc)

    def run(self) -> None:
        log.info("pipeline running (%d ingest, %d processors)", len(self._ingest), len(self._processors))
        try:
            while not self._stop.is_set():
                self._drain()
                self._dispatch()
                self.overlay.render(self._processors)
                time.sleep(self.tick_ms / 1000.0)
        finally:
            self.overlay.shutdown()

    def stop(self) -> None:
        self._stop.set()