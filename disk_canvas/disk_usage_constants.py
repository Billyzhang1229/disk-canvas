"""Constants for disk-canvas visualization."""

from enum import Enum, auto


class FileCategory(Enum):
    """Categories for different types of files."""

    CODE = auto()
    NOTEBOOK = auto()
    DATA = auto()
    COMPRESSED = auto()
    CACHE = auto()
    IMAGE = auto()
    VIDEO = auto()
    AUDIO = auto()
    DOCUMENT = auto()
    CONFIG = auto()
    OTHER = auto()


def hex_to_ansi(hex_code: str) -> str:
    """Convert a hex color code to a 24-bit ANSI escape sequence.

    Args:
        hex_code: The hex color code (e.g. '#636EFA')

    Returns:
        The corresponding ANSI escape sequence
    """
    hex_code = hex_code.lstrip("#")
    if len(hex_code) != 6:
        raise ValueError("Invalid hex code")
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"


class Colors:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    # Use the provided Plotly color palette.
    PALETTE_HEX = [
        "#636EFA",
        "#EF553B",
        "#00CC96",
        "#AB63FA",
        "#FFA15A",
        "#19D3F3",
        "#FF6692",
        "#B6E880",
        "#FF97FF",
        "#FECB52",
    ]
    # Build a dictionary mapping "color0" ... "color9" to ANSI escape sequences.
    _all_colors = {f"color{i}": hex_to_ansi(c) for i, c in enumerate(PALETTE_HEX)}
    _all_colors["white"] = "\033[38;2;250;250;250m"
    COLOR_PALETTE = list(_all_colors.keys())

    @classmethod
    def get_all_colors(cls) -> dict:
        """Get a dictionary of all available color codes.

        Returns:
            A dictionary mapping color names to ANSI codes
        """
        return cls._all_colors


# Detailed textures for detailed mode
DEFAULT_TEXTURES = {
    FileCategory.CODE: "█",
    FileCategory.NOTEBOOK: "▓",
    FileCategory.DATA: "▒",
    FileCategory.COMPRESSED: "◆",
    FileCategory.CACHE: "·",
    FileCategory.IMAGE: "◐",
    FileCategory.VIDEO: "◢",
    FileCategory.AUDIO: "◇",
    FileCategory.DOCUMENT: "○",
    FileCategory.CONFIG: "☰",
    FileCategory.OTHER: ".",
}

DETAILED_TEXTURES = [
    "█",
    "▓",
    "▒",
    "░",
    "◆",
    "◇",
    "○",
    "●",
    "◐",
    "◢",
    "☰",
    "·",
]

# Simplified textures for non-detailed mode.
SIMPLIFIED_TEXTURES = {
    FileCategory.CODE: "█",
    FileCategory.NOTEBOOK: "█",  # Same as CODE
    FileCategory.DATA: "▒",
    FileCategory.COMPRESSED: "◆",
    FileCategory.CACHE: "·",
    FileCategory.IMAGE: "◐",
    FileCategory.VIDEO: "◐",
    FileCategory.AUDIO: "◐",
    FileCategory.DOCUMENT: "○",
    FileCategory.CONFIG: "☰",
    FileCategory.OTHER: ".",
}

# Updated CATEGORY_COLORS using our new palette keys.
CATEGORY_COLORS = {
    FileCategory.CODE: "color0",
    FileCategory.NOTEBOOK: "color1",
    FileCategory.DATA: "color2",
    FileCategory.COMPRESSED: "color3",
    FileCategory.CACHE: "color4",
    FileCategory.IMAGE: "color5",
    FileCategory.VIDEO: "color6",
    FileCategory.AUDIO: "color7",
    FileCategory.DOCUMENT: "color8",
    FileCategory.CONFIG: "color9",
    FileCategory.OTHER: "color1",
}

