# disk-canvas

[![PyPI version](https://badge.fury.io/py/disk-canvas.svg)](https://badge.fury.io/py/disk-canvas)
[![Python Versions](https://img.shields.io/pypi/pyversions/disk-canvas.svg)](https://pypi.org/project/disk-canvas/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A command-line tool to visualize disk usage as a treemap-inspired ASCII mosaic. It scans a directory and produces a mosaic of uniformly sized, color-coded blocks based on file size and category. The visualization is designed to work on Linux and macOS.

## Features

- **ASCII Mosaic Visualization:** A terminal-friendly mosaic that offers a quick visual summary of disk usage.
- **Color-Coded Output:** Uses a modern Tailwind-inspired color palette.
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
disk-canvas /path/to/directory
```

Full options:

```bash
disk-canvas /path/to/directory [-t TOP] [-f] [-d DEPTH] [-D] [-U]
```

Options:

- `-t, --top`: Number of largest items per depth (default: 10)
- `-f, --files`: Show only files (exclude directories)
- `-d, --depth`: Maximum directory depth (default: 1)
- `-D, --detail`: Display a detailed legend with file extensions
- `-U, --unsort`: Use unsorted (treemap) canvas layout (default is sorted mosaic)

### Example Output

The tool provides:
1. A summary of total disk usage
2. A list of the largest files/directories
3. A visual representation of disk usage
4. A legend explaining the symbols and colors used

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
- `░` - Build files
- `☰` - Config files
- `.` - Other files

In simplified mode, similar categories share the same symbol for a cleaner view.

## Requirements

- Python 3.6 or higher
- Linux or macOS (Windows support is limited due to terminal color support)

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## Development

For development setup and guidelines, please refer to the [Contributing Guidelines](CONTRIBUTING.md).

### Running Tests

```bash
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
