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
from matplotlib.patches import Ellipse
from filesystem_visualization.filesystem_example import create_sample_filesystem
from bplus_tree import InternalNode, LeafNode


def collect_bplustree_structure(tree):
    """
    Traverse the B+ tree and collect all nodes (internal and leaves),
    their keys, children, and depth. Returns a dict of node_id -> node dict.
    """
    nodes = {}
    node_id_counter = [0]

    def traverse(node, depth, parent_id=None):
        node_id = node_id_counter[0]
        node_id_counter[0] += 1
        node_type = "internal" if isinstance(node, InternalNode) else "leaf"
        node_dict = {
            "id": node_id,
            "type": node_type,
            "keys": list(node.keys),
            "depth": depth,
            "parent": parent_id,
            "children": [],
            "node": node,
        }
        nodes[node_id] = node_dict
        if node_type == "internal":
            for child in node.children:
                child_id = traverse(child, depth + 1, node_id)
                node_dict["children"].append(child_id)
        return node_id

    traverse(tree.root, 0)
    return nodes


def get_dir_children(vfs, dir_path):
    """
    Return the children (files/dirs) of a directory path in the virtual filesystem.
    """
    all_keys = vfs.tree.get_all_leaf_keys()
    children = []
    prefix = dir_path.rstrip("/") + "/" if dir_path != "/" else "/"
    for k in all_keys:
        if k == dir_path:
            continue
        if k.startswith(prefix):
            rest = k[len(prefix):]
            if "/" not in rest:
                children.append(k)
    return children


def collect_dircentric_nodes(vfs, nodes, dir_path, depth, parent_id=None, level_nodes=None, edges=None):
    """
    First pass: Recursively collect all nodes in directory-centric order, grouped by depth.
    Returns: level_nodes (dict: depth -> list of (node_id, label, type)), edges (list of (parent_id, child_id))
    """
    if level_nodes is None:
        level_nodes = {}
    if edges is None:
        edges = []
    # DIR node
    dir_node_id = f"dir:{dir_path}"
    label = dir_path.split("/")[-1] or "root"
    level_nodes.setdefault(depth, []).append((dir_node_id, label, "dir"))
    if parent_id is not None:
        edges.append((parent_id, dir_node_id))
    # Internal node(s) for this DIR
    children = get_dir_children(vfs, dir_path)
    internal_ids = []
    if children:
        first_child = children[0]
        current = vfs.tree.root
        while isinstance(current, InternalNode):
            idx = 0
            for i, key in enumerate(current.keys):
                if first_child < key:
                    idx = i
                    break
                idx = i + 1
            internal_id = None
            for nid, n in nodes.items():
                if n["node"] is current:
                    internal_id = nid
                    break
            if internal_id is not None:
                int_label = str(current.keys)
                int_node_id = f"internal:{internal_id}:{dir_path}"
                level_nodes.setdefault(depth + 1, []).append((int_node_id, int_label, "internal"))
                edges.append((dir_node_id, int_node_id))
                internal_ids.append(int_node_id)
            current = current.children[idx]
    parent_for_leaves = internal_ids[-1] if internal_ids else dir_node_id
    # Children (files/dirs)
    for child in children:
        val = vfs.tree.search_value(child)
        if val and val.get("type") == "dir":
            collect_dircentric_nodes(vfs, nodes, child, depth + 2, parent_for_leaves, level_nodes, edges)
        else:
            file_node_id = f"file:{child}"
            file_label = child.split("/")[-1]
            level_nodes.setdefault(depth + 2, []).append((file_node_id, file_label, "file"))
            edges.append((parent_for_leaves, file_node_id))
    return level_nodes, edges


def assign_level_aligned_positions(level_nodes, x_spacing=20, y_spacing=3):
    """
    Second pass: Assign x, y positions so all nodes at the same level are aligned horizontally.
    Returns: positions dict: node_id -> (x, y)
    """
    positions = {}
    max_width = max(len(nodes) for nodes in level_nodes.values())
    for depth, nodes_at_level in level_nodes.items():
        y = -depth * y_spacing
        n = len(nodes_at_level)
        # Center nodes at each level
        start_x = -((n - 1) * x_spacing) / 2
        for i, (node_id, _, _) in enumerate(nodes_at_level):
            x = start_x + i * x_spacing
            positions[node_id] = (x, y)
    return positions


def draw_filesystem_level_aligned(vfs):
    tree = vfs.tree
    nodes = collect_bplustree_structure(tree)
    # First pass: collect nodes by level and edges
    level_nodes, edges = collect_dircentric_nodes(vfs, nodes, "/", 0)
    # Second pass: assign positions
    positions = assign_level_aligned_positions(level_nodes)
    plt.figure(figsize=(18, 8))
    ax = plt.gca()
    plt.title("Filesystem Structure (Level-Aligned Layout)\n\nBlue = directories, Green = files, Gray = internal nodes")
    # Draw edges
    for src, dst in edges:
        if src in positions and dst in positions:
            src_pos = positions[src]
            dst_pos = positions[dst]
            plt.plot([src_pos[0], dst_pos[0]], [src_pos[1], dst_pos[1]], "k-", alpha=0.7)
    # Draw nodes as ellipses
    for depth, nodes_at_level in level_nodes.items():
        for node_id, label, ntype in nodes_at_level:
            pos = positions[node_id]
            if ntype == "dir":
                color = "lightblue"
            elif ntype == "file":
                color = "lightgreen"
            else:
                color = "lightgray"
            n_lines = label.count("\n") + 1
            max_line_len = max((len(line) for line in label.split("\n")), default=1)
            # Ellipse width and height
            width = 0.45 * max(10, max_line_len)
            height = 0.9 * n_lines
            ellipse = Ellipse(
                xy=pos,
                width=width,
                height=height,
                facecolor=color,
                edgecolor="black",
                zorder=3,
            )
            ax.add_patch(ellipse)
            plt.text(
                pos[0], pos[1], label, ha="center", va="center", fontsize=6, weight="bold", wrap=True
            )
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("filesystem_visualization/filesystem_tree.png", dpi=150, bbox_inches="tight")
    print("File generated at filesystem_visualization/filesystem_tree.png")


if __name__ == "__main__":
    print("Creating filesystem...")
    fs = create_sample_filesystem()
    print("Drawing level-aligned filesystem visualization...")
    draw_filesystem_level_aligned(fs)
