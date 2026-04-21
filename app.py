from flask import Flask, render_template, request, jsonify
from game import QuoridorState
from ai import AI

app = Flask(__name__)

state = QuoridorState()
ai = AI()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/state")
def get_state():
    return jsonify({
        "pos": state.pos,
        "turn": state.turn,
        "walls": state.walls,
        "h_walls": state.h_walls,
        "v_walls": state.v_walls
    })


@app.route("/move", methods=["POST"])
def move():
    data = request.json
    c, r = data["c"], data["r"]

    if state.turn != 0:
        return jsonify({"error": "not your turn"})

    state.pos[0] = [c, r]
    state.turn = 1

    return jsonify({"ok": True})


@app.route("/ai")
def ai_move():
    move = ai.choose(state)

    if move[0] == "move":
        _, c, r = move
        state.pos[1] = [c, r]
    else:
        _, horiz, wc, wr = move
        state.place_wall(horiz, wc, wr)

    state.turn = 0
    return jsonify({"move": move})


if __name__ == "__main__":
    app.run(debug=True)