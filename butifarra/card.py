"""Card representation for butifarra."""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class Suit(Enum):
    """Card suits in Spanish deck."""
    OROS = "oros"  # Golds/Coins
    COPAS = "copas"  # Cups
    ESPADAS = "espadas"  # Swords
    BASTOS = "bastos"  # Clubs


class Rank(Enum):
    """Card ranks in Spanish deck."""
    AS = (1, "As")
    DOS = (2, "2")
    TRES = (3, "3")
    CUATRO = (4, "4")
    CINCO = (5, "5")
    SEIS = (6, "6")
    SIETE = (7, "7")
    OCHO = (8, "8")
    NUEVE = (9, "9")
    SOTA = (10, "Sota")
    CABALLO = (11, "Caballo")
    REY = (12, "Rey")

    def __init__(self, value: int, display: str):
        self._value_ = value
        self.display = display

    @property
    def numeric_value(self) -> int:
        """Get numeric value of rank."""
        return self._value_


@dataclass(frozen=True)
class Card:
    """Represents a playing card."""
    suit: Suit
    rank: Rank

    def points(self, trump: Optional[Suit] = None) -> int:
        """
        Calculate points for this card in butifarra.
        
        In butifarra:
        - As (Ace): 11 points in trump, 0 otherwise
        - Tres (3): 10 points in trump, 0 otherwise
        - Rey (King): 4 points
        - Caballo (Knight): 3 points
        - Sota (Jack): 2 points in trump, 0 otherwise
        """
        is_trump = trump and self.suit == trump
        
        if self.rank == Rank.AS:
            return 11 if is_trump else 0
        elif self.rank == Rank.TRES:
            return 10 if is_trump else 0
        elif self.rank == Rank.REY:
            return 4
        elif self.rank == Rank.CABALLO:
            return 3
        elif self.rank == Rank.SOTA:
            return 2 if is_trump else 0
        return 0

    def __str__(self) -> str:
        return f"{self.rank.display} de {self.suit.value}"

    def __repr__(self) -> str:
        return f"Card({self.suit.value}, {self.rank.display})"
