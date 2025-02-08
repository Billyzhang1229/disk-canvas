"""Test filesystem scanning functionality."""

import os

import pytest

from disk_canvas.disk_usage import (
    Node,
    ScanStats,
    filter_top_k_items,
    gather_items,
    human_readable_size,
)


@pytest.fixture
def temp_directory_structure(tmp_path):
    """Create a temporary directory structure for testing."""
    # Create main directory
    d = tmp_path / "test_dir"
    d.mkdir()

    # Create some files in the root
    (d / "file1.txt").write_text("hello")  # 5 bytes
    (d / "file2.py").write_text("print('world')")  # 13 bytes

    # Create a subdirectory
    sub = d / "subdir"
    sub.mkdir()
    (sub / "file3.txt").write_text("test content")  # 12 bytes
    (sub / "file4.py").write_text("def test(): pass")  # 15 bytes

    # Create a nested subdirectory
    nested = sub / "nested"
    nested.mkdir()
    (nested / "file5.txt").write_text("nested content")  # 14 bytes

    return d


def test_gather_items(temp_directory_structure, monkeypatch):
    """Test gathering items from a directory structure."""

    # Mock exists to always return True for our test files
    def mock_exists(path):
        return True

    # Mock getsize to return the actual size of our test files
    def mock_getsize(path):
        if path.endswith("file1.txt"):
            return 5  # len("hello")
        elif path.endswith("file2.py"):
            return 13  # len("print('world')")
        elif path.endswith("file3.txt"):
            return 12  # len("test content")
        elif path.endswith("file4.py"):
            return 15  # len("def test(): pass")
        elif path.endswith("file5.txt"):
            return 14  # len("nested content")
        return 0

    monkeypatch.setattr(os.path, "exists", mock_exists)
    monkeypatch.setattr(os.path, "getsize", mock_getsize)

    root = Node(temp_directory_structure.name, str(temp_directory_structure))
    stats = ScanStats()
    nodes = gather_items(root, stats)

    # We should have all the files and directories
    assert len(nodes) == 8  # root + 2 dirs + 5 files

    # Check that we found all files
    file_names = {node.name for node in nodes if not node.is_dir}
    assert file_names == {"file1.txt", "file2.py", "file3.txt", "file4.py", "file5.txt"}

    # Check directory sizes
    root_node = next(
        node for node in nodes if node.path == str(temp_directory_structure)
    )
    assert root_node.size == 59  # Sum of all file sizes (5 + 13 + 12 + 15 + 14)

    # Check that no errors occurred
    assert stats.long_paths_skipped == 0
    assert stats.permission_denied == 0
    assert stats.other_errors == 0


def test_gather_items_with_errors(tmp_path):
    """Test gathering items with permission errors."""
    d = tmp_path / "test_dir"
    d.mkdir()
    (d / "readable.txt").write_text("hello")

    # Create a directory with no read permissions
    no_access = d / "no_access"
    no_access.mkdir()
    os.chmod(no_access, 0o000)  # Remove all permissions

    root = Node(d.name, str(d))
    stats = ScanStats()
    gather_items(root, stats)  # We only care about stats, not items

    # Check that we recorded the permission error
    assert stats.permission_denied >= 1

    # Cleanup
    os.chmod(no_access, 0o755)  # Restore permissions for cleanup


def test_filter_top_k_items(monkeypatch):
    """Test filtering top K items by size."""

    # Mock file system operations
    def mock_isdir(path):
        return path.endswith("dir1") or path.endswith("dir2")

    def mock_exists(path):
        return True

    monkeypatch.setattr(os.path, "isdir", mock_isdir)
    monkeypatch.setattr(os.path, "exists", mock_exists)

    # Create a list of nodes with known sizes
    nodes = [
        Node("dir1", "/fake/dir1"),  # Directory
        Node("file1.txt", "/fake/file1.txt"),  # File
        Node("file2.py", "/fake/file2.py"),  # File
        Node("dir2", "/fake/dir2"),  # Directory
        Node("file3.txt", "/fake/file3.txt"),  # File
    ]

    # Set sizes
    nodes[0].size = 1000  # dir1
    nodes[1].size = 500  # file1.txt
    nodes[2].size = 800  # file2.py
    nodes[3].size = 300  # dir2
    nodes[4].size = 200  # file3.txt

    # Test 1: Get top 2 items including directories
    filtered = filter_top_k_items(
        sorted(nodes, key=lambda x: x.size, reverse=True), k=2
    )
    assert len(filtered) == 2
    assert filtered[0].size == 1000  # dir1
    assert filtered[1].size == 800  # file2.py

    # Test 2: Get top 2 items excluding directories
    filtered = filter_top_k_items(
        sorted(nodes, key=lambda x: x.size, reverse=True), k=2, exclude_dirs=True
    )
    assert len(filtered) == 2
    assert filtered[0].size == 800  # file2.py (largest file)
    assert filtered[1].size == 500  # file1.txt (second largest file)

    # Test 3: Get top 3 items with max_depth=0 (only root level)
    filtered = filter_top_k_items(
        sorted(nodes, key=lambda x: x.size, reverse=True), k=3, max_depth=0
    )
    assert all(node.depth == 0 for node in filtered)


def test_human_readable_size():
    """Test human readable size conversion."""
    assert human_readable_size(500) == "500.0B"
    assert human_readable_size(1024) == "1.0K"
    assert human_readable_size(1024 * 1024) == "1.0M"
    assert human_readable_size(1024 * 1024 * 1024) == "1.0G"
    assert human_readable_size(1024 * 1024 * 1024 * 1024) == "1.0T"


def test_gather_items_empty_dir(tmp_path):
    """Test scanning an empty directory."""
    from disk_canvas.disk_usage import Node, gather_items

    root = Node("test", str(tmp_path))
    items = gather_items(root)
    assert len(items) == 1
    assert items[0].size == 0


def test_gather_items_with_files(tmp_path):
    """Test scanning a directory with files."""
    from disk_canvas.disk_usage import Node, gather_items

    # Create test files
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("World")

    root = Node("test", str(tmp_path))
    items = gather_items(root)
    assert len(items) == 3  # root + 2 files
    assert items[0].size > 0


def test_gather_items_with_subdirs(tmp_path):
    """Test scanning a directory with subdirectories."""
    from disk_canvas.disk_usage import Node, gather_items

    # Create test structure
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("World")

    root = Node("test", str(tmp_path))
    items = gather_items(root)
    assert len(items) == 4  # root + subdir + 2 files
    assert any(item.is_dir for item in items)


def test_gather_items_permission_error(tmp_path):
    """Test handling of permission errors during scanning."""
    import os

    from disk_canvas.disk_usage import Node, ScanStats, gather_items

    # Create test structure
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file1.txt").write_text("Hello")
    os.chmod(subdir, 0o000)  # Remove all permissions

    try:
        root = Node("test", str(tmp_path))
        stats = ScanStats()
        gather_items(root, stats)  # We only care about stats, not items
        assert stats.permission_denied > 0
    finally:
        os.chmod(subdir, 0o755)  # Restore permissions
