from map import Map, exactly_number, at_most_number, at_least_one, display_map_phase1
from hitman.hitman import HitmanReferee, HC
from typing import List, Dict, Tuple
import time
import copy
import heapq

Grid = List[List[int]] 
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]
Position = List[int]
Orientation = str #N,E,S,O


#-----------------------------Class Phase1------------------------------------------------
class Phase1():
    def __init__(self) -> None :
        self.hitman = HitmanReferee()
        self.state = self.hitman.start_phase1()
        self.map = Map(
            self.state["m"], # init x
            self.state["n"], # init y
            self.state["guard_count"], 
            self.state["civil_count"]
            )
        self.delay = 0.3
        self.last_update = time.time()
        self.done = False

    def init_phase1(self) -> None :
        self.nb_cases = self.map.nb_colonnes * self.map.nb_lignes
        self.phase1_list = [(
            self.state['position'][0], 
            self.state['position'][1]
            )]
        self.current_action = ""

        self.map.sat.add_clause(
            self.map.var_rien(self.state['position'])
        )

        self.map.set_grille_score(self.state['position'], -20)

        # file d'actions à jouer
        self.actions = []
        self.current_path = []

    def end_phase_1(self) -> Dict :
        dictionnaire =  self.map.known_Map()
        self.hitman.send_content(dictionnaire)
        _, score, _, true_map = self.hitman.end_phase1()
        print(score)
        print(true_map)
        return dictionnaire
    
    # convert values for nextjs app
    def convert_cell(self, v: object) -> str :
        return v.name if hasattr(v, "name") else str(v)
    
    def convert_map(self, map_dict: Dict) -> Dict :
        return {
            f"{x},{y}" : self.convert_cell(v)
            for (x, y), v in map_dict.items()
        }

    def get_state(self) -> Dict :
        return {
            "map" : self.convert_map(self.unknown_Map()),
            "nb_lignes" : self.map.nb_lignes,
            "nb_colonnes" : self.map.nb_colonnes,
            "position" : self.convert_cell(self.state["position"])[1:5],
            "orientation" : self.convert_cell(self.state["orientation"]),
            "done" : self.done,
            "phase" : self.state["phase"],
            "action" : self.current_action,
            "known" : self.map.cases_connues
        }

    # display map functions
    def affichage_jeu_phase1(self) -> None :
        display_map_phase1(self.map.known_Map(), self.state)

    def unknown_Map(self) -> Dict :
        known = copy.deepcopy(self.map.known_Map())
        known = self.map.reconstruct_map_for_state(known)
        path = set(self.phase1_list) 
        result = {}

        for x in range(self.map.nb_colonnes) :
            for y in range(self.map.nb_lignes) :

                pos = (x, y)
                value = known[pos]

                if pos in path :
                    result[pos] = value
                    continue

                if value != HC.EMPTY :
                    result[pos] = value
                    continue

                result[pos] = HC.UNKNOWN

        return result

    def get_guard_offset(self, guard: int) -> Tuple :
        if guard == HC.GUARD_N:
            offset = 0, 1
        elif guard == HC.GUARD_E:
            offset = 1, 0
        elif guard == HC.GUARD_S:
            offset = 0, -1
        elif guard == HC.GUARD_W:
            offset = -1, 0

        return offset

    def case_guard_vis(self, guard_x: int, guard_y: int, guard: int, dist=2) -> List :
        offset_x, offset_y = self.get_guard_offset(guard)
        pos = (guard_x, guard_y)
        x, y = pos
        vision = []
        for _ in range(0, dist) :
            pos = x + offset_x, y + offset_y
            x, y = pos
            if x >= self.state["n"] or y >= self.state["m"] or x < 0 or y < 0:
                break
            vision.append((x, y))

        return vision
    
    def get_civil_offset(self, civil: int) -> Tuple :
        if civil == HC.CIVIL_N:
            offset = 0, 1
        elif civil == HC.CIVIL_E:
            offset = 1, 0
        elif civil == HC.CIVIL_S:
            offset = 0, -1
        elif civil == HC.CIVIL_W:
            offset = -1, 0

        return offset
    
    def case_civil_vis(self, civil_x: int, civil_y: int, civil: int) -> List :
        offset_x, offset_y = self.get_civil_offset(civil)
        pos = (civil_x, civil_y)
        x, y = pos
        vision = [(pos)]

        pos = x + offset_x, y + offset_y
        x, y = pos
        if self.state["n"] > x >= 0 and self.state["m"] > y >= 0:
            vision.append((pos))
        return vision
    
    # phase1 specific gameplay functions
    def vision(self) -> int :

        nb_cases_visible = len(self.state['vision'])
        for i in range(nb_cases_visible) :
            is_a_personne = False

            score_case = 0
            
            coord_case = self.state['vision'][i][0] # extract coord of the case in front of him
            element = self.state['vision'][i][1] # determine the nature of the element (E, G, C) in this case
            
            if element == HC.WALL :
                score_case = float("-inf")
                clause_nature = self.map.var_mur(coord_case)
                self.map.sat.add_clause(clause_nature)
            elif element == HC.EMPTY :
                clause_nature = self.map.var_rien(coord_case)
                self.map.sat.add_clause(clause_nature)

                self.phase1_list.append(coord_case) # for unknow display map
            elif element == HC.TARGET :
                clause_nature = self.map.var_cible(coord_case)
                self.map.sat.add_clause(clause_nature)
            elif element == HC.PIANO_WIRE :
                clause_nature = self.map.var_corde(coord_case)
                self.map.sat.add_clause(clause_nature)
            elif element == HC.SUIT :
                clause_nature = self.map.var_costume(coord_case)
                self.map.sat.add_clause(clause_nature)
                
            elif element == HC.GUARD_E or element == HC.GUARD_N or element == HC.GUARD_S or element == HC.GUARD_W :
                
                is_a_personne = True # detect a person
                cases_vues = self.case_guard_vis(coord_case[0], coord_case[1], element)

                print(f"vision du garde ({coord_case[0]},{coord_case[1]}) : {cases_vues}")

                clause_type = self.map.var_guard(coord_case) # clause de guard
                self.map.sat.add_clause(clause_type)
                clause_not_type = self.map.var_not_civil(coord_case) # clause de non civil
                self.map.sat.add_clause(clause_not_type) # ajout de la clause

                for case in cases_vues : 
                    self.map.set_grille_score(case, -10)
                    self.map.add_dangerous_case(case)

                if element == HC.GUARD_E : 
                    clause_orientation = self.map.var_east(coord_case)
                elif element == HC.GUARD_N : 
                    clause_orientation = self.map.var_north(coord_case)
                elif element == HC.GUARD_S : 
                    clause_orientation = self.map.var_south(coord_case)
                elif element == HC.GUARD_W : 
                    clause_orientation = self.map.var_west(coord_case)

                self.map.sat.add_clause(clause_orientation)

            elif element == HC.CIVIL_E or element == HC.CIVIL_N or element == HC.CIVIL_S or element == HC.CIVIL_W :
                
                is_a_personne = True
                cases_vues = self.case_civil_vis(coord_case[0], coord_case[1], element)

                print(f"vision du civil ({coord_case[0]},{coord_case[1]}) : {cases_vues}")

                clause_type = self.map.var_civil(coord_case) # clause de civil
                self.map.sat.add_clause(clause_type) # ajout de la clause
                clause_not_type = self.map.var_not_guard(coord_case) # clause de non guard
                self.map.sat.add_clause(clause_not_type) # ajout de la clause

                for case in cases_vues : 
                    self.map.set_grille_score(case, -10)

                if element == HC.CIVIL_E : 
                    clause_orientation = self.map.var_east(coord_case)
                elif element == HC.CIVIL_N : 
                    clause_orientation = self.map.var_north(coord_case)
                elif element == HC.CIVIL_S : 
                    clause_orientation = self.map.var_south(coord_case)
                elif element == HC.CIVIL_W : 
                    clause_orientation = self.map.var_west(coord_case)

                self.map.sat.add_clause(clause_orientation)

            if is_a_personne == False :
                clause_personne = self.map.var_not_personne(coord_case)
                if self.map.get_grille_score(coord_case) >= 0 :
                    self.map.set_grille_score(coord_case, score_case)
            else :
                score_case = -15
                clause_personne = self.map.var_personne(coord_case)
                self.map.set_grille_score(coord_case, score_case)

            self.map.sat.add_clause(clause_personne)

            print(f"{element} en ({coord_case[0]}, {coord_case[1]})", end="|")
        print()
            
        return nb_cases_visible

    def hear(self) -> None :

        nb_personne_entendue = self.state["hear"]
        hitman_pos = self.state["position"]
        coord_cases = self.map.hear_case(hitman_pos)

        hear_zone = coord_cases

        guard_zone = []
        guard_vars = []
        
        if self.state["is_in_guard_range"]:

            for dx, dy in [
                (1,0), (-1,0),
                (2,0), (-2,0),
                (0,1), (0,-1),
                (0,2), (0,-2)
            ]:
                x = hitman_pos[0] + dx
                y = hitman_pos[1] + dy

                if 0 <= x < self.map.nb_colonnes and 0 <= y < self.map.nb_lignes:
                    guard_zone.append((x,y))

                    guard_vars.append(
                        self.map.var_guard((x,y))[0]
                    )
        
        if guard_vars:
            self.map.sat.add_clause(
                at_least_one(guard_vars)
            )

        if nb_personne_entendue == 0:

            for coord in hear_zone:
                self.map.sat.add_clause(
                    self.map.var_not_personne(coord)
                )
            return

        personnes_connues = 0
        variables_inconnues = []

        for coord in coord_cases:

            v_personne = self.map.var_personne(coord)[0]

            result_p = self.map.sat.solve(assumptions = [v_personne])
            result_non_p = self.map.sat.solve(assumptions = [-v_personne])

            # personne certaine
            if result_p and not result_non_p :
                personnes_connues += 1

            # personne impossible
            elif (not result_p) and result_non_p :
                continue

            # inconnu
            else:
                # priorité aux cases dans guard_zone
                if coord in guard_zone:
                    variables_inconnues.insert(0, v_personne)  # priorité haute
                else:
                    variables_inconnues.append(v_personne)

        reste = nb_personne_entendue - personnes_connues

        if reste < 0 :
            raise Exception("hear incohérent avec les connaissances SAT")
        
        if reste == 0 :
            for v in variables_inconnues:
                self.map.sat.add_clause([-v])
            return

        if variables_inconnues :
            clauses = exactly_number(variables_inconnues, reste)

            for clause in clauses :
                self.map.sat.add_clause(clause)

    #=================================================================================

    def build_frontier(self) -> List :

        frontier = []
        known_map = self.map.known_Map()

        for x in range(self.map.nb_colonnes) :
            for y in range(self.map.nb_lignes) :

                pos = (x, y)
                if self.map.get_grille_score(pos) != 20 :
                    continue

                for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)] :
                    neigh = (x+dx, y+dy)
                    if neigh in known_map and self.map.get_grille_score(neigh) != 20 :
                        frontier.append(pos)
                        break
        # print("frontier", frontier)
        return frontier

    def heuristique(self, position: Tuple, target: Tuple) -> int :
        return abs(position[0] - target[0]) + abs(position[1] - target[1])
                
    def exploration_score(self, pos) -> int :

        score = 0

        # frontière
        score += 50

        # distance
        dist = self.heuristique(self.state["position"], pos)
        score -= dist
        # déjà visité
        if pos in self.phase1_list:
            score -= 20
        # personne possible
        if self.map.case_maybe_personne(pos):
            print("MAYBE PERSON", pos)
            score -= 15
        # vision connue
        if self.map.case_not_safe(pos):
            print("NOT SAFE", pos)
            score -= 20

        score += self.map.get_grille_score(pos)

        return score

    def choose_frontier(self) -> Tuple[int,int] :

        frontier = self.build_frontier()

        if not frontier :
            return None

        best = None
        best_score = float("-inf")

        for pos in frontier :

            s = self.exploration_score(pos)

            if s > best_score:
                best_score = s
                best = pos

        return best
    
    def est_position_valide_phase1(self, pos) -> bool :
        # print("thinking position...", end = "")
        carte = self.map.known_Map().keys()
        if pos not in carte :
            return False

        if self.map.case_mur(pos) :
            return False

        if self.map.case_personne(pos) :
            return False

        return True
    
    def movement_cost(self, pos) -> int :
        # print("thinking movement...", end = "")
        cost = 1

        if pos in self.phase1_list:
            cost += 3

        if self.map.case_maybe_personne(pos):
            cost += 10

        if self.map.case_not_safe(pos):
            cost += 10

        return cost
    
    def build_path_exploration(self) -> List | None :

        target = self.choose_frontier()
        print("target chosen", target)

        if target is None:
            return None

        position = self.state["position"]
        priority = []
        visited = set()

        heapq.heappush(
            priority,
            (self.heuristique(position, target), 0, position, [position])
        )

        while priority :

            _, g, current_pos, path = heapq.heappop(priority)

            if current_pos == target :
                return path

            if current_pos in visited :
                continue

            visited.add(current_pos)

            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)] :
                new_pos = (
                    current_pos[0] + dx,
                    current_pos[1] + dy
                )

                if not self.est_position_valide_phase1(new_pos) :
                    continue

                if new_pos in visited :
                    continue

                new_path = path + [new_pos]

                move_cost = self.movement_cost(new_pos)

                new_g = g + move_cost

                heapq.heappush(
                    priority,
                    (self.heuristique(new_pos, target) + new_g, new_g, new_pos, new_path)
                )

        return None
    
    def direction(self, initial: Tuple, final: Tuple) -> Orientation :
        pos = initial
        res = tuple(x - y for x, y in zip(final, pos))
        if abs(res[0]) > abs(res[1]) :
            if res[0] < 0 :
                return "W"
            elif res[0] > 0 :
                return "E"
        elif abs(res[0]) < abs(res[1]) :
            if res[1] < 0 :
                return "S"
            elif res[1] > 0 :
                return "N"
    
    def get_turns(self, direction: Tuple, hitman: Tuple) -> int :
        listeasc = ['N', 'E', 'S', 'W']
        if direction == hitman :
            return 0
        else :
            diff = listeasc.index(direction) - listeasc.index(hitman)
            if diff > 0 :
                if diff > 2 :
                    return diff - 4
                else:
                    return diff
            else:
                if diff < -2 :
                    return diff + 4
                else:
                    return diff
    
    def orientation_choix(self, choice: int) -> List :
        #bouge ou oriente le perso en fonction du resultat de get_turns
        liste = []
        if choice == 0 :
            liste += ["hr.move()"]
        elif choice == -1 :
            liste += ["hr.turn_anti_clockwise()"]
            liste += ["hr.move()"]
        elif choice == 1 :
            liste += ["hr.turn_clockwise()"]
            liste += ["hr.move()"]
        elif abs(choice) == 2 :
            liste += ["hr.turn_clockwise()"]
            liste += ["hr.turn_clockwise()"]
            liste += ["hr.move()"]
        return liste
    
    def mouvement(self, initial: Tuple, final: Tuple, liste: List, state: Dict) -> List :
        pos = initial
        if len(liste) == 1 :
            orient = state["orientation"].name
        else :
            orient = self.direction(liste[len(liste) - 2], liste[len(liste) - 1])
        direct = self.direction(pos, final)
        choix = self.get_turns(direct, orient)
        return self.orientation_choix(choix)

    def build_actions_from_path(self, path: List) -> List :

        actions = []

        if path != None :
            for i in range(len(path)-1) :

                mouvements = self.mouvement(path[i], path[i+1], path[:i+1], self.state)
                for m in mouvements :
                    actions.append(m)

        return actions
    
    def prepare_actions(self) -> None :

        self.current_path = self.build_path_exploration()
        print("path", self.current_path)

        self.actions = self.build_actions_from_path(self.current_path)

    def execute_action(self, action: str) -> None :

        actions = {
            "hr.move()" : self.hitman.move,
            "hr.turn_clockwise()" : self.hitman.turn_clockwise,
            "hr.turn_anti_clockwise()" : self.hitman.turn_anti_clockwise,
            "hr.neutralize_guard()" : self.hitman.neutralize_guard,
        }
        print(f"action jouée : {action}")
        self.state = actions[action]()
        self.current_action  = action[3:].replace("()", "  ")

    def next_step_valid(self) -> bool :

        if self.current_path is None :
            return False

        current_pos = self.state["position"]

        try:
            idx = self.current_path.index(current_pos)
        except ValueError :
            return False

        if idx + 1 >= len(self.current_path) :
            return True

        next_pos = self.current_path[idx + 1]

        if self.map.case_mur(next_pos) :
            return False

        if self.map.case_personne(next_pos) :
            return False

        if self.map.case_not_safe(next_pos) : # if not safe, recompute path
            return False
        
        if len(self.current_path) > 0 : # if target can be defined, no need to go on it
            current_target = self.current_path[-1]
            if self.map.get_grille_score(current_target) != 20 :
                return False

        return True

    def step(self) -> Dict :

        # print("SAT global =", self.map.sat.solve([]))
        print(self.map.grille_scores)

        if self.map.early_stopping() :
            self.done = True
            return self.get_state()

        now = time.time()
        if self.done :
            return self.get_state()
        
        if now - self.last_update < self.delay :
            return self.get_state()
        
        self.phase1_list.append((
            self.state['position'][0], 
            self.state['position'][1]
        ))

        self.vision()
        self.hear()
        self.affichage_jeu_phase1()

        if not self.next_step_valid() :

            # print("NEXT STEP BLOQUE")

            self.actions = []
            self.prepare_actions()

        # Plus d'actions à jouer ?
        if len(self.actions) == 0 :

            self.prepare_actions()

            if len(self.actions) == 0 :
                self.done = True
                return self.get_state()

        action = self.actions.pop(0)

        self.execute_action(action)
        return self.get_state()
