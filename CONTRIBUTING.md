# Contributing to rdr2-modmenu

Thanks for wanting to help. This project is an **external, single-player only**
mod menu pipeline for Red Dead Redemption 2. It does **not** target Red Dead
Online — PRs that touch RDO code paths will be closed.

## Ground rules

- Single-player (`RDR2.exe` offline) only.
- Keep the pipeline architecture: ingest → processor → overlay. New features
  are a new `BaseProcessor` subclass, not a hack in `bootstrap.py`.
- Offsets belong in `memory_bridge/rdr2_bridge.py::OFFSETS`, gated by game
  build string. Include the build you tested against in your PR.
- Lua-side hooks go in `script_hook/menu_hook.lua`.

## Dev setup

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python -m rdr2_modmenu.cli --once godmode -v
```

## Adding a feature

1. Subclass `BaseProcessor` in `menu_pipeline/processors.py`.
2. Register it in `bootstrap.py`.
3. Add a config toggle in `config/menu.toml`.
4. Write a test in `tests/` using a fake bridge (see `test_pipeline.py`).

## Code style

`ruff` + `black`, line length 100. Type hints on all public functions.

## Reporting offset breakage

Open an issue with: game build, patch date, and the exact feature that broke.