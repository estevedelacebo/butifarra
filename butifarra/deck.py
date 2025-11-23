"""Deck management for butifarra."""

import random
from typing import List
from .card import Card, Suit, Rank


class Deck:
    """Represents a Spanish deck of 48 cards (12 per suit)."""

    def __init__(self):
        """Initialize a full deck of 48 cards."""
        self.cards: List[Card] = []
        self._create_deck()

    def _create_deck(self) -> None:
        """Create all 48 cards in the Spanish deck."""
        self.cards = [
            Card(suit, rank)
            for suit in Suit
            for rank in Rank
        ]

    def shuffle(self) -> None:
        """Shuffle the deck randomly."""
        random.shuffle(self.cards)

    def deal(self, num_cards: int) -> List[Card]:
        """
        Deal a specified number of cards from the deck.
        
        Args:
            num_cards: Number of cards to deal
            
        Returns:
            List of dealt cards
            
        Raises:
            ValueError: If not enough cards remain in deck
        """
        if num_cards > len(self.cards):
            raise ValueError(f"Cannot deal {num_cards} cards, only {len(self.cards)} remaining")
        
        dealt = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt

    def reset(self) -> None:
        """Reset the deck to a full 48 cards."""
        self._create_deck()

    def __len__(self) -> int:
        """Return number of cards remaining in deck."""
        return len(self.cards)
