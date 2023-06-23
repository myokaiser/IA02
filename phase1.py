from map import Map,unique,at_most_number, display_map_phase1
from hitman.hitman import HitmanReferee, HC
from typing import List, Dict, Tuple

Grid = List[List[int]] 
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]
Position = [int,int]
Orientation = str #N,E,S,O


#-----------------------------Class Phase1------------------------------------------------
class Phase1():
    def __init__(self ) -> None:
        self.hitman = HitmanReferee()
        self.informations_actuelles = self.hitman.start_phase1()
        self.map = Map(self.informations_actuelles["m"], self.informations_actuelles["n"], self.informations_actuelles["guard_count"], self.informations_actuelles["civil_count"])


    def vision(self) -> int:
        nb_cases_visible = len(self.informations_actuelles['vision'])
        for i in range(nb_cases_visible):

            coord_case = self.informations_actuelles['vision'][i][0]
            element = self.informations_actuelles['vision'][i][1]
            if element == HC.WALL:
                clause_personne = self.map.var_not_personne(coord_case)
                clause = self.map.var_mur(coord_case)
            elif element == HC.EMPTY :
                clause_personne = self.map.var_not_personne(coord_case)
                clause = self.map.var_rien(coord_case)
            elif element == HC.TARGET:
                clause_personne = self.map.var_not_personne(coord_case)
                clause = self.map.var_cible(coord_case)
            elif element == HC.PIANO_WIRE:
                clause_personne = self.map.var_not_personne(coord_case)
                clause = self.map.var_corde(coord_case)
            elif element == HC.SUIT:
                clause = self.map.var_costume(coord_case)
                clause_personne = self.map.var_not_personne(coord_case)
            elif element == HC.GUARD_E or element == HC.GUARD_N or element == HC.GUARD_S or element == HC.GUARD_W:
                clause_personne = self.map.var_personne(coord_case)
                cases_vu = self.map.case_guard_vis(coord_case[1],coord_case[0],element)
                print("vision du garde ("+str(coord_case[1])+","+str(coord_case[0])+") : "+str(cases_vu))
                for case in cases_vu : 
                    clause_safe = self.map.var_not_safe((case[1],case[0]))
                    self.map.add_safe_clause(clause_safe)
                if element == HC.GUARD_E : 
                    clause = self.map.var_guard_e(coord_case)
                elif element == HC.GUARD_N : 
                    clause = self.map.var_guard_n(coord_case)
                elif element == HC.GUARD_S : 
                    clause = self.map.var_guard_s(coord_case)
                elif element == HC.GUARD_W : 
                    clause = self.map.var_guard_w(coord_case)

            elif element == HC.CIVIL_E or element == HC.CIVIL_N or element == HC.CIVIL_S or element == HC.CIVIL_W:
               
                clause_personne = self.map.var_personne(coord_case)
                cases_vu = self.map.case_civil_vis(coord_case[1],coord_case[0],element)
                print("vision du garde ("+str(coord_case[1])+","+str(coord_case[0])+") : "+str(cases_vu))
                for case in cases_vu : 
                    clause_safe = self.map.var_not_safe((case[1],case[0]))
                    self.map.add_safe_clause(clause_safe)

                if element == HC.CIVIL_E : 
                    clause = self.map.var_civil_e(coord_case)
                elif element == HC.CIVIL_N : 
                    clause = self.map.var_civil_n(coord_case)
                elif element == HC.CIVIL_S : 
                    clause = self.map.var_civil_s(coord_case)
                elif element == HC.CIVIL_W : 
                    clause = self.map.var_civil_w(coord_case)

            self.map.add_person_clause(clause_personne)
            self.map.add_known_clause(clause)
            print(str(element)+ " en ("+ str(coord_case[0]) + ", "+str(coord_case[1]) + ")")
            
            
        return nb_cases_visible

    def hear(self) -> None:
        nb_personne_entendue = self.informations_actuelles['hear']
        
        coord_cases = self.map.hear_case(self.informations_actuelles['position'][1],self.informations_actuelles['position'][0])
        variables_personnes = []
        for coord in coord_cases:
            if nb_personne_entendue == 0:
                clause = self.map.var_not_personne((coord[1],coord[0]))
                self.map.add_person_clause(clause)
            else :
                clause = self.map.var_personne((coord[1],coord[0]))
                if self.map.known_case(coord[0],coord[1]) == False: 
                    variables_personnes.append(clause[0])
                


        if variables_personnes != []:
            if nb_personne_entendue == 1 : 
                clauses = unique(variables_personnes)
                
                for clause in clauses : 
                    self.map.add_person_prob_clause(clause)
                    

            elif nb_personne_entendue >= 2 and nb_personne_entendue < 5 : 
                clauses = at_most_number(variables_personnes, nb_personne_entendue)
                for clause in clauses : 
                    self.map.add_person_prob_clause(clause)
                    

            elif nb_personne_entendue == 5:
                if self.map.nb_gardes + self.map.nb_civils <= 5 :
                    clauses = at_most_number(variables_personnes, nb_personne_entendue)
                    for clause in clauses : 
                        self.map.add_person_prob_clause(clause)
                        
                else:
                    pass

    def affichage_jeu_phase1(self) -> None:
        print("position : ("+str(self.informations_actuelles['position'][0])+" , "+str(self.informations_actuelles['position'][1])+")")
        display_map_phase1(self.map.known_Map(), self.informations_actuelles)

    def case_more_safe(self,cases: list) -> Tuple:
        unsafe = []
        safe = []
        scores = []
        nb_pos = []
        id = 0
        for case in cases : 
            
            if self.map.case_not_safe(case[0],case[1]) == True:
                unsafe.append(case)
            else : 
                case_safe = self.map.case_safe(case[0],case[1])
                scores.append(self.map.get_grille_score(case[0],case[1]))
                safe.append(case)
                nb_pos.append(0)
                for case_safety in case_safe :  
                    if self.map.case_maybe_personne(case_safety[0],case_safety[1]) == True : 
                        scores[id] -= 1
                        nb_pos[id] += 1
                    
                id += 1
        print("cases not safe : " + str(unsafe))
        if len(safe) == -1 : 
            return unsafe[0]
        else : 
            print("cases safe : " + str(safe))
            max = scores[0]
            case_suivante = safe[0]
            for num in range(id) : 
                print(str(safe[num])+" | score de la case : " + str(scores[num])+" | nb d'incertitude :"+str(nb_pos[num]))
                if scores[num] > max : 
                    max = scores[num]
                    case_suivante = safe[num]
            if max < -18 and len(unsafe) > 0:
                return unsafe[0]
                    
        return case_suivante

    def end_phase_1(self) -> Dict:
        dictionnaire =  self.map.known_Map()
        self.hitman.send_content(dictionnaire)
        _, score, _ , true_map = self.hitman.end_phase1()
        print(score)
        print(true_map)
        return dictionnaire

    def set_orientation_case_suiv(self,ligne:int,colonne:int) -> None:
        orientation = self.informations_actuelles['orientation']
        pos = self.informations_actuelles['position']
        if orientation == HC.N :
            if ligne == pos[1] - 1:
                self.hitman.turn_clockwise()
                self.affichage_jeu_phase1()
                self.hitman.turn_clockwise()
                self.affichage_jeu_phase1()
            elif colonne == pos[0] - 1:
                self.hitman.turn_anti_clockwise()
                self.affichage_jeu_phase1()
            elif colonne == pos[0] + 1:
                self.hitman.turn_clockwise()
                self.affichage_jeu_phase1()
        elif orientation == HC.E :
            if ligne == pos[1] - 1:
                self.hitman.turn_clockwise()
                self.affichage_jeu_phase1()
            elif ligne == pos[1] + 1:
                self.hitman.turn_anti_clockwise()
                self.affichage_jeu_phase1()
            elif colonne == pos[0] - 1:
                self.hitman.turn_clockwise()   
                self.affichage_jeu_phase1()
                self.hitman.turn_clockwise()    
                self.affichage_jeu_phase1()
        
        elif orientation == HC.S :
            if ligne == pos[1] + 1:
                self.hitman.turn_clockwise()
                self.affichage_jeu_phase1()
                self.hitman.turn_clockwise()
                self.affichage_jeu_phase1()
            elif colonne == pos[0] - 1:
                self.hitman.turn_clockwise()
                self.affichage_jeu_phase1()
            elif colonne == pos[0] + 1:
                self.hitman.turn_anti_clockwise()  
                self.affichage_jeu_phase1()
        
        elif orientation == HC.W :
            if ligne == pos[1] + 1:
                self.hitman.turn_clockwise()
                self.affichage_jeu_phase1()
            elif ligne == pos[1] - 1:
                self.hitman.turn_anti_clockwise()
                self.affichage_jeu_phase1()
            elif colonne == pos[0] + 1:
                self.hitman.turn_clockwise()  
                self.affichage_jeu_phase1()
                self.hitman.turn_clockwise()   
                self.affichage_jeu_phase1()
    

    def phase1(self) -> Dict:
        self.map.clauses_connues.append(self.map.var_rien((self.informations_actuelles['position'][0],self.informations_actuelles['position'][1])))
        it=0
        phase1 = []
        nb_cases = self.map.nb_colonnes * self.map.nb_lignes
        while(it<2*nb_cases):
            phase1.append([self.informations_actuelles['position'][0],self.informations_actuelles['position'][1]])
            print("ITERATION : "+str(it))
            print("Score vision : 0")
            self.vision()
            self.hear()
            self.map.set_grille_score(self.informations_actuelles['position'][1],self.informations_actuelles['position'][0],-6)
            
            if self.map.case_go(self.informations_actuelles['position'][1],self.informations_actuelles['position'][0]) == False :
                for i in range(3):
                    print("Score vision : "+str(i+1))
                    self.informations_actuelles = self.hitman.turn_anti_clockwise()
                    self.affichage_jeu_phase1()
                    self.vision()
            
            move_case = self.map.move_case(self.informations_actuelles['position'][1],self.informations_actuelles['position'][0])

            cases_possible_deplacement = []
            for case in move_case:
                if self.map.case_mur(case[0],case[1]) == False and self.map.case_personne(case[0],case[1]) == False:
                    cases_possible_deplacement.append(case)
            
            if len(cases_possible_deplacement) >= 1 : 
                case_suivante = self.case_more_safe(cases_possible_deplacement)
            else : 
                case_suivante = cases_possible_deplacement[0]
            
            clause_passage = self.map.var_pass_case((self.informations_actuelles['position'][0],self.informations_actuelles['position'][1]))
            self.map.add_pass_clause(clause_passage)

            self.set_orientation_case_suiv(case_suivante[0],case_suivante[1])
            self.informations_actuelles = self.hitman.move()
            self.affichage_jeu_phase1()

            it += 1
            print("Parcours : "+str(phase1))
            nb_cases_trouvees = self.map.nb_known_case()
            print("Nb cases connues : "+str(nb_cases_trouvees))
            if nb_cases_trouvees >= self.map.nb_cases_a_trouver:
                return self.end_phase_1()

        return self.end_phase_1()

        
    
    
