import subprocess
from typing import List, Tuple, Dict
from itertools import combinations
import numpy as np
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

def remove(string: str) -> Dict:
    for i in range(1, 18):
        placeholder = f": {i}>"
        replacement = ""
        string = string.replace(placeholder, replacement)
    string = string.replace("<", "")
    dico = eval(string)
    return dico

def display_map_phase1(map: Dict, position: str, iteration: str, score: str, nb_co:str, state: Dict) -> None:
    symbols = {
        HC.EMPTY: " ",
        HC.SUIT: "S",
        HC.GUARD_N: "G",
        HC.GUARD_W: "G",
        HC.GUARD_E: "G",
        HC.GUARD_S: "G",
        HC.WALL: "#",
        HC.TARGET: "T",
        HC.CIVIL_N: "C",
        HC.CIVIL_W: "C",
        HC.CIVIL_E: "C",
        HC.CIVIL_S: "C",
        HC.PIANO_WIRE: "P",
        #"HITMAN": "H",
        HC.N: "^",
        HC.S: "v",
        HC.E: ">", 
        HC.W: "<"
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
                if element == HC.PIANO_WIRE:
                    symbol = symbols[HC.PIANO_WIRE]
                elif element == HC.SUIT:
                    symbol = symbols[HC.SUIT]
                elif element == HC.TARGET:
                    symbol = symbols[HC.TARGET]
                else:
                    symbol = symbols.get(element, "?")
            print(" {0:^{1}} |".format(symbol, cell_width), end="")
        if y == max_y :
            print("\t", position) # display current position
        elif y == max_y - 1 :
            print("\t", iteration) # display current iteration
        elif y == max_y - 2 :
            print("\t", score) # display current score
        elif y == max_y - 3 :
            print("\t", nb_co) # display current number of known cases
        else :
            print()
        print("+-----" * (max_x + 1) + "+")


def display_map_phase2(map: Dict, state: Dict) -> None:
    symbols = {
        HC.EMPTY: " ",
        HC.SUIT: "S",
        HC.GUARD_N: "G",
        HC.GUARD_W: "G",
        HC.GUARD_E: "G",
        HC.GUARD_S: "G",
        HC.WALL: "#",
        HC.TARGET: "T",
        HC.CIVIL_N: "C",
        HC.CIVIL_W: "C",
        HC.CIVIL_E: "C",
        HC.CIVIL_S: "C",
        HC.PIANO_WIRE: "P",
        #"HITMAN": "H",
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

#-----------------------------FONCTIONS DE FICHIER--------------------------------------------
def clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str:
    dimacs = str()
    nb_clauses = 0
    for clause in clauses : 
        for el in clause : 
            dimacs += str(el) + " "
        dimacs += "0\n"
        nb_clauses += 1
    result = 'p cnf ' + str(nb_vars) +' '+ str(nb_clauses) + '\n' + dimacs
    return result

def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)

def clean_file():
    os.remove("cnf_directory/known_case.cnf")

def exec_gophersat(filename: str, cmd: str = "./gophersat.exe", encoding: str = "utf8") -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()
    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]
#-----------------------------FONCTIONS DE FICHIER--------------------------------------------



#-----------------------------FONCTIONS SUR LES CONTRAINTES--------------------------------------------
def at_least_one(variables: List[PropositionnalVariable]) -> Clause : 
    return variables[:]

def at_most_number(variables,number):
    clauses = []
    for combination in combinations(variables, number+1):
        clause = [-num for num in combination]
        clauses.append(clause)
    return clauses

def at_least_number(variables, number):
    clauses = []
    n = len(variables)
    for combination in combinations(variables, n - number + 1):
        clauses.append(list(combination))

    return clauses

def exactly_number(variables, number):
    clauses = []

    clauses.extend(at_least_number(variables, number))
    clauses.extend(at_most_number(variables, number))

    return clauses
#-----------------------------FONCTIONS SUR LES CONTRAINTES--------------------------------------------

class SATEngine:
    def __init__(self):
        self.solver = Glucose3()
        self.nb_vars = 0

    def add_clause(self, clause):
        self.solver.add_clause(clause)

        if not self.solver.solve():
            print("CLAUSE FATALE :", clause)
            raise Exception("SAT devenu UNSAT")

    def solve(self, assumptions=None):
        return self.solver.solve(assumptions=assumptions)

    def model(self):
        return self.solver.get_model()
    
