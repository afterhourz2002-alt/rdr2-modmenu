"""Helper: dump current player-struct offsets for the attached build.

Run with the game open. Output goes to offsets/<build>.json for review before
committing to rdr2_bridge.OFFSETS.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from rdr2_modmenu.memory_bridge.rdr2_bridge import RDR2ProcessBridge, OFFSETS


def main() -> int:
    bridge = RDR2ProcessBridge()
    if not bridge.attach():
        print("attach failed — is RDR2.exe running?", file=sys.stderr)
        return 1
    snap = bridge.read_player_state()
    print(json.dumps({"build": bridge.build, "snapshot": snap, "known": OFFSETS.get(bridge.build)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())