"""A command-line tool to visualize disk usage as a treemap-inspired ASCII mosaic."""

__version__ = "0.1.0"

from .disk_usage import main
from .disk_usage_constants import (
    CATEGORY_MAP,
    CATEGORY_TO_GROUP,
    DEFAULT_TEXTURES,
    LEGEND_ORDER,
    LEGEND_STYLES,
    SIMPLIFIED_TEXTURES,
    Colors,
    FileCategory,
)
