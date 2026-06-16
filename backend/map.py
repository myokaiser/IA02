from typing import List, Tuple, Dict
from itertools import combinations
import numpy as np
import pickle
import os
from hitman.hitman import HC 
from pysat.solvers import Glucose3

Grid = List[List[int]] 
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]
Position = List[int]
Orientation = str #N,E,S,O

def affiche_star_1() :
    print(r"___    ___     ___     _________     ___        __                    ___    __")
    print(r"\ /    \ /     \ /    |/  | |  \|    \  \      / /         /\         \  \   \/")
    print(r"| |    | |     | |        | |        |\  \    // |        /. \        ||\ \  ||")
    print(r"| |____| |     | |        | |        ||\  \  //| |       // \ \       || \ \ ||")
    print(r"| |    | |     | |        | |        || \  \// | |      //___\ \      ||  \ \||")
    print(r"| |    | |     | |        | |        ||  \  /  | |     //     \ \     ||   \  |")
    print(r"/_\    /_\     /_\        /_\       /_\   \/   /_\    /_\     /__\   /__\   \_|")
    print(r"-------------------------------------------------------------------------------")
    print(r"                    ___                      _          __                     ")
    print(r"                   | _ \ ___  _  _  _ _   __| |        /  |                    ")
    print(r"                   |   // _ \| || || ' \ / _` |         | |                    ")
    print(r"                   |_|_\\___/ \_._||_||_|\__/_|         |_|                    ")
    print(r"-------------------------------------------------------------------------------")

def affiche_star_2() :
    print(r"-------------------------------------------------------------------------------")
    print(r"                    ___                      _          ___                    ")
    print(r"                   | _ \ ___  _  _  _ _   __| |        |_  )                   ")
    print(r"                   |   // _ \| || || ' \ / _` |         / /                    ")
    print(r"                   |_|_\\___/ \_._||_||_|\__/_|        /___|                   ")
    print(r"-------------------------------------------------------------------------------")
#-----------------------------AFFICHAGE MAP------------------------------------------------

def display_map_phase1(map: Dict, state: Dict) -> None:
    symbols = {
        HC.EMPTY: " ",
        HC.SUIT: "S",
        HC.WALL: "#",
        HC.TARGET: "T",
        HC.PIANO_WIRE: "P",
        HC.N: "^",
        HC.S: "v",
        HC.E: ">", 
        HC.W: "<",
        HC.PERSON: "*",
        HC.GUARD: "G",
        HC.CIVIL: "C",
        HC.NORTH: "N",
        HC.SOUTH: "S",
        HC.EAST: "E", 
        HC.WEST: "W",
    }

    cell_width = 3
    max_x = max(x for x, _ in map.keys())
    max_y = max(y for _, y in map.keys())
    print("+-----" * (max_x + 1) + "+")
    for y in range(max_y, -1, -1):
        print("|", end="")
        for x in range(max_x + 1):
            if (x, y) == state["position"]:
                symbol = symbols[state["orientation"]]
            else:
                element = map.get((x, y), None)
                if len(element) == 1 :
                    element = element[0]
                    if element == HC.PIANO_WIRE:
                        symbol = symbols[HC.PIANO_WIRE]
                    elif element == HC.SUIT:
                        symbol = symbols[HC.SUIT]
                    elif element == HC.TARGET:
                        symbol = symbols[HC.TARGET]
                    elif element == HC.PERSON:
                        symbol = symbols[HC.PERSON]
                    elif element == HC.GUARD:
                        symbol = symbols[HC.GUARD]
                    elif element == HC.CIVIL:
                        symbol = symbols[HC.CIVIL]
                    else:
                        symbol = symbols.get(element, "?")
                else :
                    if HC.CIVIL in element :
                        symbol = symbols[HC.CIVIL]
                        if len(element) == 3 :
                            symbol = symbol + "_" + symbols[element[2]] # orientation
                    elif HC.GUARD in element :
                        symbol = symbols[HC.GUARD]
                        if len(element) == 3 :
                            symbol = symbol + "_" + symbols[element[2]] # orientation
            print(" {0:^{1}} |".format(symbol, cell_width), end="")
        print()
        print("+-----" * (max_x + 1) + "+")


