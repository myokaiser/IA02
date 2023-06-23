Tout d'abord, la phase 1 utilise les fichier phase1.py et map.py et la phase 2 utilise le fichier phase2.py

Pour notre projet on utilise les bibliothèques suivantes:
Pour la phase 1 :
-typing (import List, Tuple, Dict)
-subprocess
-itertools (import combinations)
-numpy
-os

Pour la phase 2 :
-display_map (from map)
-typing (import List, Tuple, Dict)
-pprint (import pprint)
-time

-typing : Elle est utilisée pour ajouter des annotations de types aux variables. Les imports tels que List, Tuple et Dict sont utilisés pour déclarer des types spécifiques, comme des listes, des tuples et des dictionnaires.
subprocess : Cette bibliothèque permet d'exécuter des commandes système à partir du code Python.
-itertools : Cette bibliothèque fournit des fonctions pour créer des itérations combinatoires. Dans ce cas, l'import combinations est utilisé pour générer toutes les combinaisons possibles d'éléments d'un ensemble.
-time : Cette bibliothèque fournit des fonctionnalités liées au temps. 


Dans le fichier phase1.py, nous définisson la classe Phase1 ainsi que les méthodes associées tel que la méthode "phase1" qui va explorer la map, mettre à jour les informations du personnage et rechercher toutes les cases nécessaires pour terminer la phase 1 du jeu.
La phase 1 fait un affichage mis à jour du labyrinthe en fonction des trouvailles de Hitamn (certains objets comme la corde ou le costume peuvent apparaitre à des coordonnées qui ne correspondent pas à celle de la réalité en fonction de l'ensemble des déductions faites, mais se positionneront bien lorsqu'Hitman aura assez d'informations.


Dans le fichier map.py, nous définisson la classe Map ainsi que les méthodes associées mais également des fonctions liés à l'affichage de la map, des fonctions liés aux fichiers .cnf et enfin des fonctions liés aux contraintes.

Dans le fichier phase2.py, nous définissons une fonction principale nommée boucle qui repose sur le fonctionnement d'un algorithme A*. Hitman, ayant pleinement conaissance de la carte, va s'imaginer parcourir la carte jusqu'aux points d'intéret du jeu (ex : corde, costume, cible) de la manière la plus optimale possible tout en évitant au maximum le regard et la neutralisation des individus de la salle.
Une fois qu'Hitman a réfléchi à la façon d'arriver à son objectif, il parcourt la carte jusqu'à fin de la mission. Son objectif est mis à jour suivant les obstacles qui se mettent en travers de sa route. 
Tout comme la phase 1, la phase 2 va s'afficher sous la forme du parcours d'un curseur (< < ^ v) représentant Hitman qui va modifier l'affichage de la carte en fonction des neutralisations effectuées et des objets récupérés



Enfin , le main lance la phase 1 avec la méthode "phase1" puis affiche la map avant de lancer la phase 2.

L'attribut __world de la classe HitmanReferee se basant exclusivement sur word_example (la carte sous forme de matrice), il faudra modifier cette variable dans le fichier hitman.py pour qu'Hitman tente d'assassiner sa cible sur d'autres environnements.
