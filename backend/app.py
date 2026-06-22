from flask import Flask, jsonify, request
from flask_cors import CORS
from phase1 import Phase1
from phase2 import Phase2
from maps import load_map
from map import get_map_next_js
import os

# INITIALIZE FLASK APP ==
app = Flask(__name__)
CORS(app)

current_map = "map1"

game_phase1 = Phase1(current_map)
game_phase1.init_phase1()

game_phase2 = Phase2(current_map)
game_phase2.init_phase2()

phase1_end = False
# ========================


@app.route("/state/ai") # route for simulation mode
def state_ai() :
    global phase1_end
    if not phase1_end :
        state = game_phase1.get_state()
        phase1_end = state["done"]
        return jsonify(state)
    else :
        state = game_phase2.get_state()
        return jsonify(state)
    

    
@app.post("/step") # route for taking a step in the simulation
def step() :
    global game_phase1, phase1_end

    if not phase1_end :
        result = game_phase1.step()
        phase1_end = result["done"]
        return jsonify(result)

    return jsonify(game_phase2.step())



@app.route("/state/manual") # route for getting the manual state
def state_manual() :
    global game_phase1
    return jsonify(game_phase1.get_state())



@app.post("/reset")
def reset():

    global game_phase1
    global game_phase2
    global phase1_end

    game_phase1 = Phase1(current_map)
    game_phase1.init_phase1()

    game_phase2 = Phase2(current_map)
    game_phase2.init_phase2()

    phase1_end = False

    return jsonify(game_phase1.get_state())



@app.post("/action/<action>")
def action(action) :

    global game_phase1

    if action == "move" :
        state = game_phase1.hitman.move()
        game_phase1.current_action = 'move'
        game_phase1.vision()
        game_phase1.hear()

    elif action == "left" :
        state = game_phase1.hitman.turn_anti_clockwise()
        game_phase1.current_action = 'turn_anti_clockwise'

    elif action == "right" :
        state = game_phase1.hitman.turn_clockwise()
        game_phase1.current_action = 'turn_clockwise'

    elif action == "kill" :
        state = game_phase1.hitman.kill_target()
        game_phase1.current_action = 'kill'

    else:
        return jsonify({"error" : "unknown action"}), 400
    
    game_phase1.phase1_list.append((state['position'][0], state['position'][1]))

    game_phase1.state = state

    return jsonify(game_phase1.convert_state(state))



@app.post("/map")
def select_map() :

    global current_map

    data = request.get_json()
    current_map = data["map"]
    print("Current map =", current_map)

    return jsonify({"ok" : True})



@app.get("/maps")
def get_maps() :

    maps = []
    for file in os.listdir("maps") :
        if file.endswith(".py") and file != "__init__.py":
            maps.append(
                file.replace(".py", "")
            )

    return maps



@app.post("/map-preview")
def map_preview() :
    data = request.get_json()
    name = data["map"]

    world = load_map(name)
    world = get_map_next_js(world)

    return jsonify({
        "grid" : world
    })



if __name__ == "__main__" :
    app.run(debug = True)