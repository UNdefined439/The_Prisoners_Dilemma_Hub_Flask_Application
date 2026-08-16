from dataclasses import dataclass
from enum import Enum


class Action(Enum):
    """An action a player could take in the Prisoner's Dilemma."""

    COOPERATE = "cooperate"
    DEFECT = "defect"


@dataclass
class GameState:
    """Stores the history of actions in a game of the Prisoner's Dilemma (Player, Bot) and the current round number (0-indexed)."""

    history: list[tuple[Action | None, Action | None]]
    round: int


class GameError(Exception):
    """An error that will be raised when a bot fails to find a action."""
