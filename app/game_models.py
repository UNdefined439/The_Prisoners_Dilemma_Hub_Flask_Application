from dataclasses import dataclass
from enum import Enum


class Action(Enum):
    """An action a player could take in the Prisoner's Dilemma."""

    COOPERATE = "cooperate"
    DEFECT = "defect"


@dataclass
class GameState:
    """History of actions in a game of the Prisoner's Dilemma."""

    history: list[tuple[Action | None, Action | None]]
    round_number: int