# Map file extensions to file categories.
CATEGORY_MAP = {
    # Code files
    ".py": FileCategory.CODE,
    ".js": FileCategory.CODE,
    ".ts": FileCategory.CODE,
    ".java": FileCategory.CODE,
    ".cpp": FileCategory.CODE,
    ".c": FileCategory.CODE,
    ".h": FileCategory.CODE,
    ".rs": FileCategory.CODE,
    ".go": FileCategory.CODE,
    ".rb": FileCategory.CODE,
    ".php": FileCategory.CODE,
    ".cs": FileCategory.CODE,
    ".swift": FileCategory.CODE,
    ".kt": FileCategory.CODE,
    ".scala": FileCategory.CODE,
    ".r": FileCategory.CODE,
    ".sh": FileCategory.CODE,
    ".bash": FileCategory.CODE,
    ".zsh": FileCategory.CODE,
    ".fish": FileCategory.CODE,
    ".vim": FileCategory.CODE,
    ".lua": FileCategory.CODE,
    ".pl": FileCategory.CODE,
    ".pm": FileCategory.CODE,
    ".t": FileCategory.CODE,
    ".sql": FileCategory.CODE,
    # Notebook files
    ".ipynb": FileCategory.NOTEBOOK,
    ".rmd": FileCategory.NOTEBOOK,
    ".qmd": FileCategory.NOTEBOOK,
    # Data files
    ".csv": FileCategory.DATA,
    ".tsv": FileCategory.DATA,
    ".json": FileCategory.DATA,
    ".yaml": FileCategory.DATA,
    ".yml": FileCategory.DATA,
    ".xml": FileCategory.DATA,
    ".toml": FileCategory.DATA,
    ".ini": FileCategory.DATA,
    ".conf": FileCategory.DATA,
    ".cfg": FileCategory.DATA,
    ".properties": FileCategory.DATA,
    ".env": FileCategory.DATA,
    ".sqlite": FileCategory.DATA,
    ".db": FileCategory.DATA,
    ".parquet": FileCategory.DATA,
    ".avro": FileCategory.DATA,
    ".orc": FileCategory.DATA,
    ".feather": FileCategory.DATA,
    ".arrow": FileCategory.DATA,
    ".hdf5": FileCategory.DATA,
    ".h5": FileCategory.DATA,
    ".nc": FileCategory.DATA,
    ".mat": FileCategory.DATA,
    ".pkl": FileCategory.DATA,
    ".pickle": FileCategory.DATA,
    ".npy": FileCategory.DATA,
    ".npz": FileCategory.DATA,
    # Compressed files
    ".zip": FileCategory.COMPRESSED,
    ".tar": FileCategory.COMPRESSED,
    ".gz": FileCategory.COMPRESSED,
    ".bz2": FileCategory.COMPRESSED,
    ".xz": FileCategory.COMPRESSED,
    ".7z": FileCategory.COMPRESSED,
    ".rar": FileCategory.COMPRESSED,
    ".tgz": FileCategory.COMPRESSED,
    ".tbz2": FileCategory.COMPRESSED,
    # Cache files
    ".pyc": FileCategory.CACHE,
    ".pyo": FileCategory.CACHE,
    ".pyd": FileCategory.CACHE,
    ".class": FileCategory.CACHE,
    ".o": FileCategory.CACHE,
    ".so": FileCategory.CACHE,
    ".dll": FileCategory.CACHE,
    ".dylib": FileCategory.CACHE,
    ".cache": FileCategory.CACHE,
    ".swp": FileCategory.CACHE,
    ".swo": FileCategory.CACHE,
    ".swn": FileCategory.CACHE,
    # Media files - Images
    ".jpg": FileCategory.IMAGE,
    ".jpeg": FileCategory.IMAGE,
    ".png": FileCategory.IMAGE,
    ".gif": FileCategory.IMAGE,
    ".bmp": FileCategory.IMAGE,
    ".tiff": FileCategory.IMAGE,
    ".webp": FileCategory.IMAGE,
    ".svg": FileCategory.IMAGE,
    ".ico": FileCategory.IMAGE,
    ".eps": FileCategory.IMAGE,
    ".raw": FileCategory.IMAGE,
    ".cr2": FileCategory.IMAGE,
    ".nef": FileCategory.IMAGE,
    ".heic": FileCategory.IMAGE,
    # Media files - Video
    ".mp4": FileCategory.VIDEO,
    ".avi": FileCategory.VIDEO,
    ".mkv": FileCategory.VIDEO,
    ".mov": FileCategory.VIDEO,
    ".wmv": FileCategory.VIDEO,
    ".flv": FileCategory.VIDEO,
    ".webm": FileCategory.VIDEO,
    ".m4v": FileCategory.VIDEO,
    ".mpg": FileCategory.VIDEO,
    ".mpeg": FileCategory.VIDEO,
    ".3gp": FileCategory.VIDEO,
    # Media files - Audio
    ".mp3": FileCategory.AUDIO,
    ".wav": FileCategory.AUDIO,
    ".flac": FileCategory.AUDIO,
    ".m4a": FileCategory.AUDIO,
    ".ogg": FileCategory.AUDIO,
    ".aac": FileCategory.AUDIO,
    ".wma": FileCategory.AUDIO,
    ".aiff": FileCategory.AUDIO,
    ".opus": FileCategory.AUDIO,
    # Document files
    ".pdf": FileCategory.DOCUMENT,
    ".doc": FileCategory.DOCUMENT,
    ".docx": FileCategory.DOCUMENT,
    ".xls": FileCategory.DOCUMENT,
    ".xlsx": FileCategory.DOCUMENT,
    ".ppt": FileCategory.DOCUMENT,
    ".pptx": FileCategory.DOCUMENT,
    ".odt": FileCategory.DOCUMENT,
    ".ods": FileCategory.DOCUMENT,
    ".odp": FileCategory.DOCUMENT,
    ".pages": FileCategory.DOCUMENT,
    ".numbers": FileCategory.DOCUMENT,
    ".keynote": FileCategory.DOCUMENT,
    ".txt": FileCategory.DOCUMENT,
    ".rtf": FileCategory.DOCUMENT,
    ".md": FileCategory.DOCUMENT,
    ".rst": FileCategory.DOCUMENT,
    ".tex": FileCategory.DOCUMENT,
    ".html": FileCategory.DOCUMENT,
    ".htm": FileCategory.DOCUMENT,
    ".epub": FileCategory.DOCUMENT,
    ".mobi": FileCategory.DOCUMENT,
    ".azw3": FileCategory.DOCUMENT,
    # Config files
    ".gitignore": FileCategory.CONFIG,
    ".dockerignore": FileCategory.CONFIG,
    ".editorconfig": FileCategory.CONFIG,
    ".prettierrc": FileCategory.CONFIG,
    ".eslintrc": FileCategory.CONFIG,
    ".babelrc": FileCategory.CONFIG,
    ".npmrc": FileCategory.CONFIG,
    ".yarnrc": FileCategory.CONFIG,
    ".config": FileCategory.CONFIG,
    "Dockerfile": FileCategory.CONFIG,
    "docker-compose.yml": FileCategory.CONFIG,
    "Makefile": FileCategory.CONFIG,
    "CMakeLists.txt": FileCategory.CONFIG,
    "requirements.txt": FileCategory.CONFIG,
    "setup.py": FileCategory.CONFIG,
    "setup.cfg": FileCategory.CONFIG,
    "pyproject.toml": FileCategory.CONFIG,
    "package.json": FileCategory.CONFIG,
    "tsconfig.json": FileCategory.CONFIG,
    "tox.ini": FileCategory.CONFIG,
    ".flake8": FileCategory.CONFIG,
    ".coveragerc": FileCategory.CONFIG,
    ".travis.yml": FileCategory.CONFIG,
    ".gitlab-ci.yml": FileCategory.CONFIG,
    ".github": FileCategory.CONFIG,
}

