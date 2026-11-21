"""rdr2-modmenu — Red Dead Redemption 2 external mod menu toolkit."""

__version__ = "0.9.4"
__build__ = "2026.03.17"

from .bootstrap import bootstrap_menu

__all__ = ["bootstrap_menu", "__version__", "__build__"]