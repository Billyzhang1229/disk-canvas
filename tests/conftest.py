"""Common test fixtures for disk-canvas tests."""

import os

import pytest

from disk_canvas.disk_usage import ExtensionStyleManager, Node


@pytest.fixture
def mock_file_system(monkeypatch):
    """Fixture to mock file system operations."""

    def mock_isdir(path):
        return path.endswith("dir") or path.endswith("directory")

    def mock_getsize(path):
        # Return predictable sizes based on file extension
        if path.endswith(".py"):
            return 1000
        elif path.endswith(".txt"):
            return 500
        elif path.endswith(".jpg"):
            return 800
        else:
            return 100

    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    monkeypatch.setattr(os.path, "getsize", mock_getsize)


@pytest.fixture
def style_manager():
    """Fixture to provide a pre-configured ExtensionStyleManager."""
    esm = ExtensionStyleManager()
    esm.record_extension(".py", 1000)
    esm.record_extension(".txt", 500)
    esm.record_extension(".jpg", 800)
    esm.assign_styles(detailed=True)
    return esm


@pytest.fixture
def node_hierarchy():
    """Fixture to provide a pre-configured node hierarchy."""
    root = Node("root", "/fake/root")
    root.size = 2300  # Sum of all children

    child1 = Node("file1.py", "/fake/root/file1.py")
    child1.size = 1000

    child2 = Node("file2.txt", "/fake/root/file2.txt")
    child2.size = 500

    child3 = Node("file3.jpg", "/fake/root/file3.jpg")
    child3.size = 800

    root.children = [child1, child2, child3]
    return root


@pytest.fixture
def empty_canvas():
    """Fixture to provide an empty canvas for rendering tests."""
    width, height = 10, 5
    return [[{"char": " ", "color": ""} for _ in range(width)] for _ in range(height)]
