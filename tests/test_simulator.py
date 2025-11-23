"""Tests for simulator module."""

import pytest
from butifarra.simulator import Simulator, SimulationStats, run_quick_simulation
from butifarra.game import Team
from butifarra.card import Suit


def test_simulation_stats_creation():
    """Test creating simulation statistics."""
    stats = SimulationStats()
    assert stats.total_games == 0
    assert stats.team_a_wins == 0
    assert stats.team_b_wins == 0


def test_simulation_stats_add_result():
    """Test adding game results to statistics."""
    stats = SimulationStats()
    stats.add_game_result(Team.TEAM_A, 80, 40, Suit.OROS)
    
    assert stats.total_games == 1
    assert stats.team_a_wins == 1
    assert stats.team_b_wins == 0
    assert stats.team_a_total_points == 80
    assert stats.team_b_total_points == 40


def test_simulation_stats_win_rates():
    """Test win rate calculations."""
    stats = SimulationStats()
    stats.add_game_result(Team.TEAM_A, 80, 40, Suit.OROS)
    stats.add_game_result(Team.TEAM_B, 40, 80, Suit.COPAS)
    
    assert stats.team_a_win_rate == 0.5
    assert stats.team_b_win_rate == 0.5


def test_simulation_stats_averages():
    """Test average score calculations."""
    stats = SimulationStats()
    stats.add_game_result(Team.TEAM_A, 80, 40, Suit.OROS)
    stats.add_game_result(Team.TEAM_A, 60, 60, Suit.COPAS)
    
    assert stats.avg_team_a_score == 70.0
    assert stats.avg_team_b_score == 50.0


def test_simulator_creation():
    """Test creating a simulator."""
    simulator = Simulator()
    assert simulator.game is not None
    assert simulator.stats is not None


def test_simulator_run_simulations():
    """Test running simulations."""
    simulator = Simulator()
    stats = simulator.run_simulations(10, trump=Suit.OROS)
    
    assert stats.total_games == 10
    assert stats.team_a_wins + stats.team_b_wins == 10


def test_simulator_random_trump():
    """Test simulations with random trump."""
    simulator = Simulator()
    stats = simulator.run_simulations(20, random_trump=True)
    
    assert stats.total_games == 20
    
    # Should have used multiple trump suits
    suits_used = sum(1 for suit in Suit if stats.trump_suit_stats[suit]['games'] > 0)
    assert suits_used > 0


def test_simulator_reset():
    """Test resetting simulator statistics."""
    simulator = Simulator()
    simulator.run_simulations(5, trump=Suit.BASTOS)
    
    simulator.reset_stats()
    assert simulator.stats.total_games == 0


def test_quick_simulation():
    """Test quick simulation function."""
    stats = run_quick_simulation(10)
    assert stats.total_games == 10


def test_simulation_stats_summary():
    """Test statistics summary generation."""
    stats = SimulationStats()
    stats.add_game_result(Team.TEAM_A, 80, 40, Suit.OROS)
    
    summary = stats.get_summary()
    assert "Total games: 1" in summary
    assert "Team A wins" in summary
