#!/usr/bin/env python3
"""Example: Analyze score distribution patterns in butifarra games."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from butifarra import Simulator


def main():
    """Analyze score distribution patterns."""
    print("Butifarra Score Distribution Analysis")
    print("=" * 60)
    print()
    
    simulator = Simulator()
    num_games = 10000
    
    print(f"Running {num_games} games to analyze score patterns...")
    print()
    
    stats = simulator.run_simulations(num_games, random_trump=True)
    
    print("RESULTS")
    print("-" * 60)
    print(f"Total games played: {stats.total_games}")
    print(f"Team A win rate: {stats.team_a_win_rate:.2%}")
    print(f"Team B win rate: {stats.team_b_win_rate:.2%}")
    print()
    print(f"Average scores:")
    print(f"  Team A: {stats.avg_team_a_score:.2f} points")
    print(f"  Team B: {stats.avg_team_b_score:.2f} points")
    print()
    
    # Analyze score distributions
    print("Most Common Final Scores (Top 10):")
    print(f"{'Rank':<6} {'Score (A-B)':<15} {'Frequency':<12} {'Percentage':<12}")
    print("-" * 60)
    
    for idx, ((a_score, b_score), count) in enumerate(stats.score_distribution.most_common(10), 1):
        percentage = (count / stats.total_games) * 100
        print(f"{idx:<6} {f'{a_score}-{b_score}':<15} {count:<12} {percentage:>10.2f}%")
    
    print()
    print("Note: With random dealing and simple play strategy, scores tend")
    print("to be relatively balanced around ~25 points per team (51 total).")


if __name__ == "__main__":
    main()
