from flask import Flask, jsonify
from backend.phase1 import Phase1

app = Flask(__name__)

game = Phase1()
game.init_phase1()

@app.route("/state")
def state():
    step = game.step()
    print("STEP", step)
    return jsonify(game.step())

@app.route("/")
def home():
    return open("frontend/index.html").read()

if __name__ == "__main__":
    app.run(debug=True)