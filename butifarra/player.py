"""Player representation for butifarra."""

from typing import List, Optional
from .card import Card, Suit


class Player:
    """Represents a player in butifarra game."""

    def __init__(self, name: str, position: int):
        """
        Initialize a player.
        
        Args:
            name: Player's name
            position: Player's position at table (0-3)
        """
        self.name = name
        self.position = position
        self.hand: List[Card] = []

    def receive_cards(self, cards: List[Card]) -> None:
        """Add cards to player's hand."""
        self.hand.extend(cards)

    def clear_hand(self) -> None:
        """Clear all cards from hand."""
        self.hand = []

    def can_follow_suit(self, lead_suit: Suit) -> bool:
        """Check if player can follow the lead suit."""
        return any(card.suit == lead_suit for card in self.hand)

    def get_valid_plays(self, lead_suit: Optional[Suit] = None) -> List[Card]:
        """
        Get list of valid cards player can play.
        
        In butifarra, if a suit is led, players must follow suit if possible.
        
        Args:
            lead_suit: The suit that was led (None if player leads)
            
        Returns:
            List of valid cards to play
        """
        if lead_suit is None:
            # Player leads, can play any card
            return self.hand.copy()
        
        # Must follow suit if possible
        same_suit = [card for card in self.hand if card.suit == lead_suit]
        if same_suit:
            return same_suit
        
        # Can't follow suit, can play anything
        return self.hand.copy()

    def play_card(self, card: Card) -> Card:
        """
        Play a card from hand.
        
        Args:
            card: Card to play
            
        Returns:
            The played card
            
        Raises:
            ValueError: If card not in hand
        """
        if card not in self.hand:
            raise ValueError(f"Card {card} not in player's hand")
        self.hand.remove(card)
        return card

    def __str__(self) -> str:
        return f"Player({self.name}, position={self.position}, cards={len(self.hand)})"

    def __repr__(self) -> str:
        return self.__str__()
