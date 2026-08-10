from abc import ABC, abstractmethod
from game_models import GameState, Action


class Bot(ABC):
    """Base class which all bot's inherit from."""

    @abstractmethod
    def get_action(self, game_state: GameState) -> Action:
        """Takes a game state and returns the action a strategy would take."""
        pass


class TitForTat(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Tit for Tat' - a strategy which repeats whatever move the opponent made last round."""

    ...


class AlwaysDefect(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Always Defect' - a strategy which defects regardless of the game state."""

    ...


class AlwaysCooperate(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Always Cooperate' - a strategy which cooperates regardless of the game state."""

    ...


class Random(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Random' - a strategy which picks at random regardless of the game state."""

    ...


class Pavlov(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Pavlov' - a strategy which repeats its previous action if it received a high pay off, if it received a low pay off it switches."""

    ...


class TitForTwoTats(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Tit for 2 Tats' - a strategy which cooperates until the opponent defects twice in a row then only defects."""

    ...


class GrimTrigger(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Grim Trigger' - cooperates until the opponent first cooperates, from then on only defects."""

    ...


class Prober(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Prober' - starts with a fixed sequence, if the opponent fights back it plays Tit for Tat otherwise only defects."""

    ...
