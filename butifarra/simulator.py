"""Simulation engine for butifarra statistics."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import Counter
import random

from .game import Game, Team
from .card import Suit


@dataclass
class SimulationStats:
    """Statistics from running simulations."""
    total_games: int = 0
    team_a_wins: int = 0
    team_b_wins: int = 0
    team_a_total_points: int = 0
    team_b_total_points: int = 0
    score_distribution: Counter = field(default_factory=Counter)
    trump_suit_stats: Dict[Suit, Dict[str, int]] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize trump suit stats."""
        if not self.trump_suit_stats:
            for suit in Suit:
                self.trump_suit_stats[suit] = {
                    'games': 0,
                    'team_a_wins': 0,
                    'team_b_wins': 0,
                    'total_points_team_a': 0,
                    'total_points_team_b': 0,
                }

    def add_game_result(
        self, 
        winning_team: Team, 
        team_a_score: int, 
        team_b_score: int, 
        trump: Suit
    ) -> None:
        """Add a game result to statistics."""
        self.total_games += 1
        
        if winning_team == Team.TEAM_A:
            self.team_a_wins += 1
        else:
            self.team_b_wins += 1
        
        self.team_a_total_points += team_a_score
        self.team_b_total_points += team_b_score
        
        # Track score distribution
        self.score_distribution[(team_a_score, team_b_score)] += 1
        
        # Track trump-specific stats
        self.trump_suit_stats[trump]['games'] += 1
        if winning_team == Team.TEAM_A:
            self.trump_suit_stats[trump]['team_a_wins'] += 1
        else:
            self.trump_suit_stats[trump]['team_b_wins'] += 1
        self.trump_suit_stats[trump]['total_points_team_a'] += team_a_score
        self.trump_suit_stats[trump]['total_points_team_b'] += team_b_score

    @property
    def team_a_win_rate(self) -> float:
        """Calculate Team A win rate."""
        if self.total_games == 0:
            return 0.0
        return self.team_a_wins / self.total_games

    @property
    def team_b_win_rate(self) -> float:
        """Calculate Team B win rate."""
        if self.total_games == 0:
            return 0.0
        return self.team_b_wins / self.total_games

    @property
    def avg_team_a_score(self) -> float:
        """Calculate average Team A score."""
        if self.total_games == 0:
            return 0.0
        return self.team_a_total_points / self.total_games

    @property
    def avg_team_b_score(self) -> float:
        """Calculate average Team B score."""
        if self.total_games == 0:
            return 0.0
        return self.team_b_total_points / self.total_games

    def get_summary(self) -> str:
        """Get a formatted summary of statistics."""
        lines = [
            "=== Butifarra Simulation Statistics ===",
            f"Total games: {self.total_games}",
            "",
            "Overall Results:",
            f"  Team A wins: {self.team_a_wins} ({self.team_a_win_rate:.1%})",
            f"  Team B wins: {self.team_b_wins} ({self.team_b_win_rate:.1%})",
            f"  Average Team A score: {self.avg_team_a_score:.1f}",
            f"  Average Team B score: {self.avg_team_b_score:.1f}",
            "",
            "Trump Suit Statistics:",
        ]
        
        for suit in Suit:
            stats = self.trump_suit_stats[suit]
            if stats['games'] > 0:
                a_win_rate = stats['team_a_wins'] / stats['games']
                avg_a = stats['total_points_team_a'] / stats['games']
                avg_b = stats['total_points_team_b'] / stats['games']
                lines.append(f"  {suit.value.capitalize()}:")
                lines.append(f"    Games: {stats['games']}")
                lines.append(f"    Team A win rate: {a_win_rate:.1%}")
                lines.append(f"    Avg scores: Team A={avg_a:.1f}, Team B={avg_b:.1f}")
        
        if self.score_distribution:
            lines.append("")
            lines.append("Most Common Score Lines (top 5):")
            for (a_score, b_score), count in self.score_distribution.most_common(5):
                pct = count / self.total_games
                lines.append(f"  {a_score}-{b_score}: {count} times ({pct:.1%})")
        
        return "\n".join(lines)


class Simulator:
    """Runs butifarra game simulations."""

    def __init__(self, player_names: Optional[List[str]] = None):
        """
        Initialize simulator.
        
        Args:
            player_names: Optional list of 4 player names
        """
        self.game = Game(player_names)
        self.stats = SimulationStats()

    def run_simulations(
        self, 
        num_games: int, 
        trump: Optional[Suit] = None,
        random_trump: bool = False
    ) -> SimulationStats:
        """
        Run multiple game simulations.
        
        Args:
            num_games: Number of games to simulate
            trump: Trump suit to use (if None and random_trump=False, cycles through suits)
            random_trump: If True, randomly select trump each game
            
        Returns:
            SimulationStats object with results
        """
        self.stats = SimulationStats()
        
        for i in range(num_games):
            # Determine trump for this game
            if trump is not None:
                game_trump = trump
            elif random_trump:
                game_trump = random.choice(list(Suit))
            else:
                # Cycle through suits
                game_trump = list(Suit)[i % len(Suit)]
            
            # Play the game
            winning_team, team_a_score, team_b_score = self.game.play_full_game(game_trump)
            
            # Record statistics
            self.stats.add_game_result(winning_team, team_a_score, team_b_score, game_trump)
        
        return self.stats

    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = SimulationStats()


def run_quick_simulation(num_games: int = 1000) -> SimulationStats:
    """
    Run a quick simulation with default settings.
    
    Args:
        num_games: Number of games to simulate
        
    Returns:
        SimulationStats object with results
    """
    simulator = Simulator()
    return simulator.run_simulations(num_games, random_trump=True)
