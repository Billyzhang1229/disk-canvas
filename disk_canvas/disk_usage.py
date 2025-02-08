#!/usr/bin/env python3
"""Main module for disk-canvas visualization."""

import argparse
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

from .disk_usage_constants import (
    CATEGORY_MAP,
    CATEGORY_TO_GROUP,
    DEFAULT_TEXTURES,
    LEGEND_ORDER,
    LEGEND_STYLES,
    SIMPLIFIED_TEXTURES,
    Colors,
    FileCategory,
)


@dataclass
class Rectangle:
    """Represents a rectangular region in the visualization."""

    x: int
    y: int
    width: int
    height: int


def get_category_for_extension(ext: str) -> FileCategory:
    """Get the file category for a given file extension.

    Args:
        ext: The file extension (including the dot)

    Returns:
        The FileCategory enum value for the extension
    """
    return CATEGORY_MAP.get(ext.lower(), FileCategory.OTHER)


def get_simplified_texture(category: FileCategory) -> str:
    """Get the simplified texture character for a file category.

    Args:
        category: The FileCategory enum value

    Returns:
        A single character representing the category
    """
    return SIMPLIFIED_TEXTURES.get(category, "■")


class ExtensionStyleManager:
    """Manages the visual styles (textures and colors) for file extensions."""

    def __init__(self):
        """Initialize the extension style manager."""
        self.ext_counts = defaultdict(int)
        self.ext_sizes = defaultdict(int)
        self.category_sizes = defaultdict(int)
        self.group_sizes = defaultdict(int)
        self.ext_styles = {}
        self.color_palette = Colors.COLOR_PALETTE

    def record_extension(self, ext: str, size: int):
        """Record a file extension and its size.

        Args:
            ext: The file extension (including the dot)
            size: The size of the file in bytes
        """
        if ext:
            ext = ext.lower()
            self.ext_counts[ext] += 1
            self.ext_sizes[ext] += size
            category = get_category_for_extension(ext)
            self.category_sizes[category] += size
            group = CATEGORY_TO_GROUP[category]
            self.group_sizes[group] += size

    def assign_styles(self, detailed: bool = False):
        """Assign visual styles to file extensions.

        Args:
            detailed: Whether to use detailed mode with more colors
        """
        sorted_exts = sorted(self.ext_counts.items(), key=lambda x: (-x[1], x[0]))
        group_color_indices = defaultdict(int)
        for ext, _ in sorted_exts:
            category = get_category_for_extension(ext)
            group = CATEGORY_TO_GROUP[category]
            if detailed:
                texture = DEFAULT_TEXTURES[category]
                color_idx = group_color_indices[group]
                color = self.color_palette[color_idx % len(self.color_palette)]
                group_color_indices[group] += 1
            else:
                texture = SIMPLIFIED_TEXTURES[category]
                color = "white"
            self.ext_styles[ext.lower()] = (texture, color)

    def get_style(
        self, ext: str, category: FileCategory, is_dir: bool = False
    ) -> Tuple[str, str]:
        """Get the visual style for a file extension.

        Args:
            ext: The file extension (including the dot)
            category: The FileCategory enum value
            is_dir: Whether the item is a directory

        Returns:
            A tuple of (texture, color)
        """
        if is_dir:
            return ".", "white"
        ext = ext.lower()
        if ext in self.ext_styles:
            return self.ext_styles[ext]
        texture = get_simplified_texture(category)
        return texture, "white"


