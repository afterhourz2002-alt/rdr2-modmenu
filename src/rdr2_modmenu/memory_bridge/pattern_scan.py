"""AOB pattern scanner used by scripts/dump_offsets.py when a build is unknown."""

from __future__ import annotations

import re

PATTERN = re.compile(rb"[\x00-\xff]")


def parse_pattern(sig: str) -> bytes:
    """Convert '48 8B 05 ?? ?? ?? ??' into a regex-compatible bytes pattern."""
    out = []
    for tok in sig.split():
        if tok in ("??", "?"):
            out.append(b".")
        else:
            out.append(re.escape(bytes([int(tok, 16)])))
    return b"".join(out)


def scan(buffer: bytes, sig: str) -> int | None:
    m = re.search(parse_pattern(sig), buffer)
    return m.start() if m else None