"""Tests for deck module."""

import pytest
from butifarra.deck import Deck


def test_deck_creation():
    """Test creating a full deck."""
    deck = Deck()
    assert len(deck) == 48


def test_deck_dealing():
    """Test dealing cards from deck."""
    deck = Deck()
    cards = deck.deal(12)
    assert len(cards) == 12
    assert len(deck) == 36


def test_deck_deal_too_many():
    """Test dealing more cards than available."""
    deck = Deck()
    deck.deal(40)
    with pytest.raises(ValueError):
        deck.deal(10)


def test_deck_shuffle():
    """Test shuffling deck."""
    deck1 = Deck()
    deck2 = Deck()
    
    # Get initial order
    initial_cards1 = [str(c) for c in deck1.cards]
    initial_cards2 = [str(c) for c in deck2.cards]
    
    # Initial decks should be identical
    assert initial_cards1 == initial_cards2
    
    # After shuffle, order should likely be different
    deck1.shuffle()
    shuffled_cards = [str(c) for c in deck1.cards]
    
    # Unlikely to be same order after shuffle (probabilistically)
    # This test could theoretically fail, but extremely unlikely
    assert shuffled_cards != initial_cards1 or len(shuffled_cards) < 10


def test_deck_reset():
    """Test resetting deck."""
    deck = Deck()
    deck.deal(30)
    assert len(deck) == 18
    
    deck.reset()
    assert len(deck) == 48