def display_map_phase2(map: Dict, state: Dict) -> None:
    symbols = {
        HC.EMPTY: " ",
        HC.SUIT: "S",
        HC.GUARD_N: "G_N",
        HC.GUARD_W: "G_W",
        HC.GUARD_E: "G_E",
        HC.GUARD_S: "G_S",
        HC.WALL: "#",
        HC.TARGET: "T",
        HC.CIVIL_N: "C_N",
        HC.CIVIL_W: "C_W",
        HC.CIVIL_E: "C_E",
        HC.CIVIL_S: "C_S",
        HC.PIANO_WIRE: "P",
        HC.N: "^",
        HC.S: "v",
        HC.E: ">", 
        HC.W: "<"
    }

    cell_width = 3
    max_x = max(x for x, y in map.keys())
    max_y = max(y for x, y in map.keys())
    print("+-----" * (max_x + 1) + "+")
    for y in range(max_y, -1, -1):
        print("|", end="")
        for x in range(max_x + 1):
            element = map.get((x, y), None)
            if (x, y) == state["position"]:
                symbol = symbols[state["orientation"]]
            else:
                if element == HC.PIANO_WIRE and state["has_weapon"]:
                    symbol = symbols[HC.EMPTY]
                elif element == HC.SUIT and state["has_suit"]:
                    symbol = symbols[HC.EMPTY]
                elif element == HC.TARGET and state["is_target_down"]:
                    symbol = symbols[HC.EMPTY]
                else:
                    symbol = symbols.get(element, "?")
            print(" {0:^{1}} |".format(symbol, cell_width), end="")
        print()
        print("+-----" * (max_x + 1) + "+")

#-----------------------------AFFICHAGE MAP------------------------------------------------

#-----------------------------FONCTIONS SUR LES CONTRAINTES--------------------------------------------

def at_least_one(variables: List[PropositionnalVariable]) -> Clause : 
    return variables[:]

def at_most_number(variables: List[PropositionnalVariable], number: int) -> Clause :
    clauses = []
    for combination in combinations(variables, number+1):
        clause = [-num for num in combination]
        clauses.append(clause)

    return clauses

def at_least_number(variables: List[PropositionnalVariable], number: int) -> Clause :
    clauses = []
    n = len(variables)
    for combination in combinations(variables, n - number + 1):
        clauses.append(list(combination))

    return clauses

def exactly_number(variables: List[PropositionnalVariable], number: int) -> Clause :
    clauses = []
    clauses.extend(at_least_number(variables, number))
    clauses.extend(at_most_number(variables, number))

    return clauses

#-----------------------------FONCTIONS SUR LES CONTRAINTES--------------------------------------------

class SATEngine:
    def __init__(self) :
        self.solver = Glucose3()
        self.nb_vars = 0

    def add_clause(self, clause) :
        self.solver.add_clause(clause)

    def check(self) :
        return self.solver.solve()

    def solve(self, assumptions=None) :
        if assumptions is None:
            assumptions = []
        return self.solver.solve(assumptions=assumptions)

    def model(self) :
        return self.solver.get_model()
    
