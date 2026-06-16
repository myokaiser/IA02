from map import affiche_star_2, affiche_star_1
from phase12 import Phase1
from phase2 import Phase2
import time

def main():
    affiche_star_1()
    phase1 = Phase1()
    phase1.init_phase1()
    while not phase1.done :
        phase1.step()
        phase1.affichage_jeu_phase1()
        time.sleep(0.5)
        break

    # affiche_star_2()
    # phase2 = Phase2()
    # phase2.init_phase2()
    # while not phase2.done :
    #     phase2.step()
    #     phase2.affichage_jeu_phase2()
    #     time.sleep(0.5)

if __name__ == "__main__":
    main()
