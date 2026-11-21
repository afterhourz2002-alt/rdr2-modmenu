from rdr2_modmenu.menu_pipeline.pipeline import ModMenuPipeline
from rdr2_modmenu.menu_pipeline.ingest import MenuEvent
from rdr2_modmenu.menu_pipeline.processors import GodModeProcessor


class FakeBridge:
    def __init__(self):
        self.health_lock = None
    def write_health_lock(self, v): self.health_lock = v


class FakeOverlay:
    def render(self, _): pass
    def shutdown(self): pass


def test_pipeline_dispatches_godmode():
    bridge = FakeBridge()
    pipeline = ModMenuPipeline(overlay=FakeOverlay())
    pipeline.register_processor("godmode", GodModeProcessor(bridge))
    pipeline._queue.append(MenuEvent(feature="godmode", payload={"enabled": True}, ts=0.0))
    pipeline._dispatch()
    assert bridge.health_lock is True