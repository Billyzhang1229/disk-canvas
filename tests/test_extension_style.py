"""Tests for ExtensionStyleManager and Node classes."""

import os

import pytest

from disk_canvas.disk_usage import (
    ExtensionStyleManager,
    FileCategory,
    Node,
    get_category_for_extension,
)


def test_extension_style_manager_init():
    """Test that ExtensionStyleManager initializes with empty counters."""
    esm = ExtensionStyleManager()
    assert len(esm.ext_counts) == 0
    assert len(esm.ext_sizes) == 0
    assert len(esm.category_sizes) == 0
    assert len(esm.group_sizes) == 0
    assert len(esm.ext_styles) == 0
    assert len(esm.color_palette) > 0  # Should have the color palette


def test_record_extension():
    """Test that recording extensions updates counters correctly."""
    esm = ExtensionStyleManager()

    # Record a Python file
    esm.record_extension(".py", 100)
    assert esm.ext_counts[".py"] == 1
    assert esm.ext_sizes[".py"] == 100

    # Record another Python file
    esm.record_extension(".py", 200)
    assert esm.ext_counts[".py"] == 2
    assert esm.ext_sizes[".py"] == 300

    # Record a different extension
    esm.record_extension(".txt", 50)
    assert esm.ext_counts[".txt"] == 1
    assert esm.ext_sizes[".txt"] == 50

    # Check category sizes
    py_category = get_category_for_extension(".py")
    txt_category = get_category_for_extension(".txt")
    assert esm.category_sizes[py_category] == 300
    assert esm.category_sizes[txt_category] == 50


def test_assign_styles_non_detailed():
    """Test style assignment in non-detailed mode."""
    esm = ExtensionStyleManager()
    esm.record_extension(".py", 100)
    esm.record_extension(".txt", 50)

    esm.assign_styles(detailed=False)

    # In non-detailed mode, all files should have white color
    py_texture, py_color = esm.get_style(".py", FileCategory.CODE)
    txt_texture, txt_color = esm.get_style(".txt", FileCategory.DOCUMENT)

    assert py_color == "white"
    assert txt_color == "white"
    assert py_texture == "█"  # Code files use █ in simplified mode
    assert txt_texture == "○"  # Document files use ○ in simplified mode


def test_assign_styles_detailed():
    """Test style assignment in detailed mode."""
    esm = ExtensionStyleManager()
    esm.record_extension(".py", 100)
    esm.record_extension(".txt", 50)

    esm.assign_styles(detailed=True)

    # In detailed mode, files should have different colors
    py_texture, py_color = esm.get_style(".py", FileCategory.CODE)
    txt_texture, txt_color = esm.get_style(".txt", FileCategory.DOCUMENT)

    assert py_color != "white"
    assert txt_color != "white"
    assert py_color in esm.color_palette
    assert txt_color in esm.color_palette


def test_get_style_directory():
    """Test that directories get the correct style."""
    esm = ExtensionStyleManager()
    texture, color = esm.get_style("", FileCategory.OTHER, is_dir=True)
    assert texture == "."
    assert color == "white"


def test_node_initialization(monkeypatch):
    """Test Node initialization with a temporary file."""

    # Mock both isdir and exists
    def mock_isdir(path):
        return path.endswith("dir")

    def mock_exists(path):
        return not path.startswith("/nonexistent")

    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    monkeypatch.setattr(os.path, "exists", mock_exists)

    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        Node("test.py", "/nonexistent/test.py")

    # Test file node
    node = Node("test.py", "/fake/test.py")
    assert node.name == "test.py"
    assert node.path == "/fake/test.py"
    assert node.extension == ".py"
    assert not node.is_dir
    assert node.category == FileCategory.CODE

    # Test directory node
    dir_node = Node("testdir", "/fake/testdir")
    assert dir_node.name == "testdir"
    assert dir_node.path == "/fake/testdir"
    assert dir_node.extension == ""
    assert dir_node.is_dir
    assert dir_node.category == FileCategory.OTHER


def test_node_set_style(monkeypatch):
    """Test that Node.set_style sets the correct attributes."""

    def mock_isdir(path):
        return False

    def mock_exists(path):
        return True

    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    monkeypatch.setattr(os.path, "exists", mock_exists)

    node = Node("test.py", "/fake/test.py")
    esm = ExtensionStyleManager()
    esm.record_extension(".py", 100)
    esm.assign_styles(detailed=False)

    # Initially texture and color should be None
    assert node.texture is None
    assert node.color is None

    # After setting style they should be set
    node.set_style(esm)
    assert node.texture is not None
    assert node.color is not None
    assert node.color == "white"  # In non-detailed mode


def test_get_category_for_extension():
    """Test getting category for file extension."""
    from disk_canvas.disk_usage import get_category_for_extension
    from disk_canvas.disk_usage_constants import FileCategory

    assert get_category_for_extension(".py") == FileCategory.CODE
    assert get_category_for_extension(".ipynb") == FileCategory.NOTEBOOK
    assert get_category_for_extension(".csv") == FileCategory.DATA
    assert get_category_for_extension(".zip") == FileCategory.COMPRESSED
    assert get_category_for_extension(".pyc") == FileCategory.CACHE
    assert get_category_for_extension(".jpg") == FileCategory.IMAGE
    assert get_category_for_extension(".mp4") == FileCategory.VIDEO
    assert get_category_for_extension(".mp3") == FileCategory.AUDIO
    assert get_category_for_extension(".pdf") == FileCategory.DOCUMENT
    assert get_category_for_extension(".unknown") == FileCategory.OTHER
