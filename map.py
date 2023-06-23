import subprocess
from typing import List, Tuple, Dict
from itertools import combinations
import numpy as np
import os
from hitman.hitman import HC 

Grid = List[List[int]] 
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]
Position = [int,int]
Orientation = str #N,E,S,O

def affiche_star_1() :
    print("___    ___     ___     _________     ___        __                    ___    __")
    print("\ /    \ /     \ /    |/  | |  \|    \  \      / /         /\         \  \   \/")
    print("| |    | |     | |        | |        |\  \    // |        /. \        ||\ \  ||")
    print("| |____| |     | |        | |        ||\  \  //| |       // \ \       || \ \ ||")
    print("| |    | |     | |        | |        || \  \// | |      //___\ \      ||  \ \||")
    print("| |    | |     | |        | |        ||  \  /  | |     //     \ \     ||   \  |")
    print("/_\    /_\     /_\        /_\       /_\   \/   /_\    /_\     /__\   /__\   \_|")
    print("-------------------------------------------------------------------------------")
    print("                    ___                      _          __                     ")
    print("                   | _ \ ___  _  _  _ _   __| |        /  |                    ")
    print("                   |   // _ \| || || ' \ / _` |         | |                    ")
    print("                   |_|_\\\___/ \_._||_||_|\__/_|         |_|                   ")
    print("-------------------------------------------------------------------------------")

def affiche_star_2() :
    print("-------------------------------------------------------------------------------")
    print("                    ___                      _          ___                    ")
    print("                   | _ \ ___  _  _  _ _   __| |        |_  )                   ")
    print("                   |   // _ \| || || ' \ / _` |         / /                    ")
    print("                   |_|_\\\___/ \_._||_||_|\__/_|        /___|                  ")
    print("-------------------------------------------------------------------------------")
#-----------------------------AFFICHAGE MAP------------------------------------------------

def remove(string: str) -> Dict:
    for i in range(1, 18):
        placeholder = f": {i}>"
        replacement = ""
        string = string.replace(placeholder, replacement)
    string = string.replace("<", "")
    dico = eval(string)
    return dico

def display_map_phase1(map: Dict, state: Dict) -> None:
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
        print()
        print("+-----" * (max_x + 1) + "+")

def display_map(map: Dict, state: Dict) -> None:
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

def exec_gophersat(filename: str, cmd: str = "./gophersat", encoding: str = "utf8") -> Tuple[bool, List[int]]:
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

def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    clauses = []
    clauses.append(at_least_one(variables))
    for clause in combinations(variables,2):
        clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def at_most_number(variables,number):
    clauses = []
    for combination in combinations(variables, number+1):
        clause = [-num for num in combination]
        clauses.append(clause)
    return clauses
#-----------------------------FONCTIONS SUR LES CONTRAINTES--------------------------------------------