#-----------------------------Class Map--------------------------------------------
class Map():
    def __init__(self, m: int, n: int, nb_gardes: int, nb_civils: int) -> None :
        
        self.nb_lignes = m
        self.nb_colonnes = n
        self.nb_cases_a_trouver = int(n*m*0.95)

        self.clauses_connues = []
        self.nb_variables = 13
        self.rien = 0
        self.mur = 1
        self.corde = 2
        self.costume = 3
        self.cible = 4

        self.personne = 5

        self.guard = 6
        self.civil = 7

        self.north = 8
        self.south = 9
        self.east  = 10
        self.west  = 11

        self.safe = 12

        self.nb_gardes = nb_gardes
        self.nb_civils = nb_civils
        self.nb_var_prop = self.nb_lignes * self.nb_colonnes * self.nb_variables

        self.grille_scores = np.ones((self.nb_lignes,self.nb_colonnes)) * 20

        self.sat = SATEngine()

        self.init_var_Map()

    def num_to_obj_HC(self, num: int) -> object :
        if num == 0 : 
            return HC.EMPTY
        elif num == 1 : 
            return HC.WALL
        elif num == 2 : 
            return HC.PIANO_WIRE
        elif num == 3 : 
            return HC.SUIT
        elif num == 4 : 
            return HC.TARGET
        
        elif num == 5 : 
            return HC.PERSON
        
        elif num == 6 : 
            return HC.GUARD
        elif num == 7 : 
            return HC.CIVIL
        
        elif num == 8 : 
            return HC.NORTH
        elif num == 9 : 
            return HC.SOUTH
        elif num == 10 : 
            return HC.EAST
        elif num == 11 : 
            return HC.WEST
        
        else:
            return HC.UNKNOWN 

    def reconstruct_map_for_state(self, dico: Dict) -> Dict :
        reonstruction_person = {
            (HC.PERSON, HC.CIVIL, HC.NORTH) : HC.CIVIL_N,
            (HC.PERSON, HC.CIVIL, HC.SOUTH) : HC.CIVIL_E,
            (HC.PERSON, HC.CIVIL, HC.EAST) : HC.CIVIL_S,
            (HC.PERSON, HC.CIVIL, HC.WEST) : HC.CIVIL_W,
            
            (HC.PERSON, HC.GUARD, HC.NORTH) : HC.GUARD_N,
            (HC.PERSON, HC.GUARD, HC.SOUTH) : HC.GUARD_E,
            (HC.PERSON, HC.GUARD, HC.EAST) : HC.GUARD_S,
            (HC.PERSON, HC.GUARD, HC.WEST) : HC.GUARD_W,
        }

        for pos in dico.keys() :
            element = dico[pos]
            if len(element) == 1 :
                dico[pos] = element[0]
            elif len(element) == 3 :
                nature, role, orientation = element
                dico[pos] = reonstruction_person[(nature, role, orientation)]
                    
        return dico

    def cell_to_variable(self, y: int, x: int, val: int) -> PropositionnalVariable :
        return (y + (self.nb_colonnes - 1) * y + x) * self.nb_variables + (val + 1)

    def variable_to_cell(self, var: PropositionnalVariable) -> Tuple[int, int, int] :
        v = (var - 1) % self.nb_variables
        var -= v
        x = int(var / self.nb_variables)
        i = x // self.nb_colonnes
        j = x - (i + (self.nb_colonnes - 1) * i)
        return [i, j, v]
    
    def init_var_Map(self) -> None :

        file_path = "base_sat.pkl"
        clauses = []

        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                clauses = pickle.load(f)

            for clause in clauses:
                self.sat.add_clause(clause)
        else :
            # =====================================================
            # EXACTEMENT UNE NATURE PAR CASE
            # =====================================================
            nature_variables = [
                self.rien,
                self.mur,
                self.corde,
                self.costume,
                self.cible,
                self.personne
            ]

            for y in range(self.nb_lignes):
                for x in range(self.nb_colonnes):

                    vars_case = [
                        self.cell_to_variable(y, x, v)
                        for v in nature_variables
                    ]
                    clauses.extend(exactly_number(vars_case, 1))

            # =====================================================
            # OBJETS UNIQUES SUR LA CARTE
            # =====================================================
            for variable in [
                self.corde,
                self.costume,
                self.cible
            ]:
                vars_objet = []
                for y in range(self.nb_lignes):
                    for x in range(self.nb_colonnes):

                        vars_objet.append(
                            self.cell_to_variable(y, x, variable)
                        )

                clauses.extend(
                    exactly_number(vars_objet, 1)
                )

            # =====================================================
            # PERSONNE <-> GUARD/CIVIL
            # =====================================================
            for y in range(self.nb_lignes):
                for x in range(self.nb_colonnes):

                    personne = self.cell_to_variable(y, x, self.personne)
                    guard = self.cell_to_variable( y, x, self.guard)
                    civil = self.cell_to_variable(y, x, self.civil)

                    # guard -> personne
                    clauses.append([-guard, personne])

                    # civil -> personne
                    clauses.append([-civil, personne])

                    # personne -> guard ou civil
                    clauses.append([-personne, guard, civil])

                    # pas les deux
                    clauses.append([-guard, -civil])

            # =====================================================
            # ORIENTATIONS
            # =====================================================
            for y in range(self.nb_lignes):
                for x in range(self.nb_colonnes):

                    personne = self.cell_to_variable(y, x, self.personne)
                    guard = self.cell_to_variable(y, x, self.guard)
                    civil = self.cell_to_variable(y, x, self.civil)

                    north = self.cell_to_variable(y, x, self.north)
                    south = self.cell_to_variable(y, x, self.south)
                    east = self.cell_to_variable(y, x, self.east)
                    west = self.cell_to_variable(y, x, self.west)

                    orientation_vars = [north, south, east, west]

                    # guard -> au moins une orientation
                    clauses.append([-guard, north, south, east, west])

                    # civil -> au moins une orientation
                    clauses.append([-civil, north, south, east, west])

                    # au plus une orientation
                    clauses.extend(
                        at_most_number(orientation_vars, 1)
                    )

                    # orientation -> personne
                    for orient in orientation_vars:
                        clauses.append([-orient, personne])

                    # orientation -> guard ou civil
                    for orient in orientation_vars:
                        clauses.append([-orient, guard, civil])

            # =====================================================
            # NOMBRE TOTAL DE PERSONNES
            # =====================================================
            personne_variables = []

            for y in range(self.nb_lignes):
                for x in range(self.nb_colonnes):

                    personne_variables.append(
                        self.cell_to_variable(y, x, self.personne)
                    )

            clauses.extend(
                exactly_number(personne_variables, self.nb_gardes + self.nb_civils)
            )

            # =====================================================
            # NOMBRE TOTAL DE GUARDS
            # =====================================================
            guard_variables = []

            for y in range(self.nb_lignes):
                for x in range(self.nb_colonnes):

                    guard_variables.append(
                        self.cell_to_variable(y, x, self.guard)
                    )

            clauses.extend(
                exactly_number(guard_variables, self.nb_gardes)
            )

            # =====================================================
            # NOMBRE TOTAL DE CIVILS
            # =====================================================
            civil_variables = []

            for y in range(self.nb_lignes):
                for x in range(self.nb_colonnes):

                    civil_variables.append(
                        self.cell_to_variable(y, x, self.civil)
                    )

            clauses.extend(
                exactly_number(civil_variables, self.nb_civils)
            )

            # =====================================================
            # ENREGISTREMENT
            # =====================================================
            for clause in clauses:
                self.sat.add_clause(clause)

            if not self.sat.check():
                raise Exception("Init UNSAT")

            with open(file_path, "wb") as f:
                pickle.dump(clauses, f)

    def is_true(self, var: PropositionnalVariable) -> bool :

        return (
            self.sat.solve(assumptions = [var])
            and
            not self.sat.solve(assumptions = [-var])
        )

    def var_mur(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.mur)]

    def var_corde(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.corde)]

    def var_costume(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.costume)]

    def var_rien(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.rien)]

    def var_cible(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.cible)]

    def var_safe(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.safe)]

    def var_not_safe(self, pos: Position) -> List :
        return [-self.cell_to_variable(pos[1], pos[0], self.safe)]

    def var_personne(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.personne)]

    def var_not_personne(self, pos: Position) -> List :
        return [-self.cell_to_variable(pos[1], pos[0], self.personne)]

    def var_guard(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.guard)]

    def var_not_guard(self, pos: Position) -> List :
        return [-self.cell_to_variable(pos[1], pos[0], self.guard)]

    def var_civil(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.civil)]

    def var_not_civil(self, pos: Position) -> List :
        return [-self.cell_to_variable(pos[1], pos[0], self.civil)]

    def var_north(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.north)]

    def var_south(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.south)]

    def var_east(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.east)]
    
    def var_west(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.west)]

    def case_certaine(self, pos: Position) -> bool :

        x, y = pos

        natures = [
            self.rien,
            self.mur,
            self.corde,
            self.costume,
            self.cible,
            self.personne
        ]

        for nature in natures:

            v = self.cell_to_variable(y, x, nature)

            if self.is_true(v):
                return True

        return False

    def nb_cases_certaines(self, phase = 1) -> List :

        total = 0
        which = []

        for y in range(self.nb_lignes) :
            for x in range(self.nb_colonnes) :

                if phase == 1 :
                    if self.case_certaine((x, y)) :
                        total += 1
                        which.append(f"{x},{y}")
                else :
                    total += 1
                    which.append(f"{x},{y}")
        return [total, which]

    def early_stopping(self) -> bool :
        nb, _ = self.nb_cases_certaines()

        pourcentage = nb / (self.nb_lignes * self.nb_colonnes)

        if pourcentage >= 0.95 :
            print("Carte suffisamment reconstruite")
            return True
        
        return False

    def case_mur(self, pos: Position) -> bool :
        v = self.var_mur(pos)[0]

        result_m = self.sat.solve(assumptions = [v])
        result_non_m = self.sat.solve(assumptions = [-v])

        if result_m and not result_non_m :
            return True
        return False

    def case_personne(self, pos: Position) -> bool :
        colonne_x, ligne_y = pos
        v = self.var_personne((colonne_x, ligne_y))[0]
        return self.is_true(v)

    def case_maybe_personne(self, pos: Position) -> bool :
        colonne_x, ligne_y = pos
        v = self.var_personne((colonne_x, ligne_y))[0]
        return self.sat.solve(assumptions = [v])

    def case_not_safe(self, pos: Position) -> bool :
        colonne_x, ligne_y = pos
        v = self.var_safe((colonne_x, ligne_y))[0]

        result_p = self.sat.solve(assumptions = [v])
        result_non_p = self.sat.solve(assumptions = [-v])

        return (not result_p) and result_non_p

    def known_Map(self) -> Dict :

        if not self.sat.solve():
            print("KNOWN MAP SAT global = False")
            return {}

        modele = self.sat.model()

        dictionnaire = {}

        for var in modele:

            if var <= 0:
                continue

            ligne, colonne, num_objet = self.variable_to_cell(var)

            objet = self.num_to_obj_HC(num_objet)

            if (colonne, ligne) not in dictionnaire:
                dictionnaire[(colonne, ligne)] = []

            dictionnaire[(colonne, ligne)].append(objet)

        return dictionnaire

    def get_grille_score(self, pos: Position) -> int :
        colonne_x, ligne_y = pos
        return self.grille_scores[ligne_y][colonne_x]

    def set_grille_score(self, pos: Position, val: int) -> None :
        colonne_x, ligne_y = pos
        self.grille_scores[ligne_y][colonne_x] = val

    def update_grille_score_with_known_map(self) -> None :
        current_map = self.known_Map()
        for pos, val in current_map.items() :
            if val == HC.GUARD_E or val == HC.GUARD_N or val == HC.GUARD_S or val == HC.GUARD_W :
                colonne_x, ligne_y = pos
                self.grille_scores[ligne_y][colonne_x] = -15
            if val == HC.CIVIL_E or val == HC.CIVIL_N or val == HC.CIVIL_S or val == HC.CIVIL_W :
                colonne_x, ligne_y = pos
                self.grille_scores[ligne_y][colonne_x] = -15

    def update_grille_score_with_frontier(self, pos: Position) -> None :
        colonne_x, ligne_y = pos

        adjs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for offset in adjs :
            x_off, y_off = offset
            x_adj = colonne_x + x_off
            y_adj = ligne_y + y_off
            if 0 <= x_adj < self.nb_colonnes and 0 <= y_adj < self.nb_lignes :
                print(x_adj, y_adj)
                map_value = self.get_grille_score((x_adj, y_adj))
                if map_value >= 0 :
                    self.grille_scores[y_adj][x_adj] = 5
    
    def hear_case(self, pos: Position) -> List :
        colonne_x, ligne_y = pos
        coord_cases = []
        upper_left_x = colonne_x - 2
        upper_left_y = ligne_y + 2
        
        for temp_y in range(upper_left_y,upper_left_y - 5, -1) :

            for temp_x in range(upper_left_x,upper_left_x + 5) :

                if temp_y >= 0 and temp_y < self.nb_lignes and temp_x >= 0 and temp_x < self.nb_colonnes :
                    if temp_y != ligne_y or temp_x != colonne_x :
                        coord_cases.append([temp_x, temp_y])
        return coord_cases
#-----------------------------Class Map--------------------------------------------