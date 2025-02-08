# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-02-08

### Fixed
- Removed `argparse` from dependencies as it's part of Python's standard library
- Fixed package installation issues on TestPyPI and PyPI

### Added
- Organized release notes into dedicated directory structure
- Added automated PyPI publishing workflow via GitHub Actions

### Development
- Added GitHub Actions workflow for automated package publishing
- Added support for both TestPyPI and PyPI deployments
- Improved development documentation

## [0.1.0] - 2025-02-08

### Added
- Initial release
- ASCII mosaic visualization of disk usage
- Color-coded output with modern Tailwind-inspired color palette
- Multiple visualization modes (detailed and simplified)
- Smart file categorization system
- Support for Linux and macOS
- Command-line interface with various options
- Configurable depth and file filtering
- Sorted mosaic and treemap-style layouts
