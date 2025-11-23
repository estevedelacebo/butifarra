#!/usr/bin/env python3
"""Example: Basic simulation running multiple games."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from butifarra import Simulator, Suit


def main():
    """Run basic simulations and print statistics."""
    print("Running butifarra simulations...\n")
    
    # Create simulator
    simulator = Simulator()
    
    # Run 10,000 games with random trump
    print("Simulation 1: 10,000 games with random trump")
    print("-" * 50)
    stats = simulator.run_simulations(10000, random_trump=True)
    print(stats.get_summary())
    print("\n\n")
    
    # Run 5,000 games with each specific trump
    for suit in Suit:
        simulator.reset_stats()
        print(f"Simulation 2: 5,000 games with {suit.value} as trump")
        print("-" * 50)
        stats = simulator.run_simulations(5000, trump=suit)
        print(stats.get_summary())
        print("\n\n")


if __name__ == "__main__":
    main()
