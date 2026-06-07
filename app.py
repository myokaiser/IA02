from flask import Flask, jsonify
from backend.phase1 import Phase1
from backend.phase2 import Phase2


app = Flask(__name__)

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
        print("STEP", step)
        phase1_end = step["done"]
        return jsonify(game_phase1.step())
    else :
        step = game_phase2.step()
        print("STEP", step)
        return jsonify(game_phase2.step())

@app.route("/")
def home():
    return open("frontend/index.html").read()

if __name__ == "__main__":
    app.run(debug=True)