#-----------------------------Class Map--------------------------------------------
class Map():
    def __init__(self, m: int, n: int, nb_gardes: int, nb_civils: int) -> None:
        
        self.nb_lignes = m
        self.nb_colonnes = n
        self.nb_cases_a_trouver = int(n*m*0.95)

        self.clauses_safe = []
        self.clauses_personnes = []
        self.clauses_personnes_probable = []
        self.clauses_connues = []
        self.clauses_passage = []
        self.nb_variables = 16
        self.rien = 0
        self.mur = 1
        self.corde = 2
        self.costume = 3
        self.cible = 4

        self.garde_n = 5
        self.garde_s = 6
        self.garde_e = 7
        self.garde_w = 8

        self.civil_n = 9
        self.civil_s = 10
        self.civil_e = 11
        self.civil_w = 12

        self.personne = 13
        self.safe = 14
        self.case_passage = 15

        self.nb_gardes = nb_gardes
        self.nb_civils = nb_civils
        self.nb_var_prop = self.nb_lignes * self.nb_colonnes * self.nb_variables

        self.grille_scores = np.ones((self.nb_lignes,self.nb_colonnes)) * 20

        self.sat = SATEngine()

        self.init_var_Map()
    
    def num_to_obj_HC(self,num: int) -> object :
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
            return HC.GUARD_N
        elif num == 6 : 
            return HC.GUARD_S
        elif num == 7 : 
            return HC.GUARD_E
        elif num == 8 : 
            return HC.GUARD_W
        elif num == 9 : 
            return HC.CIVIL_N
        elif num == 10 : 
            return HC.CIVIL_S
        elif num == 11 : 
            return HC.CIVIL_E
        elif num == 12 : 
            return HC.CIVIL_W
        else:
            return HC.UNKNOWN 

    def add_safe_clause(self, clause: Clause) -> List :
        self.clauses_safe.append(clause)
        return self.clauses_safe
    
    def add_pass_clause(self, clause: Clause) -> List :
        self.clauses_passage.append(clause)
        return self.clauses_passage
    
    def add_person_clause(self, clause: Clause) -> List :
        self.clauses_personnes.append(clause)
        return self.clauses_personnes
    
    def add_person_prob_clause(self, clause: Clause) -> List :
        self.clauses_personnes_probable.append(clause)
        return self.clauses_personnes_probable
    
    def add_known_clause(self, clause: Clause) -> List :
        self.clauses_connues.append(clause)
        return self.clauses_connues

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
        clauses = []
        for i in range(self.nb_lignes) :
            for j in range(self.nb_colonnes) :
                liste_variable = []
                liste_variable.append(self.cell_to_variable(i, j, self.personne))
        clauses.append(at_most_number(liste_variable, self.nb_civils + self.nb_gardes))
        for c1 in clauses : 
            for c2 in c1 :
                self.clauses_personnes.append(c2)

        clauses = []

        for i in range(self.nb_lignes) :
            for j in range(self.nb_colonnes) :
                liste_variable = []
                for h in range(self.nb_variables) :
                    liste_variable.append(self.cell_to_variable(i, j, h))
                clauses.append(exactly_number(liste_variable, 1))
        
        for variable in range(2, 4+1):
            liste_variable = []
            for i in range(self.nb_lignes) :
                for j in range(self.nb_colonnes) :
                    liste_variable.append(self.cell_to_variable(i, j, variable))
            clauses.append(exactly_number(liste_variable, 1))

        for c1 in clauses : 
            for c2 in c1 :
                self.clauses_connues.append(c2)

    def var_mur(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.mur)]
    
    def var_not_mur(self, pos: Position) -> List :
        return [-self.cell_to_variable(pos[1], pos[0], self.mur)]
    
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
    
    def var_guard_n(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.garde_n)]
    
    def var_guard_s(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1] ,pos[0], self.garde_s)]
    
    def var_guard_e(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.garde_e)]
    
    def var_guard_w(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.garde_w)]
    
    def var_civil_n(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.civil_n)]
    
    def var_civil_s(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.civil_s)]
    
    def var_civil_e(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.civil_e)]
    
    def var_civil_w(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.civil_w)]
    
    def var_pass_case(self, pos: Position) -> List :
        return [self.cell_to_variable(pos[1], pos[0], self.case_passage)]
    
    def var_not_pass_case(self, pos: Position) -> List :
        return [-self.cell_to_variable(pos[1], pos[0], self.case_passage)]
    
    def known_case(self,ligne: int, colonne: int) -> bool :
        for clause in self.clauses_connues :
            if len(clause) == 1 and self.variable_to_cell(clause[0])[0] == ligne and self.variable_to_cell(clause[0])[1] == colonne : 
                return True
        return False

    def case_mur(self, pos: Position) -> bool :
        v = self.var_mur(pos)[0]

        result_m = self.sat.solve(assumptions = [v])
        result_non_m = self.sat.solve(assumptions = [-v])

        if result_m and not result_non_m :
            return True
        return False
            
    def case_personne(self, ligne: int, colonne: int) -> bool :
        v = self.var_personne((colonne, ligne))[0]

        result_p = self.sat.solve(assumptions = [v])
        result_non_p = self.sat.solve(assumptions = [-v])

        return result_p and not result_non_p
    
    def case_maybe_personne(self, ligne: int, colonne: int) -> bool :
        v = self.var_personne((colonne, ligne))[0]
        return self.sat.solve(assumptions = [v])

    def case_not_safe(self, ligne: int, colonne: int) -> bool :
        v = self.var_safe((colonne, ligne))[0]

        result_p = self.sat.solve(assumptions = [v])
        result_non_p = self.sat.solve(assumptions = [-v])

        return (not result_p) and result_non_p

    def case_go(self, ligne: int, colonne: int) -> bool :
        v = self.var_pass_case((colonne, ligne))[0]

        result_p = self.sat.solve(assumptions = [v])
        result_non_p = self.sat.solve(assumptions = [-v])

        return result_p and not result_non_p

    def known_Map(self) -> bool :
        clauses = self.clauses_connues.copy()
        for i in range(self.nb_lignes) :
            for j in range(self.nb_colonnes) :
                clauses.append(self.var_not_safe((j, i)))
                clauses.append(self.var_not_personne((j, i)))
                clauses.append(self.var_not_pass_case((j, i)))

        solver = Glucose3()

        for clause in clauses :
            solver.add_clause(clause)

        if not solver.solve() :
            return {}
        
        modele = solver.get_model()
        
        dictionnaire = {}
        for it in range(len(modele)) :
            if modele[it] > 0 : 
                ligne, colonne, num_objet = self.variable_to_cell(modele[it])
                objet = self.num_to_obj_HC(num_objet)
                dictionnaire[(colonne, ligne)] = objet
        return dictionnaire

    def get_grille_score(self, pos: Position) -> int :
        colonne_x, ligne_y = pos
        return self.grille_scores[ligne_y][colonne_x]

    def set_grille_score(self, pos: Position, val: int) -> None :
        colonne_x, ligne_y = pos
        self.grille_scores[ligne_y][colonne_x] = val

    def update_grille_score_with_known_map(self) :
        current_map = self.known_Map()
        for pos, val in current_map.items() :
            if val == HC.GUARD_E or val == HC.GUARD_N or val == HC.GUARD_S or val == HC.GUARD_W :
                colonne_x, ligne_y = pos
                self.grille_scores[ligne_y][colonne_x] = -15
            if val == HC.CIVIL_E or val == HC.CIVIL_N or val == HC.CIVIL_S or val == HC.CIVIL_W :
                colonne_x, ligne_y = pos
                self.grille_scores[ligne_y][colonne_x] = -15

    def update_grille_score_with_frontier(self, pos: Position) :
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

    def nb_known_case(self) -> int :
        elements = []
        nb_cases = 0
        est_deja  = False
        for el in self.clauses_connues : 
            if len(el) == 1 :
                if el[0] > 0 : 
                    est_deja  = False
                    for nb in elements :
                        if nb == el[0] :
                            est_deja = True
                    if est_deja == False : 
                        elements.append(el[0])
                        nb_cases += 1
        return nb_cases
    
    def hear_case(self, pos: Tuple[int, int]) -> List :
        x, y = pos
        coord_cases = []
        upper_left_x = x - 2
        upper_left_y = y + 2
        
        for temp_y in range(upper_left_y,upper_left_y - 5, -1) :

            for temp_x in range(upper_left_x,upper_left_x + 5) :

                if temp_y >= 0 and temp_y < self.nb_lignes and temp_x >= 0 and temp_x < self.nb_colonnes :
                    if temp_y != y or temp_x != x :
                        coord_cases.append([temp_x, temp_y])
        return coord_cases

    def move_case(self, ligne: int, colonne: int) -> List :
        coord_cases = []
        ligne_c = ligne + 1 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        
        ligne_c = ligne - 1 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        
        ligne_c = ligne 
        colonne_c = colonne + 1
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        
        ligne_c = ligne 
        colonne_c = colonne - 1
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        
        return coord_cases

    def case_safe(self, ligne: int, colonne: int) -> List :
        coord_cases = []
        ligne_c = ligne + 1 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        ligne_c = ligne + 2 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        ligne_c = ligne + 3 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        ligne_c = ligne - 1 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        ligne_c = ligne - 2 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        ligne_c = ligne - 3 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        ligne_c = ligne  
        colonne_c = colonne + 1
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        ligne_c = ligne  
        colonne_c = colonne + 2
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        
        ligne_c = ligne  
        colonne_c = colonne + 3
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        ligne_c = ligne  
        colonne_c = colonne - 1
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        ligne_c = ligne  
        colonne_c = colonne - 2
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        
        ligne_c = ligne  
        colonne_c = colonne - 3
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c, colonne_c])
        return coord_cases
#-----------------------------Class Map--------------------------------------------


    
    