"""Test command line interface."""

import subprocess

import pytest

from disk_canvas.disk_usage import parse_args


def test_parse_args_defaults():
    """Test parsing command line arguments with defaults."""
    args = parse_args(["some/path"])
    assert args.dir == "some/path"
    assert not args.detail
    assert args.top == 10
    assert args.depth == 1
    assert not args.files
    assert not args.unsort


def test_parse_args_all_options():
    """Test parsing command line arguments with all options specified."""
    args = parse_args(
        [
            "some/path",
            "-D",  # detailed
            "-t",
            "20",  # top
            "-d",
            "3",  # depth
            "-f",  # files only
            "-U",  # unsorted
        ]
    )
    assert args.dir == "some/path"
    assert args.detail
    assert args.top == 20
    assert args.depth == 3
    assert args.files
    assert args.unsort


def test_parse_args_invalid_top():
    """Test that invalid --top values are rejected."""
    with pytest.raises(SystemExit):
        parse_args(["some/path", "-t", "0"])
    with pytest.raises(SystemExit):
        parse_args(["some/path", "-t", "-5"])


def test_parse_args_invalid_depth():
    """Test that invalid --depth values are rejected."""
    with pytest.raises(SystemExit):
        parse_args(["some/path", "-d", "-1"])


def test_cli_help(tmp_path):
    """Test that --help produces help output."""
    result = subprocess.run(
        ["python", "-m", "disk_canvas", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()
    assert "--detail" in result.stdout
    assert "--top" in result.stdout
    assert "--depth" in result.stdout
    assert "--files" in result.stdout
    assert "--unsort" in result.stdout


def test_cli_nonexistent_path():
    """Test that non-existent paths produce an error."""
    result = subprocess.run(
        ["python", "-m", "disk_canvas", "/nonexistent/path"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "error" in result.stdout.lower()


def test_cli_with_temp_directory(tmp_path):
    """Test running the CLI with a temporary directory."""
    # Create some test files
    (tmp_path / "file1.txt").write_text("hello")
    (tmp_path / "file2.py").write_text("print('world')")

    # Run disk-canvas on the temp directory
    result = subprocess.run(
        ["python", "-m", "disk_canvas", str(tmp_path)], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "file1.txt" in result.stdout
    assert "file2.py" in result.stdout


def test_cli_detail_mode(tmp_path):
    """Test running the CLI in detailed mode."""
    # Create test files
    (tmp_path / "file1.txt").write_text("hello")
    (tmp_path / "file2.py").write_text("print('world')")

    # Run disk-canvas with -D (detail)
    result = subprocess.run(
        ["python", "-m", "disk_canvas", str(tmp_path), "-D"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    # In detailed mode, we should see the extension legend
    assert "Extension Legend" in result.stdout


def test_cli_files_only(tmp_path):
    """Test running the CLI with --files option."""
    # Create a directory with files
    d = tmp_path / "subdir"
    d.mkdir()
    (d / "file1.txt").write_text("hello")
    (tmp_path / "file2.py").write_text("print('world')")

    # Run disk-canvas with -f (files only)
    result = subprocess.run(
        ["python", "-m", "disk_canvas", str(tmp_path), "-f"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    # Find the "Top N largest items" section
    output_lines = result.stdout.split("\n")
    top_items_start = next(
        i
        for i, line in enumerate(output_lines)
        if "Top" in line and "largest items" in line
    )
    top_items_end = (
        next(
            i
            for i, line in enumerate(output_lines[top_items_start:])
            if not line.strip()
        )
        + top_items_start
    )
    top_items_section = "\n".join(output_lines[top_items_start:top_items_end])

    # Directory should not be in the top items list
    assert "[DIR]" not in top_items_section
    assert "subdir" not in top_items_section
