from map import Map, exactly_number, at_most_number, at_least_number, display_map_phase1
from hitman.hitman import HitmanReferee, HC
from typing import List, Dict, Tuple
import time
import copy

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
        # print("KNOWN", self.map.known_Map())
        # print("POSITION", position)
        # print("STATE", self.state)
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
            
            coord_case = self.state['vision'][i][0] # extract coord of the case in front of him
            element = self.state['vision'][i][1] # determine the nature of the element (E, G, C) in this case
            if element == HC.WALL :
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
                clause_personne = self.map.var_personne(coord_case)
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
                clause_personne = self.map.var_not_personne(coord_case)
            else :
                clause_personne = self.map.var_personne(coord_case)
            # self.map.add_person_clause(clause_personne)
            self.map.sat.add_clause(clause_personne)
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
                    
            # if nb_personne_entendue == 5 :
            #     if self.map.nb_gardes + self.map.nb_civils <= 5 :
            #         clauses = at_most_number(variables_personnes, nb_personne_entendue)
            #         for clause in clauses : 
            #             self.map.add_person_prob_clause(clause)
                        
            #     else:
            #         pass

    def case_more_safe(self, cases: list) -> Tuple :
        unsafe = []
        safe = []
        scores = []
        nb_pos = []
        id = 0
        for case in cases : 
            
            if self.map.case_not_safe(case[0],case[1]) == True :
                unsafe.append(case)
            else : 
                case_safe = self.map.case_safe(case[0], case[1])
                scores.append(self.map.get_grille_score(case[0], case[1]))
                safe.append(case)
                nb_pos.append(0)
                for case_safety in case_safe :  
                    if self.map.case_maybe_personne(case_safety[0],case_safety[1]) == True : 
                        scores[id] -= 1
                        nb_pos[id] += 1
                    
                id += 1
        print(f"cases not safe : {unsafe}")
        if len(safe) == -1 : 
            return unsafe[0]
        else : 
            print(f"cases safe : {safe}")
            max = scores[0]
            case_suivante = safe[0]
            for num in range(id) : 
                print(f"{safe[num]} | score de la case : {scores[num]} | nb d'incertitude :{nb_pos[num]}")
                if scores[num] > max : 
                    max = scores[num]
                    case_suivante = safe[num]
            if max < -18 and len(unsafe) > 0 :
                return unsafe[0]
                    
        return case_suivante

    def set_orientation_case_suiv(self, ligne:int, colonne:int) -> None :
        orientation = self.state['orientation']
        pos = self.state['position']
        if orientation == HC.N :
            if ligne == pos[1] - 1 :
                self.rotate_action.append("hr.turn_clockwise()")
                self.rotate_action.append("hr.turn_clockwise()")
            elif colonne == pos[0] - 1 :
                self.rotate_action.append("hr.turn_anti_clockwise()")
            elif colonne == pos[0] + 1 :
                self.rotate_action.append("hr.turn_clockwise()")

        elif orientation == HC.E :
            if ligne == pos[1] - 1 :
                self.rotate_action.append("hr.turn_clockwise()")
            elif ligne == pos[1] + 1 :
                self.rotate_action.append("hr.turn_anti_clockwise()")
            elif colonne == pos[0] - 1 :
                self.rotate_action.append("hr.turn_clockwise()")
                self.rotate_action.append("hr.turn_clockwise()") 
        
        elif orientation == HC.S :
            if ligne == pos[1] + 1 :
                self.rotate_action.append("hr.turn_clockwise()")
                self.rotate_action.append("hr.turn_clockwise()")
            elif colonne == pos[0] - 1 :
                self.rotate_action.append("hr.turn_clockwise()")
            elif colonne == pos[0] + 1 :
                self.rotate_action.append("hr.turn_anti_clockwise()")
        
        elif orientation == HC.W :
            if ligne == pos[1] + 1 :
                self.rotate_action.append("hr.turn_clockwise()")
            elif ligne == pos[1] - 1 :
                self.rotate_action.append("hr.turn_anti_clockwise()")
            elif colonne == pos[0] + 1 :
                self.rotate_action.append("hr.turn_clockwise()")
                self.rotate_action.append("hr.turn_clockwise()")

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

    def step(self) -> Dict :

        print("action", self.action)

        now = time.time()
        if self.done :
            return self.get_state()
        
        nb_cases_trouvees = self.map.nb_known_case()

        # arrêt
        # if self.it >= 2 * self.nb_cases :
        #     self.done = True

        if nb_cases_trouvees >= self.map.nb_cases_a_trouver :
            print("END PHASE1")
            self.done = True

        # stockage position
        self.phase1_list.append((
            self.state['position'][0],
            self.state['position'][1]
        ))

        self.nb_co = f"Nb cases connues : {nb_cases_trouvees}"
        self.position = f"position : ({self.state['position'][0]} , {self.state['position'][1]})"
        self.iteration = f"ITERATION : {self.it}"
        self.score = "Score vision : 0"

        if now - self.last_update < self.delay :
            return self.get_state()
        
        if self.action == 'blocage' and not self.action_done :
            #========================================================
            # blocage decision        
            self.vision()
            self.hear()

            self.map.set_grille_score(self.state['position'][1], self.state['position'][0], -6)
            
            if not self.map.case_go(self.state['position'][1], self.state['position'][0]) :
                self.action_done = True
                for i in range(3) :
                    self.score = f"Score vision : {i+1}"
                    self.state = self.hitman.turn_anti_clockwise()
                    self.current_action = "turn_anti_clockwise"
                    self.affichage_jeu_phase1()
                    self.vision()

                    if self.map.case_go(self.state['position'][1], self.state['position'][0]) :
                        break
            else :
                self.action_done = False

            self.action = 'rotate_choice'
            #========================================================

        if self.action == 'rotate_choice' and not self.action_done :
            #========================================================
            # rotate decision
            move_case = self.map.move_case(self.state['position'][1], self.state['position'][0])
            cases_possible_deplacement = []
            for case in move_case :
                if not self.map.case_mur(case[0], case[1]) and not self.map.case_personne(case[0], case[1]) :
                    cases_possible_deplacement.append(case)

            if len(cases_possible_deplacement) >= 1 :
                case_suivante = self.case_more_safe(cases_possible_deplacement)
            else :
                case_suivante = cases_possible_deplacement[0]

            self.set_orientation_case_suiv(case_suivante[0], case_suivante[1])
            if self.rotate_action != [] :
                self.action_done = True
                rotate = self.rotate_action.pop(0)
                self.execute_action(rotate)
            else :
                self.action_done = False

            self.action = 'rotate'
            #========================================================

        if self.action == 'rotate' and not self.action_done :
            if self.rotate_action != [] :
                self.action_done = True
                rotate = self.rotate_action.pop(0)
                self.current_action = rotate
                self.execute_action(rotate)
                self.action = 'rotate'
            else :
                self.action_done = False
                clause_passage = self.map.var_pass_case((self.state['position'][0], self.state['position'][1]))
                self.map.add_pass_clause(clause_passage)
                self.map.sat.add_clause(clause_passage)
                self.action = 'move'


        if self.action == 'move' and not self.action_done :
            #========================================================
            # move decision
            self.action_done = True
            self.state = self.hitman.move()
            self.current_action = 'move'
            self.affichage_jeu_phase1()
            self.action = 'blocage'
            self.it += 1
            #========================================================

        print("Nouvelle action :", self.action)
        self.action_done = False
        self.last_update = now

        return self.get_state()
