"""Test rendering functionality."""

import os

from disk_canvas.disk_usage import (
    ExtensionStyleManager,
    Node,
    Rectangle,
    create_treemap,
    fill_rectangle,
    render_sorted_canvas,
)
from disk_canvas.disk_usage_constants import Colors


def test_rectangle_creation():
    """Test Rectangle dataclass initialization."""
    rect = Rectangle(x=1, y=2, width=10, height=5)
    assert rect.x == 1
    assert rect.y == 2
    assert rect.width == 10
    assert rect.height == 5


def test_fill_rectangle():
    """Test filling a rectangle on the canvas."""
    canvas = [
        [{"char": " ", "color": Colors.RESET} for _ in range(5)] for _ in range(5)
    ]
    rect = Rectangle(1, 1, 2, 2)
    fill_rectangle(canvas, rect, "X", Colors.get_all_colors()["color0"])
    # Check the filled area
    assert canvas[1][1]["char"] == "X"
    assert canvas[1][2]["char"] == "X"
    assert canvas[2][1]["char"] == "X"
    assert canvas[2][2]["char"] == "X"
    # Check the border is unchanged
    assert canvas[0][0]["char"] == " "
    assert canvas[0][4]["char"] == " "
    assert canvas[4][0]["char"] == " "
    assert canvas[4][4]["char"] == " "


def test_create_treemap(monkeypatch):
    """Test creating a treemap from a node hierarchy."""

    # Mock file system operations
    def mock_isdir(path):
        return path.endswith("root")

    def mock_exists(path):
        return True

    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    monkeypatch.setattr(os.path, "exists", mock_exists)

    # Create a canvas
    width, height = 10, 5
    canvas = [[{"char": " ", "color": ""} for _ in range(width)] for _ in range(height)]

    # Create a simple node hierarchy
    root = Node("root", "/fake/root")
    root.size = 1000
    root.texture = "█"
    root.color = "white"

    child1 = Node("child1", "/fake/root/child1")
    child1.size = 600
    child1.texture = "▓"
    child1.color = "color0"

    child2 = Node("child2", "/fake/root/child2")
    child2.size = 400
    child2.texture = "▒"
    child2.color = "color1"

    root.children = [child1, child2]

    # Create the treemap
    rect = Rectangle(0, 0, width, height)
    create_treemap(root, rect, canvas)

    # Check that the canvas was filled
    filled_cells = sum(1 for row in canvas for cell in row if cell["char"] != " ")
    assert filled_cells == width * height  # All cells should be filled


def test_render_sorted_canvas():
    """Test rendering a sorted canvas with extension styles."""
    # Create a style manager with some recorded extensions
    esm = ExtensionStyleManager()
    esm.record_extension(".py", 1000)
    esm.record_extension(".txt", 500)
    esm.record_extension(".jpg", 300)
    esm.assign_styles(detailed=True)

    # Render a small canvas
    width, height = 8, 4
    canvas = render_sorted_canvas(width, height, esm)

    # Verify canvas dimensions
    assert len(canvas) == height
    assert all(len(row) == width for row in canvas)

    # Verify that all cells have valid content
    for row in canvas:
        for cell in row:
            assert "char" in cell
            assert "color" in cell
            assert cell["char"] != " "  # No empty cells
            assert cell["color"].startswith("\033[")  # Valid ANSI color


def test_render_sorted_canvas_empty():
    """Test rendering a canvas with no recorded extensions."""
    esm = ExtensionStyleManager()
    width, height = 5, 3
    canvas = render_sorted_canvas(width, height, esm)

    # Canvas should still be created with the correct dimensions
    assert len(canvas) == height
    assert all(len(row) == width for row in canvas)

    # All cells should be empty or have reset color
    for row in canvas:
        for cell in row:
            assert cell["char"] == " "
            assert cell["color"] in ["", Colors.RESET]


def test_render_sorted_canvas_single_extension():
    """Test rendering a canvas with a single extension type."""
    esm = ExtensionStyleManager()
    esm.record_extension(".py", 1000)
    esm.assign_styles(detailed=True)

    width, height = 6, 3
    canvas = render_sorted_canvas(width, height, esm)

    # All cells should have the same character and color
    first_cell = canvas[0][0]
    for row in canvas:
        for cell in row:
            assert cell["char"] == first_cell["char"]
            assert cell["color"] == first_cell["color"]
