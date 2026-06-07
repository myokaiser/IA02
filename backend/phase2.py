from map import display_map_phase2
from hitman.hitman import HC, HitmanReferee
from pprint import pprint
from typing import List, Tuple, Dict
import time
import heapq

Grid = List[List[int]] 
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]
Position = [int,int] # position x y
Orientation = str #N,E,S,O

class Phase2():
    def __init__(self) -> None:
        self.hitman = HitmanReferee()
        self.state = self.hitman.start_phase2()

    def trouver_corde(self, carte: Dict) -> Tuple: #TODO trouver la corde
        for cle, valeur in carte.items():
            if valeur == HC.PIANO_WIRE:
                return cle
        return None

    def trouver_cible(self, carte: Dict) -> Tuple: #TODO trouver la cible
        for cle, valeur in carte.items():
            if valeur == HC.TARGET:
                return cle
        return None

    def trouver_suit(self, carte: Dict) -> Tuple: #TODO trouver la cible
        for cle, valeur in carte.items():
            if valeur == HC.SUIT:
                return cle
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
        
    def get_turns(self, direction: Tuple, hitman: Tuple) -> int:
        listeasc = ['N', 'E', 'S', 'W']
        if direction == hitman :
            return 0
        else :
            diff = listeasc.index(direction) - listeasc.index(hitman)
            if diff > 0:
                if diff > 2:
                    return diff - 4
                else:
                    return diff
            else:
                if diff < -2:
                    return diff + 4
                else:
                    return diff
    
    def heuristique(self, position: Tuple, target: Tuple) -> int:
        return abs(position[0] - target[0]) + abs(position[1] - target[1])

    def vision_guard(self, position: Tuple, carte: Dict) -> bool :
        vision = False
        for i in range(5) :
            for j in range(5) :
                posx = position[0]-i+2
                posy = position[1]-j+2
                try :
                    case = carte[(posx, posy)]
                    if "GUARD_" in case.name :
                        if self.direction((posx, posy), position) in case.name and (posx == position[0] or posy == position[1]) :
                            #print("ATTENTION UN GARDE REGARDE LA CASE, IL EST EN POSITION X =", position[0]-i+2, ",Y =", position[1]-j+2)
                            vision = True
                except :
                    pass
        return vision

    def vision_civil(self, position: Tuple, carte: Dict) -> bool :
        vision = False
        for i in range(3) :
            for j in range(3) :
                posx = position[0]-i+1
                posy = position[1]-j+1
                try :
                    case = carte[(posx, posy)]
                    if "CIVIL_" in case.name :
                        if self.direction((posx, posy), position) in case.name and (posx == position[0] or posy == position[1]) :
                            #print("ATTENTION UN CIVIL REGARDE LA CASE, IL EST EN POSITION X =", position[0]-i+1, ",Y =", position[1]-j+1)
                            vision = True
                except :
                    pass
        return vision

    def neutra_guard(self, hitman: Tuple, position: Tuple, carte: Dict) -> int :
        if "GUARD_" in carte[(position[0], position[1])].name :
            if self.direction(hitman, position) in carte[(position[0], position[1])].name :
                return 2
            else :
                return 0
        else :
            return 1
    
    def orientation_choix(self, pos: Tuple, final: Tuple, carte: Dict, choice: int) -> List : #bouge ou oriente le perso en fonction du resultat de get_turns
        liste = []
        if choice == 0 and self.neutra_guard(pos, final, carte) == 2:
            liste += ["hr.neutralize_guard()"]
            liste += ["hr.move()"]
        elif choice == 0 :
            liste += ["hr.move()"]
        elif choice == -1:
            liste += ["hr.turn_anti_clockwise()"]
            liste += ["hr.move()"]
        elif choice == 1:
            liste += ["hr.turn_clockwise()"]
            liste += ["hr.move()"]
        elif abs(choice) == 2:
            liste += ["hr.turn_clockwise()"]
            liste += ["hr.turn_clockwise()"]
            liste += ["hr.move()"]
        return liste
    
    def mouvement(self, initial: Tuple, final: Tuple, liste: List, state: Dict, carte: Dict) -> List :
        pos = initial
        if len(liste) == 1 :
            orient = state["orientation"].name
        else :
            orient = self.direction(liste[len(liste)-2], liste[len(liste)-1])
        direct = self.direction(pos, final)
        choix = self.get_turns(direct, orient)
        return self.orientation_choix(pos, final, carte, choix)

    def est_position_valide(self, hitman: Tuple, position: Tuple, carte: Dict, maniere: bool, neutra: bool) -> bool :
        if position not in carte:
            return False
        case = carte[position]
        if neutra == False :
            if maniere == False :
                if case == HC.WALL or "GUARD_" in case.name or self.vision_guard(position, carte) or self.vision_civil(position, carte) :
                    return False
                return True
            else :
                if case == HC.WALL or "GUARD_" in case.name :
                    return False
                return True
        else :
            if maniere == False :
                if case == HC.WALL or self.neutra_guard(hitman, position, carte) == 0 or self.vision_guard(position, carte) or self.vision_civil(position, carte) :
                    return False
                return True
            else :
                if case == HC.WALL or self.neutra_guard(hitman, position, carte) == 0 :
                    return False
                return True
        
    def matrix_to_dico(self, ref: List[List]) -> Dict :
        carte = {}
        for y, row in enumerate(ref):
            for x, cell in enumerate(row):
                carte[(x, len(ref)-1-y)] = cell
        return carte
    
    def convert_cell(self, v):
        return v.name if hasattr(v, "name") else str(v)
    
    def convert_map(self, map_dict: Dict):
        return {
            f"{x},{y}": self.convert_cell(v)
            for (x, y), v in map_dict.items()
        }

    def get_state(self):
        print("RAW STATE -- ", self.state)
        print("POS", str(self.state["position"]), type(self.state["position"]))
        print("STATE", self.state)
        return {
            "map": self.convert_map(self.carte),   # ou ta structure actuelle
            "position": self.convert_cell(str(self.state["position"]))[1:5],
            "orientation": self.convert_cell(self.state["orientation"]),
            "done": self.done,
            "phase": self.state["phase"]
        }
    
    def set_objectif(self):

        self.current_pos = self.state["position"]

        # Cas particulier :
        # on voulait passer devant les gardes mais on n'a pas encore le costume
        if self.way and not self.state["has_suit"]:

            self.target = self.trouver_suit(self.carte)
            self.goal = "suit"

            self.way = False
            self.neutra = False

            return

        # Pas encore arrivé à destination
        if self.current_pos != self.target:
            return

        print(
            "Objectif atteint :",
            self.goal,
            "à",
            self.current_pos
        )

        # ==========================
        # CORDE
        # ==========================

        if self.goal == "weapon":

            self.state = self.hitman.take_weapon()

            if self.state["has_weapon"]:

                self.target = self.trouver_cible(self.carte)
                self.goal = "target"

                if self.state["has_suit"]:
                    self.way = True
                else:
                    self.way = False

                self.neutra = False

            return

        # ==========================
        # CIBLE
        # ==========================

        if self.goal == "target":
            print("TARGET")
            self.state = self.hitman.kill_target()

            if self.state["is_target_down"]:
                print("HITMAN KILLED THE TARGET")
                self.target = (0, 0)
                self.goal = "finish_the_mission"

                if self.state["has_suit"]:
                    self.way = True
                else:
                    self.way = False

                self.neutra = False

            return

        # ==========================
        # COSTUME
        # ==========================

        if self.goal == "suit":

            self.state = self.hitman.take_suit()
            self.state = self.hitman.put_on_suit()

            if self.state["has_weapon"]:

                self.target = self.trouver_cible(self.carte)
                self.goal = "target"

            else:

                self.target = self.trouver_corde(self.carte)
                self.goal = "weapon"

            self.way = True
            self.neutra = False

            return

        # ==========================
        # SORTIE
        # ==========================

        if self.goal == "finish_the_mission":
            print("FINISH")
            # self.state = self.hitman.end_phase2()

            self.done = True

            return
    
    def init_phase2(self):

        self.goal = "weapon"

        self.carte = self.matrix_to_dico(self.hitman._HitmanReferee__world)

        self.target = self.trouver_corde(self.carte)

        self.way = False
        self.neutra = False

        self.done = False

        # file d'actions à jouer
        self.actions = []

    def execute_action(self, action):

        actions = {
            "hr.move()": self.hitman.move,
            "hr.turn_clockwise()": self.hitman.turn_clockwise,
            "hr.turn_anti_clockwise()": self.hitman.turn_anti_clockwise,
            "hr.neutralize_guard()": self.hitman.neutralize_guard,
        }

        self.state = actions[action]()

        self.carte = self.matrix_to_dico(
            self.hitman._HitmanReferee__world
        )

    def prepare_actions(self):

        self.set_objectif()

        # if self.goal == "mission_completed":
        #     print("PREPARE TO FINISH")
        #     self.state = self.hitman.end_phase2()

        #     self.done = True

        #     return

        path = self.build_path()

        if path is None:

            self.handle_no_path()

            return

        self.actions = self.build_actions_from_path(path)

    def step(self):

        if self.done:
            return self.get_state()

        # Plus d'actions à jouer ?
        if len(self.actions) == 0:

            self.prepare_actions()

            if len(self.actions) == 0:
                self.done = True
                return self.get_state()

        action = self.actions.pop(0)

        self.execute_action(action)

        return self.get_state()

    def build_path(self):

        position = self.state["position"]

        priority = []

        visited = set()

        heapq.heappush(
            priority,
            (
                self.heuristique(position, self.target),
                position,
                []
            )
        )

        while priority:

            _, current_pos, path = heapq.heappop(priority)

            if current_pos == self.target:

                return [position] + path

            if current_pos in visited:
                continue

            visited.add(current_pos)

            for dx, dy in [
                (0,-1),
                (0,1),
                (-1,0),
                (1,0)
            ]:

                new_pos = (
                    current_pos[0] + dx,
                    current_pos[1] + dy
                )

                if (
                    self.est_position_valide(
                        current_pos,
                        new_pos,
                        self.carte,
                        self.way,
                        self.neutra
                    )
                    and new_pos not in visited
                ):

                    new_path = path + [new_pos]

                    heapq.heappush(
                        priority,
                        (
                            self.heuristique(
                                new_pos,
                                self.target
                            ) + len(new_path),
                            new_pos,
                            new_path
                        )
                    )

        return None
    
    def build_actions_from_path(self, path):

        actions = []

        for i in range(len(path)-1):

            mouvements = self.mouvement(
                path[i],
                path[i+1],
                path[:i+1],
                self.state,
                self.carte
            )

            for m in mouvements:
                actions.append(m)

        return actions

    def handle_no_path(self):

        if self.goal == "weapon" and self.way == False:
            self.target = self.trouver_suit(self.carte)
            self.goal = "suit"

        elif self.goal == "suit" and self.way == False:
            self.target = self.trouver_corde(self.carte)
            self.goal = "weapon"
            self.way = True

        elif self.goal == "weapon" and self.way == True:
            self.target = self.trouver_suit(self.carte)
            self.goal = "suit"
            self.way = True

        elif self.goal == "suit" and self.way == True:
            self.target = self.trouver_corde(self.carte)
            self.goal = "weapon"
            self.way = True
            self.neutra = True

        else :
            self.target = self.trouver_suit(self.carte)
            self.goal = "suit"
            self.way = True
            self.neutra = True

    def phase2(self, way: bool = False, neutra: bool = False) -> Dict:

        carte = self.matrix_to_dico(self.hitman._HitmanReferee__world) # map
        target = self.trouver_corde(carte) # corde
        goal = 'weapon' # initial state of goal
        etat = self.state

        deplacements = [(0, -1), (0, 1), (-1, 0), (1, 0)]# Déplacement possible à partir d'une position donnée
        position = etat["position"]# Position de départ
        print("objectif :", target)

        if way == True and etat['has_suit'] == False : # si Hitman a l'arme mais pas le costume
            target = self.trouver_suit(carte)
            goal = "suit"
            way = False
            print("pass")

        if position == target: # si hitman est sur la cible, le programme s'arrête
            return etat
        
        priority = []# liste des noeuds à visiter en priorité
        visited = set()# liste des noeuds visités
        heapq.heappush(priority, (self.heuristique(position, target), position, []))
        while priority:
            priority.sort() # Tri de la liste selon les priorités
            _, current_pos, path = heapq.heappop(priority)# Récupération du nœud avec la plus basse priorité
            # TARGET
            if current_pos == target:# Hitman a atteint la cible
                path = [etat["position"]] + path
                for i in range(len(path)-1):
                    for fonction in self.mouvement(path[i], path[i+1], path[:i+1], etat, carte) :
                        print("STATUT :", etat["status"])
                        print("PARCOURS :", path)
                        print("ACTION JOUE :", fonction)
                        print("OBJECTIF :", goal)
                        actions = {
                            "hr.move()": self.hitman.move,
                            "hr.turn_clockwise()": self.hitman.turn_clockwise,
                            "hr.turn_anti_clockwise()": self.hitman.turn_anti_clockwise,
                            "hr.neutralize_guard()": self.hitman.neutralize_guard,
                        }
                        etat = actions[fonction]()
                        carte = self.matrix_to_dico(self.hitman._HitmanReferee__world)
                        display_map_phase2(carte, etat)
                        # time.sleep(0.5) #TODO timer = 2s
                        
                if goal == 'weapon' :
                    etat = self.hitman.take_weapon()
                    if etat['has_weapon'] == True and etat['has_suit'] == False :
                        print("cond arme")
                        etat = self.boucle(self.trouver_cible(carte), etat, 'target', carte, way = False)
                    elif etat['has_weapon'] == True and etat['has_suit'] == True :
                        etat = self.boucle(self.trouver_cible(carte), etat, 'target', carte, way = True)

                elif goal == 'target' :
                    etat = self.hitman.kill_target()
                    if etat['is_target_down'] == True and etat['has_suit'] == False :
                        print("cond cible")
                        etat = self.boucle((0,0), etat, 'finish_the_mission', carte, way = False)
                    elif etat['is_target_down'] == True and etat['has_suit'] == True :
                        etat = self.boucle((0,0), etat, 'finish_the_mission', carte, way = True)

                elif goal == 'suit' :
                    etat = self.hitman.take_suit()
                    etat = self.hitman.put_on_suit()
                    if etat['has_weapon'] == False and etat['has_suit'] == False :
                        print("cond costume")
                        etat = self.boucle(self.trouver_corde(carte), etat, 'weapon', carte, way = False)
                    elif etat['has_weapon'] == False and etat['has_suit'] == True :
                        etat = self.boucle(self.trouver_corde(carte), etat, 'weapon', carte, way = True)
                    elif etat['has_weapon'] == True and etat['has_suit'] == True : # on a déjà l'arme et il y a un obstacle sur le chemin de la cible
                        etat = self.boucle(self.trouver_cible(carte), etat, 'target', carte, way = True)
                        
                elif goal == 'finish_the_mission' :
                    etat = self.hitman.end_phase2()
                    pprint(etat)
                return etat
            # PASS
            if current_pos in visited:
                continue
            # THEN
            visited.add(current_pos) # ajout de la position actuelle au set des noeuds visités
            for dx, dy in deplacements:# Génère les voisins possibles
                new_x, new_y = current_pos[0] + dx, current_pos[1] + dy #création des 4 déplacements possibles suivant le x et y de hitman
                new_pos = (new_x, new_y) # tuple de l'un des 4 déplacements possibles
                if self.est_position_valide(current_pos, new_pos, carte, way, neutra) and new_pos not in visited: # on vérifie que le déplacement est valide (pas de mur, de garde, etc) et qu'il n'appartient pas déjà à visited
                    new_path = path + [new_pos]
                    heapq.heappush(
                        priority,
                        (self.heuristique(new_pos, target) + len(new_path), new_pos, new_path)
                    )

        if target not in path :
            if goal == "corde" :
                print("pas de chemin vers la corde, on essaye avec le suit")
                target = self.trouver_suit(carte)
                etat = self.boucle(target, etat, "suit", carte)

            elif goal == "suit" :
                print("pas de chemin vers le suit, on essaye avec la corde en passant devant les gardes")
                target = self.trouver_corde(carte)
                etat = self.boucle(target, etat, "weapon", carte, way = True)

            elif goal == "weapon" and way == True :
                print("pas de chemin vers la corde en passant devant les gardes, on essaye avec le suit en passant devant les gardes")
                target = self.trouver_suit(carte)
                etat = self.boucle(target, etat, "suit", carte, way = True)

            elif goal == "suit" and way == True :
                print("pas de chemin vers le suit en passant devant les gardes, on essaye avec la corde en neutralisant les gardes")
                target = self.trouver_corde(carte)
                etat = self.boucle(target, etat, "weapon", carte, way = True, neutra = True)

            else :
                print("pas de chemin vers la corde en neutralisant les gardes, on essaye avec le suit en neutralisant les gardes")
                target = self.trouver_suit(carte)
                etat = self.boucle(target, etat, "suit", carte, way = True, neutra = True)
        return etat
