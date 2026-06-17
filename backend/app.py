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

@app.route("/state/ai")
def state_ai():
    global phase1_end
    if not phase1_end :
        state = game_phase1.get_state()
        phase1_end = state["done"]
        return jsonify(state)
    else :
        state = game_phase2.get_state()
        return jsonify(state)
    
@app.post("/step")
def step():
    global game_phase1, phase1_end

    if not phase1_end:
        result = game_phase1.step()
        phase1_end = result["done"]
        return jsonify(result)

    return jsonify(game_phase2.step())

# @app.route("/state/ai")
# def state_ai():

#     state = game_phase2.get_state()
#     return jsonify(state)
    
# @app.post("/step")
# def step():
#     global game_phase1, phase1_end

#     return jsonify(game_phase2.step())

@app.route("/state/manual")
def state_manual():
    global game_phase1
    return jsonify(game_phase1.get_state())

@app.post("/reset")
def reset():
    global game_phase1, game_phase2, phase1_end

    game_phase1 = Phase1()
    game_phase1.init_phase1()

    game_phase2 = Phase2()
    game_phase2.init_phase2()

    phase1_end = False

    return jsonify(game_phase1.get_state())

@app.post("/action/<action>")
def action(action):

    global game_phase1

    if action == "move":
        state = game_phase1.hitman.move()
        game_phase1.current_action = 'move'
        game_phase1.vision()
        game_phase1.hear()

    elif action == "left":
        state = game_phase1.hitman.turn_anti_clockwise()
        game_phase1.current_action = 'turn_anti_clockwise'

    elif action == "right":
        state = game_phase1.hitman.turn_clockwise()
        game_phase1.current_action = 'turn_clockwise'

    elif action == "kill":
        state = game_phase1.hitman.kill_target()
        game_phase1.current_action = 'kill'

    else:
        return jsonify({"error": "unknown action"}), 400
    
    game_phase1.phase1_list.append((state['position'][0], state['position'][1]))

    game_phase1.state = state

    return jsonify(game_phase1.convert_state(state))

# @app.route("/")
# def home():
#     return open("frontend_backup/index.html").read()

if __name__ == "__main__":
    app.run(debug=True)