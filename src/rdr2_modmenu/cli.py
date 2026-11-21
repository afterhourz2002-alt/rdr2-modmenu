"""Console entrypoint: `rdr2-modmenu` launches the pipeline or a one-shot feature."""

from __future__ import annotations

import argparse
import logging
import sys

from .bootstrap import bootstrap_menu


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rdr2-modmenu")
    parser.add_argument("--config", default="config/menu.toml")
    parser.add_argument("--once", metavar="FEATURE", help="dispatch a single feature and exit")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    pipeline = bootstrap_menu(args.config)
    if args.once:
        from .menu_pipeline.ingest import MenuEvent
        import time
        pipeline._queue.append(MenuEvent(feature=args.once, payload={"enabled": True}, ts=time.time()))
        pipeline._dispatch()
        return 0

    try:
        pipeline.run()
    except KeyboardInterrupt:
        pipeline.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())