class Node:
    """Represents a file or directory in the filesystem tree."""

    def __init__(self, name: str, path: str, depth: int = 0):
        """Initialize a node.

        Args:
            name: The name of the file or directory
            path: The full path to the file or directory
            depth: The depth in the filesystem tree
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path does not exist: {path}")
        self.name = name
        self.path = path
        self.size = 0
        self.children: List[Node] = []
        self.depth = depth
        self.is_dir = os.path.isdir(path)
        # Handle files without extensions
        if not self.is_dir:
            self.extension = os.path.splitext(path)[1].lower()
            self.category = get_category_for_extension(self.extension)
        else:
            self.extension = ""
            self.category = FileCategory.OTHER
        self.color = None
        self.texture = None

    def set_style(self, style_manager: ExtensionStyleManager, detailed: bool = False):
        """Set the visual style for this node.

        Args:
            style_manager: The ExtensionStyleManager instance
            detailed: Whether to use detailed mode
        """
        self.texture, self.color = style_manager.get_style(
            self.extension, self.category, self.is_dir
        )


@dataclass
class ScanStats:
    """Statistics collected during filesystem scanning."""

    long_paths_skipped: int = 0
    permission_denied: int = 0
    other_errors: int = 0


def gather_items(root: Node, stats: ScanStats = None) -> List[Node]:
    """Gather all files and directories under a root node.

    Args:
        root: The root Node to start from
        stats: Optional ScanStats to collect scanning statistics

    Returns:
        List of all nodes in the tree
    """
    if stats is None:
        stats = ScanStats()
    stack = [root]
    nodes = []
    while stack:
        node = stack.pop()
        nodes.append(node)
        if node.is_dir:
            try:
                with os.scandir(node.path) as it:
                    for entry in it:
                        try:
                            child = Node(entry.name, entry.path, node.depth + 1)
                            node.children.append(child)
                            stack.append(child)
                        except OSError as e:
                            if e.errno == 63:
                                stats.long_paths_skipped += 1
                            else:
                                stats.other_errors += 1
            except PermissionError:
                stats.permission_denied += 1

    # Calculate sizes - directories don't contribute to size
    for node in reversed(nodes):
        if node.is_dir:
            # Directory size is sum of children's sizes but doesn't contribute to parent
            node.size = sum(child.size for child in node.children)
        else:
            try:
                node.size = os.path.getsize(node.path)
            except OSError:
                node.size = 0
    return nodes


def filter_top_k_items(
    sorted_items: List[Node], k: int, exclude_dirs: bool = False, max_depth: int = 1
) -> List[Node]:
    """Filter and return the top K largest items.

    Args:
        sorted_items: List of nodes to filter
        k: Number of items to return
        exclude_dirs: Whether to exclude directories
        max_depth: Maximum depth to consider

    Returns:
        List of the top K largest items
    """
    filtered = []
    for item in sorted_items:
        if item.depth > max_depth:
            continue
        if exclude_dirs and item.is_dir:
            continue
        filtered.append(item)

    filtered.sort(key=lambda x: x.size, reverse=True)
    return filtered[:k]


def print_top_k_largest(
    items: List[Node], k: int, exclude_dirs: bool = False, max_depth: int = 1
):
    """Print information about the top K largest items.

    Args:
        items: List of all nodes
        k: Number of items to show
        exclude_dirs: Whether to exclude directories
        max_depth: Maximum depth to consider
    """
    sorted_items = sorted(items, key=lambda x: x.size, reverse=True)
    filtered_items = filter_top_k_items(sorted_items, k, exclude_dirs, max_depth)
    if not filtered_items:
        print(f"\nNo items found within depth {max_depth}.")
        return
    max_path_len = max(len(os.path.relpath(item.path)) for item in filtered_items)
    print(f"\nTop {k} largest items (max depth: {max_depth}):")
    header = (
        f"{'Size':>10} {'Type':<6} {'Depth':<6} "
        f"{'Category':<12} {'Path':<{max_path_len}}"
    )
    print(header)
    print("-" * (10 + 6 + 6 + 12 + max_path_len + 4))
    for item in filtered_items:
        size_str = human_readable_size(item.size)
        item_type = "[DIR]" if item.is_dir else "[FILE]"
        # Always show the category, even for files without extensions
        category = item.category.name
        rel_path = os.path.relpath(item.path)
        line = (
            f"{size_str:>10} {item_type:<6} {item.depth:<6} "
            f"{category:<12} {rel_path}"
        )
        print(line)
    print()


def print_detailed_legend(style_manager: ExtensionStyleManager, detailed: bool = False):
    """Print a legend explaining the visualization symbols.

    Args:
        style_manager: The ExtensionStyleManager instance
        detailed: Whether to show detailed extension information
    """
    if detailed:
        print("\nDetailed Extension Legend:")
        by_category = defaultdict(list)
        for ext, count in style_manager.ext_counts.items():
            category = get_category_for_extension(ext)
            by_category[category].append((ext, count))
        for category in FileCategory:
            if category in by_category:
                cat_size = style_manager.category_sizes[category]
                print(f"\n{category.name} files: ({human_readable_size(cat_size)})")
                exts = by_category[category]
                exts.sort(key=lambda x: (-style_manager.ext_sizes[x[0]], x[0]))
                for ext, count in exts:
                    texture, color = style_manager.get_style(ext, category)
                    color_code = Colors.get_all_colors()[color]
                    ext_size = style_manager.ext_sizes[ext]
                    line = (
                        f"  {color_code}{texture} {ext:8}{Colors.RESET} "
                        f"({count} files, {human_readable_size(ext_size)})"
                    )
                    print(line)
    else:
        print("\nLarge Categories:")
        for group, desc in LEGEND_ORDER:
            symbol = LEGEND_STYLES[group]["symbol"]
            color_code = Colors.get_all_colors()[LEGEND_STYLES[group]["color"]]
            size_val = style_manager.group_sizes.get(group, 0)
            line = (
                f"{color_code}{symbol}{Colors.RESET} - {desc} "
                f"({human_readable_size(size_val)})"
            )
            print(line)


def create_treemap(node: Node, rect: Rectangle, canvas: List[List[Dict]]):
    """Create a treemap visualization of the filesystem tree.

    Args:
        node: The root node to visualize
        rect: The rectangle to draw in
        canvas: The canvas to draw on
    """
    # Only fill non-directory nodes
    if not node.is_dir:
        fill_rectangle(canvas, rect, node.texture, Colors.get_all_colors()[node.color])
    if not node.children:
        return

    # Filter out empty children and get total size of non-empty children
    valid_children = [child for child in node.children if child.size > 0]
    if not valid_children:
        return

    # Sort children by size
    valid_children.sort(key=lambda x: x.size, reverse=True)
    total_size = sum(child.size for child in valid_children)
    if total_size == 0:
        return

    # Determine split direction based on rectangle dimensions
    split_horizontal = rect.width > rect.height
    current_position = 0

    # Distribute space proportionally to children
    for child in valid_children:
        proportion = child.size / total_size
        if split_horizontal:
            width = max(1, int(rect.width * proportion))
            child_rect = Rectangle(
                rect.x + current_position, rect.y, width, rect.height
            )
            current_position += width
        else:
            height = max(1, int(rect.height * proportion))
            child_rect = Rectangle(
                rect.x, rect.y + current_position, rect.width, height
            )
            current_position += height
        create_treemap(child, child_rect, canvas)


def fill_rectangle(canvas: List[List[Dict]], rect: Rectangle, char: str, color: str):
    """Fill a rectangle on the canvas with a character and color.

    Args:
        canvas: The canvas to draw on
        rect: The rectangle to fill
        char: The character to use
        color: The color to use
    """
    for y in range(rect.y, rect.y + rect.height):
        if y >= len(canvas):
            continue
        for x in range(rect.x, rect.x + rect.width):
            if x >= len(canvas[y]):
                continue
            canvas[y][x] = {"char": char, "color": color}


def print_canvas(canvas: List[List[Dict]]):
    """Print the visualization canvas to the terminal.

    Args:
        canvas: The canvas to print
    """
    reset = Colors.RESET
    lines = []
    for row in canvas:
        line = "".join(f"{cell['color']}{cell['char']}{reset}" for cell in row)
        lines.append(line)
    print("\n".join(lines))


def get_terminal_size() -> Tuple[int, int]:
    """Get the current terminal size.

    Returns:
        A tuple of (width, height)
    """
    try:
        ts = os.get_terminal_size()
        return ts.columns, ts.lines - 2
    except OSError:
        return 80, 24


def human_readable_size(size: int) -> str:
    """Convert a size in bytes to a human-readable string.

    Args:
        size: The size in bytes

    Returns:
        A human-readable size string (e.g., "1.5M")
    """
    for unit in ["B", "K", "M", "G", "T"]:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}P"


def print_scan_summary(stats: ScanStats):
    """Print a summary of filesystem scanning statistics.

    Args:
        stats: The ScanStats instance
    """
    if stats.long_paths_skipped or stats.permission_denied or stats.other_errors:
        print("\nScan Summary:")
        if stats.long_paths_skipped:
            print(
                f"- {stats.long_paths_skipped} items skipped due to path length limits"
            )
        if stats.permission_denied:
            print(f"- {stats.permission_denied} items skipped due to permission denied")
        if stats.other_errors:
            print(f"- {stats.other_errors} items skipped due to other errors")
        print()


def render_sorted_canvas(
    width: int, height: int, style_manager: ExtensionStyleManager
) -> List[List[Dict]]:
    """Render a sorted mosaic visualization.

    Args:
        width: Canvas width
        height: Canvas height
        style_manager: The ExtensionStyleManager instance

    Returns:
        The rendered canvas
    """
    total_cells = width * height
    # Only use file sizes, not directory sizes
    total_bytes = sum(style_manager.ext_sizes.values())
    if total_bytes == 0:
        total_bytes = 1
    sorted_styles = []
    for category in FileCategory:
        ext_list = [
            (ext, style_manager.ext_sizes[ext])
            for ext in style_manager.ext_counts
            if get_category_for_extension(ext) == category
        ]
        if not ext_list:
            continue
        ext_list.sort(key=lambda x: (-x[1], x[0]))
        for ext, size in ext_list:
            style = style_manager.get_style(ext, category, is_dir=False)
            sorted_styles.append((style, size))
    cell_list = []
    allocated_cells = 0
    for style, size in sorted_styles:
        fraction = size / total_bytes
        num_cells = round(fraction * total_cells)
        cell_list.extend(
            [{"char": style[0], "color": Colors.get_all_colors()[style[1]]}] * num_cells
        )
        allocated_cells += num_cells
    if allocated_cells < total_cells:
        cell_list.extend(
            [{"char": " ", "color": Colors.RESET}] * (total_cells - allocated_cells)
        )
    else:
        cell_list = cell_list[:total_cells]
    new_canvas = [[None for _ in range(width)] for _ in range(height)]
    for idx, cell in enumerate(cell_list):
        row = idx % height
        col = idx // height
        if col < width:
            new_canvas[row][col] = cell
    for r in range(height):
        for c in range(width):
            if new_canvas[r][c] is None:
                new_canvas[r][c] = {"char": " ", "color": Colors.RESET}
    return new_canvas


def parse_args(args=None):
    """Parse command line arguments.

    Args:
        args: Optional list of command line arguments

    Returns:
        The parsed arguments
    """
    parser = argparse.ArgumentParser(description="Disk Usage Visualization")
    parser.add_argument("dir", help="Directory to analyze")
    parser.add_argument(
        "-t",
        "--top",
        type=int,
        default=10,
        help="Number of largest items per depth (default: 10)",
    )
    parser.add_argument(
        "-f",
        "--files",
        action="store_true",
        help="Show only files (exclude directories)",
    )
    parser.add_argument(
        "-d", "--depth", type=int, default=1, help="Max directory depth (default: 1)"
    )
    parser.add_argument(
        "-D", "--detail", action="store_true", help="Display detailed legend"
    )
    parser.add_argument(
        "-U",
        "--unsort",
        action="store_true",
        help="Use unsorted (treemap) canvas (default is sorted)",
    )

    args = parser.parse_args(args)
    if args.top <= 0:
        parser.error("--top must be positive")
    if args.depth < 0:
        parser.error("--depth must be non-negative")
    return args


def main():
    """Run the disk-canvas visualization tool."""
    args = parse_args()
    if not os.path.exists(args.dir):
        print(f"Error: Path '{args.dir}' does not exist")
        sys.exit(1)
    root = Node(os.path.basename(args.dir), os.path.abspath(args.dir))
    stats = ScanStats()
    try:
        items = gather_items(root, stats=stats)
        if not items:
            print("Error: No items could be processed in the directory")
            sys.exit(1)
    except Exception as e:
        print(f"Error scanning directory: {e}")
        sys.exit(1)
    style_manager = ExtensionStyleManager()
    for item in items:
        if not item.is_dir:
            style_manager.record_extension(item.extension, item.size)
    style_manager.assign_styles(detailed=args.detail)
    for item in items:
        item.set_style(style_manager, detailed=args.detail)
    term_width, term_height = get_terminal_size()
    canvas = [
        [{"char": " ", "color": Colors.RESET} for _ in range(term_width)]
        for _ in range(term_height)
    ]
    print(f"\nDisk Usage Visualization for: {root.path}")
    print(f"Total size: {human_readable_size(root.size)}")
    print_scan_summary(stats)
    print_top_k_largest(items, args.top, args.files, args.depth)
    if args.unsort:
        create_treemap(root, Rectangle(0, 0, term_width, term_height), canvas)
    else:
        canvas = render_sorted_canvas(term_width, term_height, style_manager)
    print_canvas(canvas)
    print_detailed_legend(style_manager, detailed=args.detail)


if __name__ == "__main__":
    main()
