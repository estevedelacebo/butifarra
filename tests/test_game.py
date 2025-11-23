"""Tests for game module."""

import pytest
from butifarra.game import Game, Team
from butifarra.card import Suit


def test_game_creation():
    """Test creating a game."""
    game = Game()
    assert len(game.players) == 4
    assert game.trump is None


def test_game_with_custom_names():
    """Test creating game with custom player names."""
    names = ["Alice", "Bob", "Charlie", "Diana"]
    game = Game(names)
    assert [p.name for p in game.players] == names


def test_game_invalid_player_count():
    """Test game creation with wrong number of players."""
    with pytest.raises(ValueError):
        Game(["Alice", "Bob"])


def test_deal_cards():
    """Test dealing cards to players."""
    game = Game()
    game.deal_cards()
    
    # Each player should have 12 cards
    for player in game.players:
        assert len(player.hand) == 12
    
    # Deck should be empty
    assert len(game.deck) == 0


def test_set_trump():
    """Test setting trump suit."""
    game = Game()
    game.set_trump(Suit.OROS)
    assert game.trump == Suit.OROS


def test_play_full_game():
    """Test playing a complete game."""
    game = Game()
    winning_team, team_a_score, team_b_score = game.play_full_game(Suit.OROS)
    
    # Should have played 12 tricks
    assert len(game.tricks) == 12
    
    # Scores should be positive
    assert team_a_score >= 0
    assert team_b_score >= 0
    
    # One team should have won
    assert winning_team in [Team.TEAM_A, Team.TEAM_B]
    
    # All cards should have been played
    for player in game.players:
        assert len(player.hand) == 0


def test_team_assignment():
    """Test that teams are correctly assigned."""
    game = Game()
    
    # Players 0 and 2 are Team A
    assert game._get_player_team(game.players[0]) == Team.TEAM_A
    assert game._get_player_team(game.players[2]) == Team.TEAM_A
    
    # Players 1 and 3 are Team B
    assert game._get_player_team(game.players[1]) == Team.TEAM_B
    assert game._get_player_team(game.players[3]) == Team.TEAM_B


def test_game_reset():
    """Test resetting game state."""
    game = Game()
    game.play_full_game(Suit.COPAS)
    
    game.reset()
    assert len(game.tricks) == 0
    assert game.trump is None
    assert game.scores[Team.TEAM_A] == 0
    assert game.scores[Team.TEAM_B] == 0
