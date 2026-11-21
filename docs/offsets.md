# Offset reference

Offsets live in `src/rdr2_modmenu/memory_bridge/rdr2_bridge.py::OFFSETS`
and are keyed by the game build string shown in the RDR2 launcher.

| Build    | Player base | Health | Coords | Wanted |
| -------- | ----------- | ------ | ------ | ------ |
| 1491.50  | 0x03F2A1C8  | 0x2B8  | 0x30   | 0x4A0  |
| 1491.16  | 0x03F2A0F0  | 0x2B8  | 0x30   | 0x4A0  |
| 1436.28  | 0x03E1B9A0  | 0x2B0  | 0x28   | 0x498  |

## Adding a build

1. Run `python scripts/dump_offsets.py` with the game open on the new build.
2. Diff the snapshot against the previous build's snapshot.
3. Add a row above and a matching entry in `OFFSETS`.
4. Open a PR titled `offsets: add build <version>`.

If a build is missing from `OFFSETS`, `RDR2ProcessBridge` logs a warning and
runs in dry-run mode (no memory writes).