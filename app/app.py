from flask import Flask, render_template, request, jsonify
from game_models import GameState, Action
from bots import (
    TitForTat,
    AlwaysDefect,
    AlwaysCooperate,
    Random,
    Pavlov,
    TitForTwoTats,
    GrimTrigger,
    Prober,
)

app: Flask = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/learn")
def learn():
    return render_template("learn.html")


@app.route("/play")
def play():
    return render_template("play.html")


@app.route("/api/game", methods=["POST"])
def game():
    data = request.get_json()

    if not data:
        return jsonify({"error": "missing JSON payload"}), 400

    id: int | None = data.get("strat_id")
    history: list[list[str | None]] | None = data.get("history")
    round: int | None = data.get("round")
    action: Action | str | None = data.get("action")

    if None in [id, history, round, action]:
        return jsonify({"error": "missing data"}), 400

    action = Action(action)
    converted_history: list[list[Action | None]] = []
    for r in history:
        curr_r: list[Action | None] = []

        for i in r:
            if i is not None:
                curr_r.append(Action(i))
            else:
                curr_r.append(None)

            converted_history.append(curr_r)

    game: GameState = GameState(history=[], round=round - 1)

    try:
        match id:
            case 1:
                response: Action = TitForTat.get_action(game)
            case 2:
                response: Action = Pavlov.get_action(game)
            case 3:
                response: Action = TitForTwoTats.get_action(game)
            case 4:
                response: Action = Random.get_action(game)
            case 5:
                response: Action = AlwaysCooperate.get_action(game)
            case 6:
                response: Action = AlwaysDefect.get_action(game)
            case 7:
                response: Action = GrimTrigger.get_action(game)
            case 8:
                response: Action = Prober.get_action(game)
            case _:
                return jsonify({"error": "invalid bot id"}), 400
    except:
        return jsonify({"error": "bot failed to return an action"}), 400

    if action == Action.COOPERATE and response == Action.COOPERATE:
        player_score, bot_score = 3, 3
    elif action == Action.COOPERATE and response == Action.DEFECT:
        player_score, bot_score = 0, 5
    elif action == Action.DEFECT and response == Action.COOPERATE:
        player_score, bot_score = 5, 0
    else:
        player_score, bot_score = 1, 1

    return (
        jsonify(
            {
                "player_score": player_score,
                "bot_score": bot_score,
                "round": round + 1,
                "explanation": f"Your opponent decided to {response.value}.",
                "response": response.value,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run()