#-----------------------------Class Map--------------------------------------------
class Map():
    def __init__(self, m : int, n : int, nb_gardes : int, nb_civils : int) -> None:
        
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

        self.grille_scores = np.zeros((self.nb_lignes,self.nb_colonnes))

        self.init_var_Map()
    
    def num_to_obj_HC(self,num: int):
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
            return HC.EMPTY 

    def add_safe_clause(self, clause : Clause) -> List :
        self.clauses_safe.append(clause)
        return self.clauses_safe
    
    def add_pass_clause(self, clause : Clause) -> List :
        self.clauses_passage.append(clause)
        return self.clauses_passage
    
    def add_person_clause(self, clause : Clause) -> List :
        self.clauses_personnes.append(clause)
        return self.clauses_personnes
    
    def add_person_prob_clause(self, clause : Clause) -> List :
        self.clauses_personnes_probable.append(clause)
        return self.clauses_personnes_probable
    
    def add_known_clause(self, clause : Clause) -> List :
        self.clauses_connues.append(clause)
        return self.clauses_connues

    def cell_to_variable(self, ligne: int, colonne: int, val: int) -> PropositionnalVariable:
        return (ligne+(self.nb_colonnes-1)*ligne+colonne)*self.nb_variables+(val+1)
        

    def variable_to_cell(self, var: PropositionnalVariable) -> Tuple[int, int, int]:
        v = (var-1)%self.nb_variables
        var -= v
        x = int(var/self.nb_variables)
        i = x//self.nb_colonnes
        j = x - (i+(self.nb_colonnes-1)*i)
        return [i,j,v]
    
    def init_var_Map(self) -> None:
        clauses = []
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                liste_variable = []
                liste_variable.append(self.cell_to_variable(i,j,self.personne))
        clauses.append(at_most_number(liste_variable,self.nb_civils+self.nb_gardes))
        for c1 in clauses : 
            for c2 in c1:
                self.clauses_personnes.append(c2)
        
        clauses = []

        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                liste_variable = []
                for h in range(self.nb_variables):
                    liste_variable.append(self.cell_to_variable(i,j,h))
                clauses.append(unique(liste_variable))
        
        for variable in range(2,4+1):
            liste_variable = []
            for i in range(self.nb_lignes):
                for j in range(self.nb_colonnes):
                    liste_variable.append(self.cell_to_variable(i,j,variable))
            clauses.append(unique(liste_variable))

        for c1 in clauses : 
            for c2 in c1:
                self.clauses_connues.append(c2)


    def var_mur(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.mur)]
    
    def var_not_mur(self, pos : Position) -> List:
        return [-self.cell_to_variable(pos[1],pos[0],self.mur)]
    
    def var_corde(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.corde)]
    
    def var_costume(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.costume)]
    
    def var_rien(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.rien)]
    
    def var_cible(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.cible)]
    
    def var_safe(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.safe)]
    
    def var_not_safe(self, pos : Position) -> List:
        return [-self.cell_to_variable(pos[1],pos[0],self.safe)]
    
    def var_personne(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.personne)]
    
    def var_not_personne(self, pos : Position) -> List:
        return [-self.cell_to_variable(pos[1],pos[0],self.personne)]
    
    def var_guard_n(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.garde_n)]
    
    def var_guard_s(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.garde_s)]
    
    def var_guard_e(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.garde_e)]
    
    def var_guard_w(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.garde_w)]
    
    def var_civil_n(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.civil_n)]
    
    def var_civil_s(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.civil_s)]
    
    def var_civil_e(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.civil_e)]
    
    def var_civil_w(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.civil_w)]
    
    def var_pass_case(self, pos : Position) -> List:
        return [self.cell_to_variable(pos[1],pos[0],self.case_passage)]
    
    def var_not_pass_case(self, pos : Position) -> List:
        return [-self.cell_to_variable(pos[1],pos[0],self.case_passage)]

    
    def get_grille_score(self,ligne:int,colonne:int) -> int:
        return self.grille_scores[ligne][colonne]

    def set_grille_score(self,ligne:int,colonne:int,val:int) -> None:
        self.grille_scores[ligne][colonne] += val
    
    
    def known_case(self,ligne:int,colonne:int) -> bool:
        for clause in self.clauses_connues:
            if len(clause) == 1 and self.variable_to_cell(clause[0])[0] == ligne and self.variable_to_cell(clause[0])[1] == colonne : 
                return True
        return False


    def case_mur(self,ligne:int,colonne:int) -> bool:
        clauses = self.clauses_connues.copy()
        clauses.append(self.var_mur((colonne,ligne)))
        dimacs = clauses_to_dimacs(clauses,self.nb_var_prop)
        write_dimacs_file(dimacs,"cnf_directory/known_case.cnf")
        result_m = exec_gophersat("cnf_directory/known_case.cnf")[0]

        clauses = self.clauses_connues.copy()
        clauses.append(self.var_not_mur((colonne,ligne)))
        dimacs = clauses_to_dimacs(clauses,self.nb_var_prop)
        write_dimacs_file(dimacs,"cnf_directory/known_case.cnf")
        result_non_m = exec_gophersat("cnf_directory/known_case.cnf")[0]

        if result_m == True and result_non_m == False : 
            return True
        else : 
            return False
        
    def case_personne(self,ligne:int,colonne:int) -> bool:
        clauses = self.clauses_personnes.copy()
        clauses.append(self.var_personne((colonne,ligne)))
        dimacs = clauses_to_dimacs(clauses,self.nb_var_prop)
        write_dimacs_file(dimacs,"cnf_directory/person_case.cnf")
        result_p = exec_gophersat("cnf_directory/person_case.cnf")[0]

        clauses = self.clauses_personnes.copy()
        clauses.append(self.var_not_personne((colonne,ligne)))
        dimacs = clauses_to_dimacs(clauses,self.nb_var_prop)
        write_dimacs_file(dimacs,"cnf_directory/person_case.cnf")
        result_non_p = exec_gophersat("cnf_directory/person_case.cnf")[0]
        if result_p == True and result_non_p == False : 
            return True
        else : 
            return False
    
    def case_maybe_personne(self,ligne:int,colonne:int) -> bool:
        clauses = self.clauses_personnes.copy() 
        clauses.append(self.var_personne((colonne,ligne)))
        dimacs = clauses_to_dimacs(clauses,self.nb_var_prop)
        write_dimacs_file(dimacs,"cnf_directory/person_case.cnf")
        result_p = exec_gophersat("cnf_directory/person_case.cnf")[0]

        if result_p == True : 
            return True
        else : 
            return False

    def case_not_safe(self,ligne:int,colonne:int) -> bool:
        clauses = self.clauses_safe.copy()
        clauses.append(self.var_safe((colonne,ligne)))
        dimacs = clauses_to_dimacs(clauses,self.nb_var_prop)
        write_dimacs_file(dimacs,"cnf_directory/safe_case.cnf")
        result_p = exec_gophersat("cnf_directory/safe_case.cnf")[0]

        clauses = self.clauses_safe.copy()
        clauses.append(self.var_not_safe((colonne,ligne)))
        dimacs = clauses_to_dimacs(clauses,self.nb_var_prop)
        write_dimacs_file(dimacs,"cnf_directory/safe_case.cnf")
        result_non_p = exec_gophersat("cnf_directory/safe_case.cnf")[0]

        if result_p == False and result_non_p == True : 
            return True
        else : 
            return False

    def case_go(self,ligne:int,colonne:int) -> bool:
        clauses = self.clauses_passage.copy()
        clauses.append(self.var_pass_case((colonne,ligne)))
        dimacs = clauses_to_dimacs(clauses,self.nb_var_prop)
        write_dimacs_file(dimacs,"cnf_directory/pass_case.cnf")
        result_p = exec_gophersat("cnf_directory/pass_case.cnf")[0]

        clauses = self.clauses_passage.copy()
        clauses.append(self.var_not_pass_case((colonne,ligne)))
        dimacs = clauses_to_dimacs(clauses,self.nb_var_prop)
        write_dimacs_file(dimacs,"cnf_directory/pass_case.cnf")
        result_non_p = exec_gophersat("cnf_directory/pass_case.cnf")[0]

        if result_p == True and result_non_p == False : 
            return True
        else : 
            return False


    def known_Map(self) -> bool:
        clauses = self.clauses_connues.copy()
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                clauses.append(self.var_not_safe((j,i)))
                clauses.append(self.var_not_personne((j,i)))
                clauses.append(self.var_not_pass_case((j,i)))
        dimacs = clauses_to_dimacs(clauses,self.nb_var_prop)
        write_dimacs_file(dimacs,"cnf_directory/Map_modele.cnf")
        modele = exec_gophersat("cnf_directory/Map_modele.cnf")[1]
        
        dictionnaire = {}
        for it in range(len(modele)) :
            if modele[it] > 0 : 
                ligne, colonne, num_objet = self.variable_to_cell(modele[it])
                objet = self.num_to_obj_HC(num_objet)
                dictionnaire[(colonne,ligne)] = objet
        return dictionnaire


    def nb_known_case(self) -> int:
        elements = []
        nb_cases = 0
        est_deja  = False
        for el in self.clauses_connues : 
            if len(el) == 1:
                if el[0] > 0 : 
                    est_deja  = False
                    for nb in elements:
                        if nb == el[0]:
                            est_deja = True
                    if est_deja == False : 
                        elements.append(el[0])
                        nb_cases += 1
        return nb_cases
    

    def hear_case(self,ligne_pos:int,colonne_pos:int) -> list:
        coord_cases = []
        colonne_coin_gauche = colonne_pos - 2
        ligne_coin_gauche = ligne_pos - 2
        
        for ligne in range(ligne_coin_gauche,ligne_coin_gauche+5):
            for colonne in range(colonne_coin_gauche,colonne_coin_gauche+5):
                if ligne >= 0 and ligne < self.nb_lignes and colonne >= 0 and colonne < self.nb_colonnes :
                    if ligne != ligne_pos or colonne != colonne_pos :
                        coord_cases.append([ligne,colonne])
        return coord_cases



    def move_case(self,ligne:int,colonne:int) -> List:
        coord_cases = []
        ligne_c = ligne + 1 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        
        ligne_c = ligne - 1 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        
        ligne_c = ligne 
        colonne_c = colonne + 1
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        
        ligne_c = ligne 
        colonne_c = colonne - 1
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        
        return coord_cases
    def case_safe(self,ligne,colonne) -> List:
        coord_cases = []
        ligne_c = ligne + 1 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        ligne_c = ligne + 2 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        ligne_c = ligne + 3 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        ligne_c = ligne - 1 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        ligne_c = ligne - 2 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        ligne_c = ligne - 3 
        colonne_c = colonne
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        ligne_c = ligne  
        colonne_c = colonne + 1
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        ligne_c = ligne  
        colonne_c = colonne + 2
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        
        ligne_c = ligne  
        colonne_c = colonne + 3
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        ligne_c = ligne  
        colonne_c = colonne - 1
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        ligne_c = ligne  
        colonne_c = colonne - 2
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        
        ligne_c = ligne  
        colonne_c = colonne - 3
        if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
            coord_cases.append([ligne_c,colonne_c])
        return coord_cases
    
    def case_guard_vis(self,ligne,colonne,element) -> List:
        coord_cases = []
        if element == HC.GUARD_E : 
            ligne_c = ligne  
            colonne_c = colonne + 1
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
            ligne_c = ligne  
            colonne_c = colonne + 2
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
        elif element == HC.GUARD_W : 
            ligne_c = ligne  
            colonne_c = colonne - 1
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
            ligne_c = ligne  
            colonne_c = colonne - 2
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
        elif element == HC.GUARD_S : 
            ligne_c = ligne -1 
            colonne_c = colonne 
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
            ligne_c = ligne -2 
            colonne_c = colonne 
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
        elif element == HC.GUARD_N: 
            ligne_c = ligne +1 
            colonne_c = colonne 
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
            ligne_c = ligne +2 
            colonne_c = colonne 
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
        return coord_cases

    def case_civil_vis(self,ligne:int,colonne:int,element:int) -> List:
        coord_cases = []
        if element == HC.CIVIL_E : 
            ligne_c = ligne  
            colonne_c = colonne + 1
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
        elif element == HC.CIVIL_W : 
            ligne_c = ligne  
            colonne_c = colonne - 1
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
        elif element == HC.CIVIL_S : 
            ligne_c = ligne -1 
            colonne_c = colonne 
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
        elif element == HC.CIVIL_N: 
            ligne_c = ligne +1 
            colonne_c = colonne 
            if ligne_c >= 0 and ligne_c < self.nb_lignes and colonne_c >= 0 and colonne_c < self.nb_colonnes :
                coord_cases.append([ligne_c,colonne_c])
        return coord_cases
#-----------------------------Class Map--------------------------------------------


    
    