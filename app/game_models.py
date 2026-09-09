from dataclasses import dataclass
from typing import ClassVar
from enum import Enum


class Action(Enum):
    """An action a player could take in the Prisoner's Dilemma."""

    COOPERATE = "cooperate"
    DEFECT = "defect"


@dataclass
class GameState:
    """Stores the history of actions in a game of the Prisoner's Dilemma (Player, Bot) and the current round number (0-indexed)."""

    history: list[list[Action | None]]
    round: int
    MAXROUNDS: ClassVar[int] = 10


class GameError(Exception):
    """An error that will be raised when a bot fails to find a action."""
