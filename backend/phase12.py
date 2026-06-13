from map import Map, exactly_number, at_most_number, at_least_number, display_map_phase1
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
        self.delay = 0.1
        self.last_update = time.time()
        self.done = False

    def init_phase1(self) -> None :
        self.it = 0
        self.nb_cases = self.map.nb_colonnes * self.map.nb_lignes
        self.phase1_list = [(
            self.state['position'][0], 
            self.state['position'][1]
            )]
        self.action = "blocage"
        self.rotate_action = []
        self.action_done = False
        self.current_action = ""
        self.nb_co = ""
        self.iteration = ""
        self.position = ""
        self.score = ""
        self.map.clauses_connues.append(
            self.map.var_rien((
                self.state['position'][0],
                self.state['position'][1]
            ))
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
            "nb_co" : self.nb_co,
            "iteration" : self.iteration,
            "score" : self.score,
            "done" : self.done,
            "phase" : self.state["phase"],
            "action" : self.current_action
        }

    # display map functions
    def affichage_jeu_phase1(self) -> None :
        display_map_phase1(self.map.known_Map(), self.position, self.iteration, self.score, self.nb_co, self.state)

    def unknown_Map(self) -> Dict :
        known = copy.deepcopy(self.map.known_Map())
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

    def get_guard_offset(self, guard: int):
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
    
    def get_civil_offset(self, civil: int):
        if civil == HC.CIVIL_N:
            offset = 0, 1
        elif civil == HC.CIVIL_E:
            offset = 1, 0
        elif civil == HC.CIVIL_S:
            offset = 0, -1
        elif civil == HC.CIVIL_W:
            offset = -1, 0

        return offset
    
    def case_civil_vis(self, civil_x: int, civil_y: int, civil: int):
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
                clause = self.map.var_mur(coord_case)
            elif element == HC.EMPTY :
                clause = self.map.var_rien(coord_case)
            elif element == HC.TARGET :
                clause = self.map.var_cible(coord_case)
            elif element == HC.PIANO_WIRE :
                clause = self.map.var_corde(coord_case)
            elif element == HC.SUIT :
                clause = self.map.var_costume(coord_case)
                
            elif element == HC.GUARD_E or element == HC.GUARD_N or element == HC.GUARD_S or element == HC.GUARD_W :
                is_a_personne = True # detect a person
                cases_vues = self.case_guard_vis(coord_case[0], coord_case[1], element)
                print(f"vision du garde ({coord_case[0]},{coord_case[1]}) : {cases_vues}")
                for case in cases_vues : 
                    clause_safe = self.map.var_not_safe(case)
                    self.map.sat.add_clause(clause_safe)
                if element == HC.GUARD_E : 
                    clause = self.map.var_guard_e(coord_case)
                elif element == HC.GUARD_N : 
                    clause = self.map.var_guard_n(coord_case)
                elif element == HC.GUARD_S : 
                    clause = self.map.var_guard_s(coord_case)
                elif element == HC.GUARD_W : 
                    clause = self.map.var_guard_w(coord_case)

            elif element == HC.CIVIL_E or element == HC.CIVIL_N or element == HC.CIVIL_S or element == HC.CIVIL_W :
                is_a_personne = True
                cases_vues = self.case_civil_vis(coord_case[0], coord_case[1], element)
                print(f"vision du civil ({coord_case[0]},{coord_case[1]}) : {cases_vues}")
                for case in cases_vues : 
                    clause_safe = self.map.var_not_safe(case)
                    self.map.sat.add_clause(clause_safe)

                if element == HC.CIVIL_E : 
                    clause = self.map.var_civil_e(coord_case)
                elif element == HC.CIVIL_N : 
                    clause = self.map.var_civil_n(coord_case)
                elif element == HC.CIVIL_S : 
                    clause = self.map.var_civil_s(coord_case)
                elif element == HC.CIVIL_W : 
                    clause = self.map.var_civil_w(coord_case)

            if is_a_personne == False :
                clause_personne = self.map.var_not_personne(coord_case) #TODO temp remove
                if self.map.get_grille_score(coord_case) >= 0 :
                    self.map.set_grille_score(coord_case, score_case)
            else :
                score_case = -15
                clause_personne = self.map.var_personne(coord_case) #TODO temp remove
                self.map.set_grille_score(coord_case, score_case)
            # self.map.add_person_clause(clause_personne)
            self.map.sat.add_clause(clause_personne) #TODO temp remove
            self.map.add_known_clause(clause)
            self.map.sat.add_clause(clause)
            print(f"{element} en ({coord_case[0]}, {coord_case[1]})", end="|")
        print()
            
        return nb_cases_visible

    def hear(self) -> None :
        nb_personne_entendue = self.state['hear'] # nombre de personnes entendu dans un périmètre de 2
        # print("nb", nb_personne_entendue)
        
        coord_cases = self.map.hear_case(self.state['position']) # coordonnées des cases dans le périmètre d'écoute d'hitman
        # print("coord hear", coord_cases)
        
        variables_personnes = []
        for coord in coord_cases :
            if nb_personne_entendue == 0 : # aucune personne dans le périmètre
                clause = self.map.var_not_personne((coord[1], coord[0])) #TODO à changer et mettre uniquement coord
                # self.map.add_person_clause(clause) # ne sert pas
                self.map.sat.add_clause(clause)
            else :
                clause = self.map.var_personne((coord[1], coord[0]))
                if self.map.known_case(coord[0], coord[1]) == False : # si la personne n'est pas connu de la carte
                    variables_personnes.append(clause[0]) # extrait de la valeur de laclause hors de sa liste

        if variables_personnes != [] :
            clauses = exactly_number(
                variables_personnes,
                nb_personne_entendue
            )

            for clause in clauses:
                self.map.sat.add_clause(clause)

    #=================================================================================
    def build_frontier(self):

        frontier = []
        known_map = self.map.known_Map()

        for x in range(self.map.nb_colonnes):
            for y in range(self.map.nb_lignes):

                pos = (x, y)
                if self.map.get_grille_score(pos) != 20:
                    continue

                for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                    neigh = (x+dx, y+dy)
                    if neigh in known_map and self.map.get_grille_score(neigh) != 20:
                        frontier.append(pos)
                        break
        print("frontier", frontier)
        # print("known_map", known_map)
        return frontier

    def heuristique(self, position: Tuple, target: Tuple) -> int :
        return abs(position[0] - target[0]) + abs(position[1] - target[1])
                
    def exploration_score(self, pos):

        score = 0
        x, y = pos

        # frontière
        score += 50

        # distance
        dist = self.heuristique(
            self.state["position"],
            pos
        )
        score -= dist
        # déjà visité
        if pos in self.phase1_list:
            score -= 20
        # personne possible
        if self.map.case_maybe_personne(y, x):
            score -= 15
        # vision connue
        if self.map.case_not_safe(y, x):
            score -= 10

        return score

    def choose_frontier(self):

        frontier = self.build_frontier()

        if not frontier:
            return None

        best = None
        best_score = float("-inf")

        for pos in frontier:

            s = self.exploration_score(pos)

            if s > best_score:
                best_score = s
                best = pos

        return best
    
    def est_position_valide_phase1(self, pos):
        carte = self.map.known_Map().keys()
        if pos not in carte:
            return False

        x, y = pos

        if self.map.case_mur(pos):
            return False

        if self.map.case_personne(y, x):
            return False

        return True
    
    def movement_cost(self, pos):

        x, y = pos

        cost = 1

        if pos in self.phase1_list:
            cost += 3

        if self.map.case_maybe_personne(y, x):
            cost += 5

        if self.map.case_not_safe(y, x):
            cost += 5

        return cost
    
    def build_path_exploration(self):

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

        while priority:

            _, g, current_pos, path = heapq.heappop(priority)

            if current_pos == target:
                return path

            if current_pos in visited:
                continue

            visited.add(current_pos)

            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                new_pos = (
                    current_pos[0] + dx,
                    current_pos[1] + dy
                )

                if not self.est_position_valide_phase1(new_pos):
                    continue

                if new_pos in visited:
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

    def next_step_valid(self):

        if self.current_path is None:
            return False

        current_pos = self.state["position"]

        try:
            idx = self.current_path.index(current_pos)
        except ValueError:
            return False

        if idx + 1 >= len(self.current_path):
            return True

        next_pos = self.current_path[idx + 1]

        x, y = next_pos

        if self.map.case_mur(next_pos):
            return False

        if self.map.case_personne(y, x):
            return False

        return True

    def step(self) -> Dict :

        print("SAT global =", self.map.sat.solve([]))
        print(self.map.grille_scores)

        self.vision()
        # self.hear() #TODO temp remove
        self.affichage_jeu_phase1() #TODO affichage already in main file while running the programm

        if not self.next_step_valid():

            print("NEXT STEP BLOQUE")

            self.actions = []
            self.prepare_actions()

        now = time.time()
        if self.done :
            return self.get_state()
        
        if now - self.last_update < self.delay :
            return self.get_state()

        # Plus d'actions à jouer ?
        if len(self.actions) == 0 :

            self.prepare_actions()

            if len(self.actions) == 0 :
                self.done = True
                return self.get_state()

        action = self.actions.pop(0)

        self.execute_action(action)
        # self.affichage_jeu_phase1() #TODO affichage already in main file while running the programm

        return self.get_state()
