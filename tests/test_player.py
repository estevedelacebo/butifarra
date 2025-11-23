"""Tests for player module."""

import pytest
from butifarra.player import Player
from butifarra.card import Card, Suit, Rank


def test_player_creation():
    """Test creating a player."""
    player = Player("Alice", 0)
    assert player.name == "Alice"
    assert player.position == 0
    assert len(player.hand) == 0


def test_player_receive_cards():
    """Test player receiving cards."""
    player = Player("Bob", 1)
    cards = [
        Card(Suit.OROS, Rank.AS),
        Card(Suit.COPAS, Rank.REY),
    ]
    player.receive_cards(cards)
    assert len(player.hand) == 2


def test_player_can_follow_suit():
    """Test checking if player can follow suit."""
    player = Player("Charlie", 2)
    player.receive_cards([
        Card(Suit.OROS, Rank.AS),
        Card(Suit.COPAS, Rank.REY),
        Card(Suit.BASTOS, Rank.TRES),
    ])
    
    assert player.can_follow_suit(Suit.OROS)
    assert player.can_follow_suit(Suit.COPAS)
    assert not player.can_follow_suit(Suit.ESPADAS)


def test_player_get_valid_plays():
    """Test getting valid plays."""
    player = Player("Diana", 3)
    player.receive_cards([
        Card(Suit.OROS, Rank.AS),
        Card(Suit.OROS, Rank.REY),
        Card(Suit.COPAS, Rank.TRES),
    ])
    
    # Can play any card when leading
    valid = player.get_valid_plays()
    assert len(valid) == 3
    
    # Must follow suit if possible
    valid = player.get_valid_plays(Suit.OROS)
    assert len(valid) == 2
    assert all(c.suit == Suit.OROS for c in valid)
    
    # Can play any card if can't follow suit
    valid = player.get_valid_plays(Suit.BASTOS)
    assert len(valid) == 3


def test_player_play_card():
    """Test playing a card."""
    player = Player("Eve", 0)
    card = Card(Suit.OROS, Rank.AS)
    player.receive_cards([card])
    
    played = player.play_card(card)
    assert played == card
    assert len(player.hand) == 0


def test_player_play_invalid_card():
    """Test playing card not in hand."""
    player = Player("Frank", 1)
    player.receive_cards([Card(Suit.OROS, Rank.AS)])
    
    invalid_card = Card(Suit.COPAS, Rank.REY)
    with pytest.raises(ValueError):
        player.play_card(invalid_card)
