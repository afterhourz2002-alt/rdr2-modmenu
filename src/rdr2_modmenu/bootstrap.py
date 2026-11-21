"""Entry wiring for the mod menu: builds the pipeline from config + drivers."""

from __future__ import annotations

import logging
from pathlib import Path

from .menu_pipeline.pipeline import ModMenuPipeline
from .menu_pipeline.ingest import ScriptIngestHandler, MemoryIngestHandler
from .menu_pipeline.processors import (
    NoclipProcessor,
    MoneyDropProcessor,
    VehicleSpawnProcessor,
    GodModeProcessor,
)
from .overlay_core.overlay import OverlayRenderer
from .memory_bridge.rdr2_bridge import RDR2ProcessBridge
from .config.loader import load_config

log = logging.getLogger("rdr2_modmenu")


def bootstrap_menu(config_path: str | Path = "config/menu.toml") -> ModMenuPipeline:
    """Assemble the ingest -> process -> render pipeline for a running RDR2 session."""
    cfg = load_config(config_path)
    bridge = RDR2ProcessBridge(process_name=cfg.process_name, build=cfg.game_build)

    if not bridge.attach():
        log.warning("RDR2 process %s not found — running in dry-run mode", cfg.process_name)

    overlay = OverlayRenderer(
        font=cfg.overlay.font,
        scale=cfg.overlay.scale,
        toggle_key=cfg.overlay.toggle_key,
    )

    pipeline = ModMenuPipeline(overlay=overlay)
    pipeline.register_ingest(ScriptIngestHandler(bridge))
    pipeline.register_ingest(MemoryIngestHandler(bridge, poll_hz=cfg.poll_hz))

    pipeline.register_processor("godmode", GodModeProcessor(bridge))
    pipeline.register_processor("noclip", NoclipProcessor(bridge))
    pipeline.register_processor("money_drop", MoneyDropProcessor(bridge))
    pipeline.register_processor("vehicle_spawn", VehicleSpawnProcessor(bridge))

    log.info("modmenu bootstrapped (build=%s, features=%d)", cfg.game_build, len(cfg.features))
    return pipeline