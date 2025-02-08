# disk-canvas

[![PyPI version](https://badge.fury.io/py/disk-canvas.svg)](https://badge.fury.io/py/disk-canvas)
[![Python Versions](https://img.shields.io/pypi/pyversions/disk-canvas.svg)](https://pypi.org/project/disk-canvas/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A command-line tool to visualize disk usage as a treemap-inspired ASCII mosaic. It scans a directory and produces a mosaic of uniformly sized, color-coded blocks based on file size and category. The visualization is designed to work on Linux and macOS.

## Features

- **ASCII Mosaic Visualization:** A terminal-friendly mosaic that offers a quick visual summary of disk usage.
- **Color-Coded Output:** Uses a modern Plotly-inspired color palette.
- **Multiple Modes:** Detailed mode with a legend mapping file extensions, or a simplified mode grouping files by category.
- **Cross-Platform:** Works on Linux and macOS.
- **Smart File Categorization:** Automatically categorizes files into:
  - Code (Python, Java, JavaScript, etc.)
  - Notebooks (Jupyter, R Markdown)
  - Data (CSV, JSON, SQL, etc.)
  - Compressed (ZIP, TAR, etc.)
  - Cache/Build files
  - Media (Images, Video, Audio)
  - Documents (PDF, Office, Text)
  - Configuration files
- **Flexible Display Options:** Choose between a sorted mosaic view or a treemap-style visualization.

## Installation

### From PyPI

```bash
pip install disk-canvas
```

### From Source

Clone the repository, then run:

```bash
cd disk-canvas
pip install .
```

## Usage

Basic usage:

```bash
python -m disk_canvas /path/to/directory
```

Full options:

```bash
python -m disk_canvas /path/to/directory [-t TOP] [-f] [-d DEPTH] [-D] [-U]
```

Options:

- `-t, --top`: Number of largest items per depth (default: 10)
- `-f, --files`: Show only files (exclude directories)
- `-d, --depth`: Maximum directory depth (default: 1)
- `-D, --detail`: Display a detailed legend with file extensions
- `-U, --unsort`: Use unsorted (treemap) canvas layout (default is sorted mosaic)

### Example Output

```
Disk Usage Visualization for: /Users/bz/Developer/disk-canvas
Total size: 405.8K

Top 10 largest items (max depth: 1):
      Size Type   Depth  Category     Path
----------------------------------------------------------
    405.8K [DIR]  0      DIR          .
    156.6K [DIR]  1      DIR          .git
     79.6K [DIR]  1      DIR          tests
     54.7K [DIR]  1      DIR          disk_canvas
     52.0K [FILE] 1      OTHER        .coverage
     27.9K [DIR]  1      DIR          dist
     13.8K [FILE] 1      DATA         coverage.xml
      5.6K [DIR]  1      DIR          disk_canvas.egg-info
      4.8K [FILE] 1      DOCUMENT     README.md
      2.8K [DIR]  1      DIR          .pytest_cache

████████████████▒▒▒▒◆◆◆◆◆······················○○........................
███████████████▒▒▒▒▒◆◆◆◆◆······················○○........................
███████████████▒▒▒▒▒◆◆◆◆◆·····················○○○........................
███████████████▒▒▒▒▒◆◆◆◆◆·····················○○○........................
███████████████▒▒▒▒▒◆◆◆◆······················○○☰........................
███████████████▒▒▒▒▒◆◆◆◆······················○○.........................

Detailed Extension Legend:

CODE files: (55.3K)
  █ .py      (10 files, 55.3K)

DATA files: (17.6K)
  ▒ .xml     (1 files, 13.8K)
  ▒ .toml    (1 files, 1.8K)
  ▒ .yml     (2 files, 1.5K)
  ▒ .yaml    (1 files, 617.0B)

COMPRESSED files: (16.9K)
  ◆ .gz      (1 files, 16.9K)

CACHE files: (78.9K)
  · .pyc     (10 files, 78.9K)

DOCUMENT files: (8.3K)
  ○ .md      (4 files, 7.6K)
  ○ .txt     (5 files, 690.0B)

CONFIG files: (734.0B)
  ☰ .gitignore (2 files, 551.0B)
  ☰ .flake8  (1 files, 183.0B)

OTHER files: (88.7K)
  . .coverage (1 files, 52.0K)
  . .sample  (13 files, 23.0K)
  . .whl     (1 files, 11.0K)
  . .pack    (1 files, 1.5K)
  . .idx     (1 files, 1.1K)
  . .tag     (1 files, 191.0B)
```

## Color and Symbol Legend

The visualization uses different symbols for different file types:

- `█` - Code files
- `▓` - Notebooks
- `▒` - Data files
- `◆` - Compressed files
- `·` - Cache files
- `◐` - Image files
- `◢` - Video files
- `◇` - Audio files
- `○` - Documents
- `☰` - Config files
- `.` - Other files

In simplified mode, similar categories share the same symbol for a cleaner view.

## Requirements

- Python 3.8 or higher
- Linux or macOS (Windows support is limited due to terminal color support)

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## Development

For development setup and guidelines, please refer to the [Contributing Guidelines](CONTRIBUTING.md).

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Style

The project uses:
- [Black](https://github.com/psf/black) for code formatting
- [isort](https://github.com/PyCQA/isort) for import sorting
- [flake8](https://github.com/PyCQA/flake8) for linting

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
