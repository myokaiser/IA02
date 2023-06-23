from map import affiche_star_2, affiche_star_1
from phase1 import Phase1
from phase2 import matrix_to_dico, trouver_corde, boucle
from hitman.hitman import HitmanReferee, complete_map_example

def main():
    affiche_star_1()
    phase1 = Phase1()
    map_str = phase1.phase1()
    map_str = str(map_str)
    affiche_star_2()
    hr = HitmanReferee()
    state = hr.start_phase2()
    map = matrix_to_dico(hr._HitmanReferee__world)
    corde = trouver_corde(map)
    state = boucle(corde, state, 'weapon', map)

if __name__ == "__main__":
    main()
