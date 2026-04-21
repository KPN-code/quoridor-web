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


# ── Pelaajan siirto ─────────────────────────────────────────────
@app.route("/move", methods=["POST"])
def move():
    data = request.json

    if state.turn != 0:
        return jsonify({"error": "not your turn"})

    # nappulaliike
    if data["type"] == "move":
        c, r = data["c"], data["r"]

        if [c, r] not in state.legal_moves(0):
            return jsonify({"error": "illegal move"})

        state.pos[0] = [c, r]
        state.turn = 1
        return jsonify({"ok": True})

    # seinä
    elif data["type"] == "wall":
        if state.walls[0] <= 0:
            return jsonify({"error": "no walls left"})

        horiz = data["horiz"]
        wc = data["wc"]
        wr = data["wr"]

        if not state.place_wall(horiz, wc, wr):
            return jsonify({"error": "illegal wall"})

        state.turn = 1
        return jsonify({"ok": True})

    return jsonify({"error": "invalid request"})


# ── AI ──────────────────────────────────────────────────────────
@app.route("/ai")
def ai_move():
    if state.turn != 1:
        return jsonify({"error": "not AI turn"})

    move = ai.choose(state)

    if move is None:
        return jsonify({"error": "ai failed"})

    if move[0] == "move":
        _, c, r = move
        state.pos[1] = [c, r]
    else:
        _, horiz, wc, wr = move
        state.place_wall(horiz, wc, wr)

    state.turn = 0
    return jsonify({"move": move})


# ── Reset (debug helpottaa) ─────────────────────────────────────
@app.route("/reset")
def reset():
    global state
    state = QuoridorState()
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
