from abc import ABC, abstractmethod
from app.game_models import GameState, Action, GameError
import random


class Bot(ABC):
    """Base class which all bot's inherit from."""

    BLURB: str
    NAME: str

    @classmethod
    @abstractmethod
    def get_action(cls, game_state: GameState) -> Action:
        """Takes a game state and returns the action a strategy would take."""
        pass


class TitForTat(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Tit for Tat' - a strategy which repeats whatever move the opponent made last round."""

    BLURB = "Tit for tat is a strategy which repeats whatever move the opponent made last round."
    NAME = "Tit for Tat"

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        # Cooperate in the first round.
        if game_state.round == 0:
            return Action.COOPERATE

        print(game_state, round)
        # Get the player's action from last round
        last_action: Action | None = game_state.history[game_state.round - 1][0]

        # If game state is invalid raise GameError
        if last_action == None:
            raise GameError

        return last_action


class AlwaysDefect(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Always Defect' - a strategy which defects regardless of the game state."""

    BLURB = "Always Defect is a straightforward strategy that will always defect."
    NAME = "Always Defect"

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        return Action.DEFECT


class AlwaysCooperate(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Always Cooperate' - a strategy which cooperates regardless of the game state."""

    BLURB = (
        "Always Co-operate is a straightforward strategy that will always co-operate."
    )
    NAME = "Always Co-operate"

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        return Action.COOPERATE


class Random(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Random' - a strategy which picks at random regardless of the game state."""

    BLURB = "The random strategy has no pattern, or strategy, and is just completely random."
    NAME = "Random"

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        return random.choice([Action.COOPERATE, Action.DEFECT])


class Pavlov(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Pavlov' - a strategy which repeats its previous action if it received a high pay off, if it received a low pay off it switches."""

    BLURB = (
        "Pavlov is a strategy which bases its decisions based off last rounds results."
    )
    NAME = "Pavlov"

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        if game_state.round == 0:
            return Action.COOPERATE

        last_player_action, last_bot_action = game_state.history[game_state.round - 1]

        if last_bot_action == Action.COOPERATE:
            # Return Co-operate if last round was high rewarding (both co-operated) else (player defected) defect to fight back.
            return (
                Action.COOPERATE
                if last_player_action == Action.COOPERATE
                else Action.DEFECT
            )
        else:
            # Return Defect if last round was high rewarding (bot defected while player co-operated) else (player defected) co-operate to make ammends.
            return (
                Action.DEFECT
                if last_player_action == Action.COOPERATE
                else Action.COOPERATE
            )


class TitForTwoTats(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Tit for 2 Tats' - a strategy which cooperates until the opponent defects twice in a row then only defects."""

    BLURB = "Tit for two tats is a strategy which is more forgiving than tit for tat, until you break its trust and betray it twice in a row."
    NAME = "Tit for Two Tats"

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        # Check if player has defected twice in a row.
        for r in range(game_state.round):
            if (
                game_state.history[r][0]
                == game_state.history[r + 1][0]
                == Action.DEFECT
            ):
                return Action.DEFECT

        # If player has not defected twice in a row co-operate.
        return Action.COOPERATE


class GrimTrigger(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Grim Trigger' - cooperates until the opponent first defects, from then on only defects."""

    BLURB = "Grim trigger is a strategy that does not forgive, ever."
    NAME = "Grim Trigger"

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        # Check if player defected in any round so far.
        for round in game_state.history[: game_state.round]:
            if round[0] is None:
                raise GameError

            if round[0] == Action.DEFECT:
                return Action.DEFECT

        return Action.COOPERATE


class Prober(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Prober' - starts with a fixed sequence, if the opponent fights back it plays Tit for Tat otherwise only defects."""

    BLURB = "Prober is a strategy which starts with a fixed sequence. The opponents response to the fixed sequence dictate its future actions. It can become either tit for tat or always defect."
    NAME = "Prober"
    SEQUENCE: list[Action] = [Action.DEFECT, Action.COOPERATE, Action.COOPERATE]

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        # Initial
        if game_state.round < 3:
            return cls.SEQUENCE[game_state.round]

        # Check results of probing.
        for round in game_state.history[:3]:
            if round[0] is None:
                raise GameError

            # Play tit for tat if player defected in the first 3 rounds.
            elif round[0] is Action.DEFECT:
                return TitForTat.get_action(game_state)

        else:
            return Action.DEFECT
