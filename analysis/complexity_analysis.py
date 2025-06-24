import time
import matplotlib.pyplot as plt
import numpy as np
from bplus_tree import BPlusTree
import math


class BPlusTreeComplexityAnalysis:
    """
    Class to analyze and visualize the time complexity of B+ tree operations.
    """

    def __init__(self):
        self.results = {}

    def measure_operation_time(self, operation_func, data_sizes, tree_order=4):
        """
        Measure execution time for different data sizes.
        """
        times = []

        for size in data_sizes:
            # Create a fresh tree for each test
            tree = BPlusTree(tree_order)

            # Prepare data if needed
            if operation_func.__name__ == "test_search":
                # Insert data first for search operations
                for i in range(size):
                    tree.insert(i, f"value_{i}")

            # Measure operation time
            start_time = time.time()
            operation_func(tree, size)
            end_time = time.time()

            times.append(end_time - start_time)

        return times

    def test_insert(self, tree, size):
        """Test insertion operation"""
        for i in range(size):
            tree.insert(i, f"value_{i}")

    def test_search(self, tree, size):
        """Test search operation"""
        for i in range(size):
            tree.search_value(i)

    def test_search_missing(self, tree, size):
        """Test search for non-existent keys"""
        for i in range(size):
            tree.search_value(size + i)  # Search for keys that don't exist

    def test_range_query(self, tree, size):
        """Test range query operation"""
        # Insert data first
        for i in range(size):
            tree.insert(i, f"value_{i}")

        # Perform range queries
        for i in range(0, size, max(1, size // 10)):
            end = min(i + size // 10, size)
            tree.range_query(i, end)

    def test_delete(self, tree, size):
        """Test deletion operation"""
        # Insert data first
        for i in range(size):
            tree.insert(i, f"value_{i}")

        # Delete half the keys
        for i in range(0, size, 2):
            tree.delete(i)

    def analyze_complexities(self):
        """
        Analyze and plot the time complexity of all B+ tree operations.
        """
        # Data sizes to test (logarithmic scale for better visualization)
        data_sizes = [10, 50, 100, 500, 1000, 2000, 5000]

        # Define operations to test
        operations = {
            "Insert": self.test_insert,
            "Search (existing)": self.test_search,
            "Search (missing)": self.test_search_missing,
            "Range Query": self.test_range_query,
            "Delete": self.test_delete,
        }

        # Measure times for each operation
        for op_name, op_func in operations.items():
            print(f"Measuring {op_name}...")
            times = self.measure_operation_time(op_func, data_sizes)
            self.results[op_name] = {"sizes": data_sizes, "times": times}

        # Create the complexity analysis plot
        self.plot_complexity_analysis()

        # Create theoretical vs actual comparison
        self.plot_theoretical_vs_actual()

    def plot_complexity_analysis(self):
        """
        Plot the time complexity analysis for all operations.
        """
        plt.figure(figsize=(15, 10))

        # Create subplots for different operations
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()

        # Color scheme for operations
        colors = ["blue", "green", "red", "orange", "purple"]

        for i, (op_name, data) in enumerate(self.results.items()):
            ax = axes[i]

            # Plot actual measurements
            ax.plot(
                data["sizes"],
                data["times"],
                "o-",
                color=colors[i],
                label=f"{op_name} (Actual)",
                linewidth=2,
                markersize=6,
            )

            # Add theoretical complexity curves
            sizes = np.array(data["sizes"])

            if op_name == "Insert":
                # O(log n) for insertion
                theoretical = np.log(sizes) * (data["times"][-1] / np.log(sizes[-1]))
                ax.plot(
                    sizes, theoretical, "--", color="gray", label="O(log n)", alpha=0.7
                )

            elif op_name in ["Search (existing)", "Search (missing)"]:
                # O(log n) for search
                theoretical = np.log(sizes) * (data["times"][-1] / np.log(sizes[-1]))
                ax.plot(
                    sizes, theoretical, "--", color="gray", label="O(log n)", alpha=0.7
                )

            elif op_name == "Range Query":
                # O(log n + k) where k is the range size
                # For this test, k is proportional to n, so O(n)
                theoretical = sizes * (data["times"][-1] / sizes[-1])
                ax.plot(sizes, theoretical, "--", color="gray", label="O(n)", alpha=0.7)

            elif op_name == "Delete":
                # O(log n) for deletion
                theoretical = np.log(sizes) * (data["times"][-1] / np.log(sizes[-1]))
                ax.plot(
                    sizes, theoretical, "--", color="gray", label="O(log n)", alpha=0.7
                )

            ax.set_xlabel("Data Size (n)")
            ax.set_ylabel("Time (seconds)")
            ax.set_title(f"{op_name} - Time Complexity")
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_xscale("log")
            ax.set_yscale("log")

        # Remove the last unused subplot
        axes[-1].set_visible(False)

        plt.tight_layout()
        plt.savefig(
            "analysis/bplus_tree_complexity_analysis.png", dpi=300, bbox_inches="tight"
        )
        plt.show()

    def plot_theoretical_vs_actual(self):
        """
        Create a comprehensive comparison of theoretical vs actual complexities.
        """
        plt.figure(figsize=(16, 12))

        # Define theoretical complexities
        theoretical_complexities = {
            "Insert": "O(log n)",
            "Search (existing)": "O(log n)",
            "Search (missing)": "O(log n)",
            "Range Query": "O(log n + k)",
            "Delete": "O(log n)",
        }

        # Create a summary table
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))

        # Plot 1: All operations on same graph
        colors = ["blue", "green", "red", "orange", "purple"]

        for i, (op_name, data) in enumerate(self.results.items()):
            ax1.plot(
                data["sizes"],
                data["times"],
                "o-",
                color=colors[i],
                label=f"{op_name} ({theoretical_complexities[op_name]})",
                linewidth=2,
                markersize=6,
            )

        ax1.set_xlabel("Data Size (n)")
        ax1.set_ylabel("Time (seconds)")
        ax1.set_title("B+ Tree Operations - Time Complexity Comparison")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale("log")
        ax1.set_yscale("log")

        # Plot 2: Complexity summary table
        ax2.axis("off")

        # Create table data
        table_data = []
        for op_name in self.results.keys():
            table_data.append(
                [
                    op_name,
                    theoretical_complexities[op_name],
                    "O(1)" if op_name == "Search (existing)" else "O(log n)",
                    "O(n)" if op_name == "Range Query" else "O(log n)",
                    "O(log n)" if op_name != "Range Query" else "O(n)",
                ]
            )

        # Create table
        table = ax2.table(
            cellText=table_data,
            colLabels=["Operation", "Average Case", "Best Case", "Worst Case", "Space"],
            cellLoc="center",
            loc="center",
        )

        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 2)

        # Style the table
        for i in range(len(table_data) + 1):
            for j in range(5):
                if i == 0:  # Header row
                    table[(i, j)].set_facecolor("#4CAF50")
                    table[(i, j)].set_text_props(weight="bold", color="white")
                else:
                    table[(i, j)].set_facecolor("#f0f0f0" if i % 2 == 0 else "white")

        ax2.set_title(
            "B+ Tree Complexity Summary", fontsize=16, fontweight="bold", pad=20
        )

        plt.tight_layout()
        plt.savefig(
            "analysis/bplus_tree_complexity_summary.png", dpi=300, bbox_inches="tight"
        )
        plt.show()

    def print_complexity_summary(self):
        """
        Print a detailed complexity summary.
        """
        print("\n" + "=" * 80)
        print("B+ TREE COMPLEXITY ANALYSIS SUMMARY")
        print("=" * 80)

        print("\nOPERATION COMPLEXITIES:")
        print("-" * 50)

        complexities = {
            "Insert": {
                "average": "O(log n)",
                "best": "O(1)",
                "worst": "O(log n)",
                "space": "O(log n)",
                "description": "Insertion requires finding the correct leaf and potentially splitting nodes",
            },
            "Search": {
                "average": "O(log n)",
                "best": "O(1)",
                "worst": "O(log n)",
                "space": "O(1)",
                "description": "Search navigates from root to leaf using internal node keys",
            },
            "Delete": {
                "average": "O(log n)",
                "best": "O(1)",
                "worst": "O(log n)",
                "space": "O(log n)",
                "description": "Deletion may require borrowing from siblings or merging nodes",
            },
            "Range Query": {
                "average": "O(log n + k)",
                "best": "O(log n)",
                "worst": "O(n)",
                "space": "O(k)",
                "description": "Uses doubly-linked leaf structure for efficient range traversal",
            },
        }

        for op, details in complexities.items():
            print(f"\n{op.upper()}:")
            print(f"  Average Case: {details['average']}")
            print(f"  Best Case:    {details['best']}")
            print(f"  Worst Case:   {details['worst']}")
            print(f"  Space:        {details['space']}")
            print(f"  Description:  {details['description']}")

        print("\n" + "=" * 80)
        print("KEY CHARACTERISTICS:")
        print("-" * 30)
        print("• All leaf nodes are at the same level (balanced tree)")
        print("• Internal nodes only store keys for navigation")
        print("• Leaf nodes store actual data and are linked together")
        print("• Tree order 'm' determines maximum children per node")
        print("• Height is always O(log n) due to balanced structure")
        print("• Range queries are efficient due to leaf node linking")
        print("=" * 80)


def run_complexity_analysis():
    """
    Main function to run the complexity analysis.
    """
    print("Starting B+ Tree Complexity Analysis...")

    analyzer = BPlusTreeComplexityAnalysis()
    analyzer.analyze_complexities()
    analyzer.print_complexity_summary()

    print("\nAnalysis complete! Check the generated PNG files for visualizations.")


if __name__ == "__main__":
    run_complexity_analysis()
