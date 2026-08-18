from app.bots import (
    TitForTat,
    AlwaysDefect,
    AlwaysCooperate,
    Pavlov,
    TitForTwoTats,
    GrimTrigger,
    Prober,
)
from app.game_models import GameState, Action

possible_rounds: dict[str, list[Action | None]] = {
    "None": [None, None],
    "coop": [Action.COOPERATE, Action.COOPERATE],
    "defect": [Action.DEFECT, Action.DEFECT],
    # Temptation to Defect - player defects, bot co-ops
    "temptation": [Action.DEFECT, Action.COOPERATE],
    # Sucker's Payoff - player co-ops, bot defects
    "sucker": [Action.COOPERATE, Action.DEFECT],
}

game_states: list[GameState] = [
    GameState(
        [
            possible_rounds["coop"],
            possible_rounds["temptation"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
        ],
        2,
    ),
    GameState(
        [
            possible_rounds["coop"],
            possible_rounds["temptation"],
            possible_rounds["sucker"],
            possible_rounds["coop"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
        ],
        4,
    ),
    GameState(
        [
            possible_rounds["coop"],
            possible_rounds["temptation"],
            possible_rounds["sucker"],
            possible_rounds["defect"],
            possible_rounds["sucker"],
            possible_rounds["coop"],
            possible_rounds["temptation"],
            possible_rounds["temptation"],
            possible_rounds["defect"],
            possible_rounds["None"],
        ],
        9,
    ),
    GameState(
        [
            possible_rounds["sucker"],
            possible_rounds["coop"],
            possible_rounds["coop"],
            possible_rounds["temptation"],
            possible_rounds["temptation"],
            possible_rounds["temptation"],
            possible_rounds["defect"],
            possible_rounds["coop"],
            possible_rounds["sucker"],
            possible_rounds["None"],
        ],
        9,
    ),
    GameState(
        [
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
            possible_rounds["None"],
        ],
        0,
    ),
]

# Note: Game states hold values that don't match every strategy's play. The test is just what a bot would do if put into the situation of the game state and was to now apply their logic.


def test_TitForTat():
    assert TitForTat.get_action(game_states[0]) == Action.DEFECT
    assert TitForTat.get_action(game_states[1]) == Action.COOPERATE
    assert TitForTat.get_action(game_states[2]) == Action.DEFECT
    assert TitForTat.get_action(game_states[3]) == Action.COOPERATE
    assert TitForTat.get_action(game_states[4]) == Action.COOPERATE


def test_AlwaysDefect():
    assert AlwaysDefect.get_action(game_states[0]) == Action.DEFECT
    assert AlwaysDefect.get_action(game_states[1]) == Action.DEFECT
    assert AlwaysDefect.get_action(game_states[2]) == Action.DEFECT
    assert AlwaysDefect.get_action(game_states[3]) == Action.DEFECT
    assert AlwaysDefect.get_action(game_states[4]) == Action.DEFECT


def test_AlwaysCooperate():
    assert AlwaysCooperate.get_action(game_states[0]) == Action.COOPERATE
    assert AlwaysCooperate.get_action(game_states[1]) == Action.COOPERATE
    assert AlwaysCooperate.get_action(game_states[2]) == Action.COOPERATE
    assert AlwaysCooperate.get_action(game_states[3]) == Action.COOPERATE
    assert AlwaysCooperate.get_action(game_states[4]) == Action.COOPERATE


def test_Random():
    # Its not viable to test this result.
    pass


def test_Pavlov():
    assert Pavlov.get_action(game_states[0]) == Action.DEFECT
    assert Pavlov.get_action(game_states[1]) == Action.COOPERATE
    assert Pavlov.get_action(game_states[2]) == Action.COOPERATE
    assert Pavlov.get_action(game_states[3]) == Action.DEFECT
    assert Pavlov.get_action(game_states[4]) == Action.COOPERATE


def test_TitForTwoTats():
    assert TitForTwoTats.get_action(game_states[0]) == Action.COOPERATE
    assert TitForTwoTats.get_action(game_states[1]) == Action.COOPERATE
    assert TitForTwoTats.get_action(game_states[2]) == Action.DEFECT
    assert TitForTwoTats.get_action(game_states[3]) == Action.DEFECT
    assert TitForTwoTats.get_action(game_states[4]) == Action.COOPERATE


def test_GrimTrigger():
    assert GrimTrigger.get_action(game_states[0]) == Action.DEFECT
    assert GrimTrigger.get_action(game_states[1]) == Action.DEFECT
    assert GrimTrigger.get_action(game_states[2]) == Action.DEFECT
    assert GrimTrigger.get_action(game_states[3]) == Action.DEFECT
    assert GrimTrigger.get_action(game_states[4]) == Action.COOPERATE


def test_Prober():
    assert Prober.get_action(game_states[0]) == Action.COOPERATE
    assert Prober.get_action(game_states[1]) == Action.COOPERATE
    assert Prober.get_action(game_states[2]) == Action.DEFECT
    assert Prober.get_action(game_states[3]) == Action.DEFECT
    assert Prober.get_action(game_states[4]) == Action.DEFECT
