# B+ Tree Complexity Analysis

This project includes comprehensive complexity analysis tools to visualize and understand the time complexity of B+ tree operations using Big O notation.

## Features

- **Time Complexity Measurement**: Measures actual execution time for different data sizes
- **Theoretical vs Actual Comparison**: Compares measured performance with theoretical Big O complexity
- **Visual Charts**: Generates detailed plots showing complexity relationships
- **Comprehensive Analysis**: Covers all major B+ tree operations (Insert, Search, Delete, Range Query)

## Operations Analyzed

| Operation   | Average Case | Best Case | Worst Case | Space Complexity |
| ----------- | ------------ | --------- | ---------- | ---------------- |
| Insert      | O(log n)     | O(1)      | O(log n)   | O(log n)         |
| Search      | O(log n)     | O(1)      | O(log n)   | O(1)             |
| Delete      | O(log n)     | O(1)      | O(log n)   | O(log n)         |
| Range Query | O(log n + k) | O(log n)  | O(n)       | O(k)             |

## Installation

1. Create and activate a virtual environment:

For MacOS/Linux:

```bash
python3 -m venv venv

source venv/bin/activate
```

For Windows:

```cmd
python -m venv venv

.\venv\Scripts\activate
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Run from Command Line

```bash
python3 -m analysis.run_complexity_analysis
```

### Option 2: Use Jupyter Notebook (Currently not working)

```bash
jupyter notebook complexity_analysis.ipynb
```

### Option 3: Import and Use in Your Code

```python
from analysis.complexity_analysis import BPlusTreeComplexityAnalysis

analyzer = BPlusTreeComplexityAnalysis()
analyzer.analyze_complexities()
analyzer.print_complexity_summary()
```

## Output

The analysis generates:

1. **Individual Operation Plots**: Separate charts for each operation showing actual vs theoretical complexity
2. **Comparison Chart**: All operations plotted together for easy comparison
3. **Complexity Summary Table**: Detailed breakdown of all complexity cases
4. **Console Output**: Detailed textual analysis and explanations

## Generated Files

- `analysis/bplus_tree_complexity_analysis.png`: Individual operation complexity plots
- `analysis/bplus_tree_complexity_summary.png`: Comprehensive comparison and summary table

## Understanding the Results

### Log-Log Plots

The charts use logarithmic scales for both axes to better visualize the relationships:

- **X-axis**: Data size (n) - logarithmic scale
- **Y-axis**: Execution time - logarithmic scale
- **Solid lines**: Actual measured performance
- **Dashed lines**: Theoretical Big O complexity

### Key Insights

1. **Balanced Structure**: B+ trees maintain O(log n) height due to their balanced nature
2. **Efficient Search**: All search operations follow the same logarithmic pattern
3. **Range Queries**: Benefit from doubly-linked leaf structure for efficient traversal
4. **Consistent Performance**: Operations show predictable logarithmic scaling

## Technical Details

### Test Parameters

- **Tree Order**: 4 (configurable)
- **Data Sizes**: [10, 50, 100, 500, 1000, 2000, 5000]
- **Measurements**: Multiple runs per size for accuracy

### Complexity Classes Explained

- **O(1)**: Constant time - operation time doesn't depend on data size
- **O(log n)**: Logarithmic time - typical for balanced tree operations
- **O(n)**: Linear time - time proportional to data size
- **O(log n + k)**: Logarithmic plus range size - for range queries

## Customization

You can modify the analysis by:

1. **Changing data sizes**: Modify the `data_sizes` list in `analyze_complexities()`
2. **Adjusting tree order**: Change the `tree_order` parameter
3. **Adding new operations**: Implement new test methods and add them to the operations dictionary
4. **Customizing plots**: Modify the plotting functions for different visualizations

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running from the correct directory
2. **Missing Dependencies**: Install matplotlib and numpy: `pip install matplotlib numpy`
3. **Memory Issues**: Reduce data sizes for large-scale testing
4. **Slow Execution**: The analysis can take several minutes for larger data sizes

### Performance Tips

- Use smaller data sizes for quick testing
- Run on a machine with sufficient memory
- Consider running overnight for comprehensive analysis
- Use the Jupyter notebook for interactive exploration

## Contributing

To add new complexity analysis features:

1. Add new test methods to the `BPlusTreeComplexityAnalysis` class
2. Update the operations dictionary in `analyze_complexities()`
3. Add appropriate theoretical complexity curves in plotting functions
4. Update documentation and complexity tables

## References

- [B+ Tree Wikipedia](https://en.wikipedia.org/wiki/B%2B_tree)
- [Big O Notation](https://en.wikipedia.org/wiki/Big_O_notation)
- [Time Complexity Analysis](https://en.wikipedia.org/wiki/Time_complexity)
