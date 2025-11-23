"""Tests for card module."""

import pytest
from butifarra.card import Card, Suit, Rank


def test_card_creation():
    """Test creating a card."""
    card = Card(Suit.OROS, Rank.AS)
    assert card.suit == Suit.OROS
    assert card.rank == Rank.AS


def test_card_points_trump():
    """Test card points calculation with trump."""
    # As (Ace) in trump
    card = Card(Suit.OROS, Rank.AS)
    assert card.points(Suit.OROS) == 11
    assert card.points(Suit.COPAS) == 0
    
    # Tres (3) in trump
    card = Card(Suit.OROS, Rank.TRES)
    assert card.points(Suit.OROS) == 10
    assert card.points(Suit.COPAS) == 0
    
    # Rey (King) - always 4 points
    card = Card(Suit.OROS, Rank.REY)
    assert card.points(Suit.OROS) == 4
    assert card.points(Suit.COPAS) == 4
    
    # Caballo (Knight) - always 3 points
    card = Card(Suit.OROS, Rank.CABALLO)
    assert card.points(Suit.OROS) == 3
    assert card.points(Suit.COPAS) == 3
    
    # Sota (Jack) in trump
    card = Card(Suit.OROS, Rank.SOTA)
    assert card.points(Suit.OROS) == 2
    assert card.points(Suit.COPAS) == 0


def test_card_string_representation():
    """Test card string representation."""
    card = Card(Suit.OROS, Rank.AS)
    assert "As" in str(card)
    assert "oros" in str(card)
