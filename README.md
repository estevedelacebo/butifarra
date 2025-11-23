# Butifarra

Statistics and simulations about the butifarra card game.

## Overview

Butifarra is a popular Catalan trick-taking card game played with 4 players in 2 teams using a Spanish deck (48 cards). This package provides a simulation framework to compute various statistics about the game, including win rates, score distributions, and the impact of different trump suits.

## Features

- **Complete game implementation**: Full butifarra game rules and logic
- **Simulation engine**: Run thousands of games to gather statistics
- **Statistical analysis**: Track win rates, scores, and trump suit impact
- **Flexible configuration**: Customize players, trump selection, and simulation parameters
- **Example scripts**: Ready-to-use examples for common analysis tasks

## Installation

```bash
# Clone the repository
git clone https://github.com/estevedelacebo/butifarra.git
cd butifarra

# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
from butifarra import run_quick_simulation

# Run 1000 games and get statistics
stats = run_quick_simulation(1000)
print(stats.get_summary())
```

## Usage Examples

### Basic Simulation

```python
from butifarra import Simulator, Suit

# Create simulator
simulator = Simulator()

# Run 10,000 games with random trump
stats = simulator.run_simulations(10000, random_trump=True)
print(stats.get_summary())

# Run games with specific trump
stats = simulator.run_simulations(5000, trump=Suit.OROS)
print(f"Team A win rate: {stats.team_a_win_rate:.1%}")
print(f"Average Team A score: {stats.avg_team_a_score:.1f}")
```

### Analyzing Trump Impact

```python
from butifarra import Simulator, Suit

simulator = Simulator()

for suit in Suit:
    stats = simulator.run_simulations(1000, trump=suit)
    print(f"{suit.value}: Team A wins {stats.team_a_win_rate:.1%}")
    simulator.reset_stats()
```

### Running Example Scripts

The `examples/` directory contains ready-to-use scripts:

```bash
# Basic simulation with statistics
python examples/quick_stats.py

# Comprehensive simulation report
python examples/basic_simulation.py

# Trump suit impact analysis
python examples/analyze_trump_impact.py
```

## Game Rules

Butifarra is played with:
- **Players**: 4 players in 2 teams (players 0,2 vs 1,3)
- **Deck**: Spanish deck of 48 cards (12 cards per suit: As, 2-9, Sota, Caballo, Rey)
- **Suits**: Oros (golds), Copas (cups), Espadas (swords), Bastos (clubs)
- **Objective**: Win tricks and score points

### Scoring

Points are awarded based on the cards won in tricks:

**Trump cards:**
- As (Ace): 11 points
- Tres (3): 10 points
- Rey (King): 4 points
- Caballo (Knight): 3 points
- Sota (Jack): 2 points

**Non-trump cards:**
- Rey (King): 4 points
- Caballo (Knight): 3 points

### Card Strength

**In trump suit:**
As > 3 > Rey > Caballo > Sota > 9 > 8 > 7 > 6 > 5 > 4 > 2

**In non-trump suits:**
As > Rey > Caballo > Sota > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=butifarra --cov-report=html
```

### Project Structure

```
butifarra/
├── butifarra/          # Main package
│   ├── card.py         # Card, Suit, and Rank definitions
│   ├── deck.py         # Deck management
│   ├── player.py       # Player logic
│   ├── game.py         # Game rules and mechanics
│   └── simulator.py    # Simulation engine and statistics
├── examples/           # Example scripts
├── tests/             # Test suite
└── README.md          # This file
```

## Statistics Collected

The simulation framework tracks:

- **Win rates**: Percentage of games won by each team
- **Average scores**: Mean points scored per game
- **Score distribution**: Most common final scores
- **Trump suit impact**: How different trump suits affect outcomes
- **Game outcomes**: Detailed results for each simulated game

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Butifarra is a traditional Catalan card game with rich history and cultural significance in Catalonia.
