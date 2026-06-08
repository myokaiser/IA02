from flask import Flask, jsonify
from flask_cors import CORS
from phase1 import Phase1
from phase2 import Phase2


app = Flask(__name__)
CORS(app)

game_phase1 = Phase1()
game_phase1.init_phase1()

game_phase2 = Phase2()
game_phase2.init_phase2()

phase1_end = False

@app.route("/state")
def state():
    global phase1_end
    if not phase1_end :
        step = game_phase1.step()
        phase1_end = step["done"]
        return jsonify(game_phase1.step())
    else :
        step = game_phase2.step()
        return jsonify(game_phase2.step())

@app.post("/reset")
def reset():
    global game_phase1, game_phase2, phase1_end

    game_phase1 = Phase1()
    game_phase1.init_phase1()

    game_phase2 = Phase2()
    game_phase2.init_phase2()

    phase1_end = False

    return jsonify(game_phase1.get_state("0", "0", "0"))

# @app.route("/")
# def home():
#     return open("frontend/index.html").read()

if __name__ == "__main__":
    app.run(debug=True)