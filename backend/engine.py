from phase1 import Phase1
from phase2 import Phase2
from map import matrix_to_dico
from hitman.hitman import HitmanReferee
import HC


class GameEngine:
    def __init__(self):
        self.phase = 1

        # init phase 1
        self.phase1 = Phase1()
        self.phase1.phase1()

        # init phase 2
        self.phase2 = Phase2()
        self.phase2.phase2()

    def step(self):
        """
        1 tick du jeu
        """

        if self.phase == 1:
            # si phase1 est déjà exécutée en bloc
            self.phase = 2

        elif self.phase == 2:
            self.state = self.phase2.step(self.state, self.map)

        return self.get_state()

    def get_state(self):
        return {
            "map": self.map,
            "position": self.state["position"],
            "orientation": self.state["orientation"],
            "phase": self.phase
        }