#!/usr/bin/env python3
"""Example: Analyze impact of different trump suits on game outcomes."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from butifarra import Simulator, Suit


def main():
    """Analyze trump suit impact on game statistics."""
    print("Analyzing Trump Suit Impact on Butifarra Games")
    print("=" * 60)
    print()
    
    simulator = Simulator()
    num_games = 10000
    
    results = {}
    
    # Run simulations for each trump suit
    for suit in Suit:
        print(f"Running {num_games} games with {suit.value} as trump...")
        stats = simulator.run_simulations(num_games, trump=suit)
        
        results[suit] = {
            'win_rate_a': stats.team_a_win_rate,
            'win_rate_b': stats.team_b_win_rate,
            'avg_score_a': stats.avg_team_a_score,
            'avg_score_b': stats.avg_team_b_score,
        }
        
        simulator.reset_stats()
    
    # Display comparative results
    print("\n" + "=" * 60)
    print("COMPARATIVE RESULTS")
    print("=" * 60)
    print()
    print(f"{'Trump Suit':<15} {'Team A Win%':<15} {'Team B Win%':<15} {'Avg A Score':<15} {'Avg B Score':<15}")
    print("-" * 75)
    
    for suit in Suit:
        r = results[suit]
        print(f"{suit.value:<15} {r['win_rate_a']:>13.1%} {r['win_rate_b']:>13.1%} {r['avg_score_a']:>13.1f} {r['avg_score_b']:>13.1f}")
    
    print()
    print("Note: In random card dealing with equal play strategies,")
    print("both teams should have approximately 50% win rate.")


if __name__ == "__main__":
    main()
