"""Tests for disk_usage_constants.py."""

import pytest

from disk_canvas.disk_usage_constants import (
    CATEGORY_MAP,
    DEFAULT_TEXTURES,
    SIMPLIFIED_TEXTURES,
    Colors,
    FileCategory,
    hex_to_ansi,
)


def test_hex_to_ansi_valid():
    """Test that valid hex codes are converted correctly to ANSI escape sequences."""
    # Test with a known color from the palette
    ansi = hex_to_ansi("#636EFA")
    assert ansi.startswith("\033[38;2;")
    # Verify the RGB values are correct (99,110,250)
    assert ansi == "\033[38;2;99;110;250m"

    # Test with white
    ansi = hex_to_ansi("#FFFFFF")
    assert ansi == "\033[38;2;255;255;255m"


def test_hex_to_ansi_invalid():
    """Test that invalid hex codes raise ValueError."""
    with pytest.raises(ValueError):
        hex_to_ansi("#123")  # Too short
    with pytest.raises(ValueError):
        hex_to_ansi("#GGGGGG")  # Invalid hex characters


def test_colors_get_all_colors():
    """Test that Colors.get_all_colors() returns the expected dictionary."""
    colors = Colors.get_all_colors()

    # Check that we have all 10 color indices plus white
    for i in range(10):
        assert f"color{i}" in colors
    assert "white" in colors

    # Check that all values are ANSI escape sequences
    for color_code in colors.values():
        assert color_code.startswith("\033[38;2;")
        assert color_code.endswith("m")


def test_file_category_mapping():
    """Test that common file extensions map to the expected categories."""
    # Test some common file extensions
    assert CATEGORY_MAP[".py"] == FileCategory.CODE
    assert CATEGORY_MAP[".ipynb"] == FileCategory.NOTEBOOK
    assert CATEGORY_MAP[".csv"] == FileCategory.DATA
    assert CATEGORY_MAP[".zip"] == FileCategory.COMPRESSED
    assert CATEGORY_MAP[".jpg"] == FileCategory.IMAGE
    assert CATEGORY_MAP[".mp4"] == FileCategory.VIDEO
    assert CATEGORY_MAP[".mp3"] == FileCategory.AUDIO
    assert CATEGORY_MAP[".pdf"] == FileCategory.DOCUMENT
    assert CATEGORY_MAP[".pyc"] == FileCategory.CACHE


def test_texture_mappings():
    """Test that all file categories have corresponding textures."""
    # Test that every FileCategory has a texture in both maps
    for category in FileCategory:
        assert category in DEFAULT_TEXTURES
        assert category in SIMPLIFIED_TEXTURES

        # Verify textures are single characters
        assert len(DEFAULT_TEXTURES[category]) == 1
        assert len(SIMPLIFIED_TEXTURES[category]) == 1


def test_color_palette_consistency():
    """Test that the color palette is consistent with the number of colors."""
    # Check that PALETTE_HEX and COLOR_PALETTE have the same length
    assert len(Colors.PALETTE_HEX) == len(Colors.COLOR_PALETTE) - 1  # -1 for white

    # Check that all color keys in COLOR_PALETTE exist in _all_colors
    colors = Colors.get_all_colors()
    for color_key in Colors.COLOR_PALETTE:
        assert color_key in colors
