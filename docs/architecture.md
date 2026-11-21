# Architecture

```
script_hook/menu_hook.lua  ──pipe──┐
                                   ▼
                        menu_pipeline/ingest.py
                                   │
                                   ▼
                        menu_pipeline/pipeline.py
                                   │
                                   ▼
                       menu_pipeline/processors.py
                                   │
                                   ▼
                      memory_bridge/rdr2_bridge.py
                                   │
                                   ▼
                        overlay_core/overlay.py
```

- **ingest** — converts script-hook commands and memory snapshots into `MenuEvent`s.
- **pipeline** — thread-safe queue, dispatches events to registered processors at `tick_ms`.
- **processors** — one per feature (`godmode`, `noclip`, `money_drop`, `vehicle_spawn`).
- **bridge** — the only module that touches `pymem`; everything else is testable with a fake.
- **overlay** — imgui frame renderer, toggled via `overlay.toggle_key`.

Adding a feature means adding a `BaseProcessor` subclass and registering it in
`bootstrap.py` — nothing else.