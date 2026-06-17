from raw.map import affiche_star_2, affiche_star_1
from raw.phase1 import Phase1
from raw.phase2 import Phase2

def main():
    affiche_star_1()
    phase1 = Phase1()
    map_str = phase1.phase1()
    print("map_str", map_str)
    map_str = str(map_str)

    # affiche_star_2()
    # phase2 = Phase2()
    # phase2.phase2()

if __name__ == "__main__":
    main()
