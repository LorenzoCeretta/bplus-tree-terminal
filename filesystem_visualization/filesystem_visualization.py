# Script to visualize the filesystem as a tree
# Logic:
# 1. Get all file paths from the B+ tree
# 2. Split paths by "/"
# 3. Place nodes on a grid - leaves get x positions, parents go in the middle
# 4. Draw lines between parents and children
# 5. Color directories blue, files green

# This shows the logical filesystem structure, not the actual B+ tree internals
# The B+ tree stores all these paths as keys in leaf nodes at the same level

import matplotlib.pyplot as plt
from filesystem_visualization.filesystem_example import create_sample_filesystem


def draw_filesystem(vfs):
    """Draw the filesystem as a tree"""

    paths = vfs.tree.get_all_leaf_keys()
    if not paths:
        print("No files found")
        return

    # Build parent-child relationships
    children = {}
    for path in paths:
        if path == "/":
            continue

        # Find parent path
        if "/" in path[1:]:  # has subdirectories
            parent = "/" + "/".join(path[1:].split("/")[:-1])
        else:
            parent = "/"

        if parent not in children:
            children[parent] = []
        children[parent].append(path)

    # Position nodes
    positions = {}
    x_pos = 0

    def set_positions(node, level):
        nonlocal x_pos

        kids = children.get(node, [])
        if not kids:  # leaf node
            positions[node] = (x_pos, -level)
            x_pos += 2
            return

        # Position children first
        for kid in kids:
            set_positions(kid, level + 1)

        # Put parent in middle of children
        kid_x_positions = [positions[kid][0] for kid in kids]
        middle_x = sum(kid_x_positions) / len(kid_x_positions)
        positions[node] = (middle_x, -level)

    set_positions("/", 0)

    # Draw the tree
    plt.figure(figsize=(14, 8))
    plt.title("Filesystem Tree\n\nBlue = directories, Green = files")

    # Draw connections
    for parent, kids in children.items():
        parent_pos = positions[parent]
        for kid in kids:
            kid_pos = positions[kid]
            plt.plot(
                [parent_pos[0], kid_pos[0]],
                [parent_pos[1], kid_pos[1]],
                "k-",
                alpha=0.7,
            )

    # Draw nodes
    for path, pos in positions.items():
        name = path.split("/")[-1] if path != "/" else "root"
        node_info = vfs.tree.search_value(path)
        is_directory = node_info and node_info.get("type") == "dir"
        color = "lightblue" if is_directory else "lightgreen"

        plt.scatter(pos[0], pos[1], s=1000, c=color, edgecolors="black")
        plt.text(
            pos[0], pos[1], name, ha="center", va="center", fontsize=9, weight="bold"
        )

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(
        "filesystem_visualization/filesystem_tree.png", dpi=150, bbox_inches="tight"
    )
    print("File generated at filesystem_visualization/filesystem_tree.png")


if __name__ == "__main__":
    print("Creating filesystem...")
    fs = create_sample_filesystem()
    print("Drawing filesystem visualization...")
    draw_filesystem(fs)
