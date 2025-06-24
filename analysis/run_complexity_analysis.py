#!/usr/bin/env python3
"""
B+ Tree Complexity Analysis Runner

This script runs the complexity analysis for B+ tree operations
and generates visualizations of the time complexity.
"""

import sys
import os

# Add the current directory to the path so we can import bplus_tree
sys.path.append(".")

try:
    from .complexity_analysis import run_complexity_analysis

    print("Starting B+ Tree Complexity Analysis...")
    run_complexity_analysis()
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please make sure you have installed the required dependencies:")
    print("pip install matplotlib numpy")
    sys.exit(1)
except Exception as e:
    print(f"Error running analysis: {e}")
    sys.exit(1)
