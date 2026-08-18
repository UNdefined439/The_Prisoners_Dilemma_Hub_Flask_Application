from flask import Flask, render_template, request, jsonify
from app.game_models import GameState, Action
from app.bots import (
    TitForTat,
    AlwaysDefect,
    AlwaysCooperate,
    Random,
    Pavlov,
    TitForTwoTats,
    GrimTrigger,
    Prober,
    Bot,
)

app: Flask = Flask(__name__)

bot_ids: dict[int, type[Bot]] = {
    1: TitForTat,
    2: Pavlov,
    3: TitForTwoTats,
    4: Random,
    5: AlwaysCooperate,
    6: AlwaysDefect,
    7: GrimTrigger,
    8: Prober,
}


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
    player_total: int | None = data.get("player_total")
    bot_total: int | None = data.get("bot_total")

    if (
        id is None
        or history is None
        or round is None
        or action is None
        or player_total is None
        or bot_total is None
    ):
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

    game: GameState = GameState(history=converted_history, round=round - 1)

    try:
        if 0 < id < 9:
            response: Action = bot_ids[id].get_action(game)
        else:
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

    if round < 10:
        explanation: str = f"Your opponent decided to {response.value}."
    else:
        explanation: str = (
            f"{'Congradulations you beat' if player_total > bot_total else 'You lost to' if player_total < bot_total else 'You tied with'} {bot_ids[id].NAME}. {bot_ids[id].BLURB}"
        )

    return (
        jsonify(
            {
                "player_score": player_score,
                "bot_score": bot_score,
                "explanation": explanation,
                "response": response.value,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run()
