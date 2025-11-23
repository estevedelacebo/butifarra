#!/usr/bin/env python3
"""Example: Quick statistics from a small simulation."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from butifarra import run_quick_simulation


def main():
    """Run a quick simulation and display results."""
    print("Quick Butifarra Simulation")
    print("=" * 60)
    print()
    print("Running 1,000 games with random trump selection...")
    print()
    
    stats = run_quick_simulation(1000)
    print(stats.get_summary())


if __name__ == "__main__":
    main()
