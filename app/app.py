from flask import Flask, render_template
from game_models import GameState, Action

app: Flask = Flask(__name__)


@app.route("/")
def index():
    ...
    return render_template("index.html")


@app.route("/learn")
def learn():
    ...
    return render_template("learn.html")


@app.route("/play")
def play():
    ...
    return render_template("play.html")


@app.route("/api/game", methods=["POST"])
def game():
    ...
    return ""


if __name__ == "__main__":
    app.run()
