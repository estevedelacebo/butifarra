"""Game logic for butifarra."""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum
from .card import Card, Suit, Rank
from .deck import Deck
from .player import Player


class Team(Enum):
    """Teams in butifarra (players 0,2 vs 1,3)."""
    TEAM_A = 0  # Players 0 and 2
    TEAM_B = 1  # Players 1 and 3


@dataclass
class Trick:
    """Represents a trick (4 cards played)."""
    cards: List[Tuple[Player, Card]]
    winner: Player
    points: int


class Game:
    """Manages a game of butifarra."""

    def __init__(self, player_names: Optional[List[str]] = None):
        """
        Initialize a game.
        
        Args:
            player_names: Optional list of 4 player names
        """
        if player_names is None:
            player_names = [f"Player {i}" for i in range(4)]
        
        if len(player_names) != 4:
            raise ValueError("Butifarra requires exactly 4 players")
        
        self.players = [Player(name, i) for i, name in enumerate(player_names)]
        self.deck = Deck()
        self.tricks: List[Trick] = []
        self.trump: Optional[Suit] = None
        self.scores = {Team.TEAM_A: 0, Team.TEAM_B: 0}

    def deal_cards(self) -> None:
        """Deal 12 cards to each player."""
        self.deck.reset()
        self.deck.shuffle()
        
        for player in self.players:
            player.clear_hand()
            cards = self.deck.deal(12)
            player.receive_cards(cards)

    def set_trump(self, trump: Suit) -> None:
        """Set the trump suit for this game."""
        self.trump = trump

    def play_trick(self, starting_player: int = 0) -> Trick:
        """
        Play one trick starting with specified player.
        
        Args:
            starting_player: Position of player who leads
            
        Returns:
            Trick object with results
        """
        played_cards: List[Tuple[Player, Card]] = []
        lead_suit: Optional[Suit] = None
        
        # Each player plays a card
        for i in range(4):
            player_pos = (starting_player + i) % 4
            player = self.players[player_pos]
            
            # Get valid plays
            valid_cards = player.get_valid_plays(lead_suit)
            
            # Simple strategy: play first valid card
            # (In simulations, this can be replaced with different strategies)
            card = valid_cards[0]
            player.play_card(card)
            
            if i == 0:
                lead_suit = card.suit
            
            played_cards.append((player, card))
        
        # Determine winner
        winner, points = self._determine_trick_winner(played_cards, lead_suit)
        
        trick = Trick(cards=played_cards, winner=winner, points=points)
        self.tricks.append(trick)
        
        # Add points to winning team
        team = self._get_player_team(winner)
        self.scores[team] += points
        
        return trick

    def _determine_trick_winner(
        self, 
        played_cards: List[Tuple[Player, Card]], 
        lead_suit: Suit
    ) -> Tuple[Player, int]:
        """
        Determine who wins the trick and calculate points.
        
        Rules:
        1. Trump cards beat non-trump cards
        2. Among trump cards, highest rank wins
        3. Among non-trump cards of lead suit, highest rank wins
        4. Cards not following suit cannot win (unless trump)
        
        Args:
            played_cards: List of (player, card) tuples
            lead_suit: The suit that was led
            
        Returns:
            Tuple of (winning player, points)
        """
        total_points = sum(card.points(self.trump) for _, card in played_cards)
        
        # Separate trump and non-trump cards
        trump_cards = [(p, c) for p, c in played_cards if c.suit == self.trump]
        
        if trump_cards:
            # Trump was played, highest trump wins
            winner, winning_card = max(
                trump_cards, 
                key=lambda x: self._card_strength(x[1], self.trump, is_trump=True)
            )
        else:
            # No trump, highest card of lead suit wins
            lead_suit_cards = [(p, c) for p, c in played_cards if c.suit == lead_suit]
            winner, winning_card = max(
                lead_suit_cards,
                key=lambda x: self._card_strength(x[1], self.trump, is_trump=False)
            )
        
        return winner, total_points

    def _card_strength(self, card: Card, trump: Optional[Suit], is_trump: bool) -> int:
        """
        Calculate card strength for comparison.
        
        In butifarra, trump card order: As, 3, Rey, Caballo, Sota, 9, 8, 7, 6, 5, 4, 2
        Non-trump order: As, Rey, Caballo, Sota, 9, 8, 7, 6, 5, 4, 3, 2
        """
        if is_trump:
            trump_order = {
                Rank.AS: 12,
                Rank.TRES: 11,
                Rank.REY: 10,
                Rank.CABALLO: 9,
                Rank.SOTA: 8,
                Rank.NUEVE: 7,
                Rank.OCHO: 6,
                Rank.SIETE: 5,
                Rank.SEIS: 4,
                Rank.CINCO: 3,
                Rank.CUATRO: 2,
                Rank.DOS: 1,
            }
            return trump_order.get(card.rank, 0)
        else:
            non_trump_order = {
                Rank.AS: 12,
                Rank.REY: 11,
                Rank.CABALLO: 10,
                Rank.SOTA: 9,
                Rank.NUEVE: 8,
                Rank.OCHO: 7,
                Rank.SIETE: 6,
                Rank.SEIS: 5,
                Rank.CINCO: 4,
                Rank.CUATRO: 3,
                Rank.TRES: 2,
                Rank.DOS: 1,
            }
            return non_trump_order.get(card.rank, 0)

    def _get_player_team(self, player: Player) -> Team:
        """Get the team of a player."""
        return Team.TEAM_A if player.position % 2 == 0 else Team.TEAM_B

    def play_full_game(self, trump: Suit) -> Tuple[Team, int, int]:
        """
        Play a complete game of butifarra.
        
        Args:
            trump: Trump suit for this game
            
        Returns:
            Tuple of (winning_team, team_a_score, team_b_score)
        """
        self.deal_cards()
        self.set_trump(trump)
        self.tricks = []
        self.scores = {Team.TEAM_A: 0, Team.TEAM_B: 0}
        
        starting_player = 0
        
        # Play 12 tricks
        for _ in range(12):
            trick = self.play_trick(starting_player)
            starting_player = trick.winner.position
        
        # Determine winner
        team_a_score = self.scores[Team.TEAM_A]
        team_b_score = self.scores[Team.TEAM_B]
        winning_team = Team.TEAM_A if team_a_score > team_b_score else Team.TEAM_B
        
        return winning_team, team_a_score, team_b_score

    def reset(self) -> None:
        """Reset game state."""
        self.tricks = []
        self.trump = None
        self.scores = {Team.TEAM_A: 0, Team.TEAM_B: 0}
        for player in self.players:
            player.clear_hand()
