"""Butifarra card game simulations and statistics."""

__version__ = "0.1.0"

from .card import Card, Suit, Rank
from .deck import Deck
from .player import Player
from .game import Game, Team
from .simulator import Simulator, SimulationStats, run_quick_simulation

__all__ = [
    "Card",
    "Suit",
    "Rank",
    "Deck",
    "Player",
    "Game",
    "Team",
    "Simulator",
    "SimulationStats",
    "run_quick_simulation",
]