LEGEND_ORDER = [
    ("CODE_GROUP", "Code/Notebook files"),
    ("MEDIA_GROUP", "Media/Documents"),
    ("DATA_GROUP", "Data/Compressed files"),
    ("SYSTEM_GROUP", "Cache/Build/Config files"),
    ("OTHER_GROUP", "Other files"),
]

LEGEND_STYLES = {
    "CODE_GROUP": {
        "symbol": SIMPLIFIED_TEXTURES[FileCategory.CODE],
        "color": "white",
    },
    "MEDIA_GROUP": {
        "symbol": SIMPLIFIED_TEXTURES[FileCategory.DOCUMENT],
        "color": "white",
    },
    "DATA_GROUP": {
        "symbol": SIMPLIFIED_TEXTURES[FileCategory.DATA],
        "color": "white",
    },
    "SYSTEM_GROUP": {
        "symbol": SIMPLIFIED_TEXTURES[FileCategory.CACHE],
        "color": "white",
    },
    "OTHER_GROUP": {
        "symbol": SIMPLIFIED_TEXTURES[FileCategory.OTHER],
        "color": "white",
    },
}

LARGE_CATEGORIES = {
    "CODE_GROUP": {FileCategory.CODE, FileCategory.NOTEBOOK},
    "DATA_GROUP": {FileCategory.DATA, FileCategory.COMPRESSED},
    "SYSTEM_GROUP": {FileCategory.CACHE, FileCategory.CONFIG},
    "MEDIA_GROUP": {
        FileCategory.IMAGE,
        FileCategory.VIDEO,
        FileCategory.AUDIO,
        FileCategory.DOCUMENT,
    },
    "OTHER_GROUP": {FileCategory.OTHER},
}

CATEGORY_TO_GROUP = {}
for group_name, categories in LARGE_CATEGORIES.items():
    for category in categories:
        CATEGORY_TO_GROUP[category] = group_name
