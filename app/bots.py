from abc import ABC, abstractmethod
from game_models import GameState, Action, GameError
import random


class Bot(ABC):
    """Base class which all bot's inherit from."""

    @classmethod
    @abstractmethod
    def get_action(cls, game_state: GameState) -> Action:
        """Takes a game state and returns the action a strategy would take."""
        pass


class TitForTat(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Tit for Tat' - a strategy which repeats whatever move the opponent made last round."""

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        # Cooperate in the first round.
        if game_state.round == 0:
            return Action.COOPERATE

        # Get the player's action from last round
        last_action: Action | None = game_state.history[game_state.round - 1][0]

        # If game state is invalid raise GameError
        if last_action == None:
            raise GameError

        return last_action


class AlwaysDefect(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Always Defect' - a strategy which defects regardless of the game state."""

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        return Action.DEFECT


class AlwaysCooperate(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Always Cooperate' - a strategy which cooperates regardless of the game state."""

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        return Action.COOPERATE


class Random(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Random' - a strategy which picks at random regardless of the game state."""

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        return random.choice([Action.COOPERATE, Action.DEFECT])


class Pavlov(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Pavlov' - a strategy which repeats its previous action if it received a high pay off, if it received a low pay off it switches."""

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
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

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        defects: int = 0

        # Count the times Player has defected.
        for r in range(game_state.round):
            if game_state.history[r][0] == Action.DEFECT:
                defects += 1

                # If player defected at least twice defect.
                if defects == 2:
                    return Action.DEFECT

        # If player has not defected at least twice co-operate.
        return Action.COOPERATE


class GrimTrigger(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Grim Trigger' - cooperates until the opponent first defects, from then on only defects."""

    @classmethod
    def get_action(cls, game_state: GameState) -> Action:
        # Check if player defected in any round so far.
        for round in game_state.history[: game_state.round + 1]:
            if round[0] == None:
                raise GameError

            if round[0] == Action.DEFECT:
                return Action.DEFECT

        return Action.COOPERATE


class Prober(Bot):
    """A class containing the functionality of a bot that implements the Prisoner's Dilemma strategy 'Prober' - starts with a fixed sequence, if the opponent fights back it plays Tit for Tat otherwise only defects."""

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
