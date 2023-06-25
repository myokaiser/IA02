Ce fichier a pour objectif d'expliquer brièvement le fonctionnement du projet.
Vous trouverez également la modélisation SAT et STRIPS à la fin de ce document.

# ----------ATTENTION---------- #
Avant d'exécuter la fonction main du projet (faisant tourner la pahse 1 et 2), veuillez vérifier que vous ouvrez le projet à partir du sous dossier "PROJET" du rendu au lieu de l'ouvrir à partir de "06_LE_MINH_SCHENTEN". Sinon, le processus des fichiers cnf de la phase1 retournera une erreur.
L'attribut __world de la classe HitmanReferee se basant exclusivement sur word_example (la carte sous forme de matrice), il faudra modifier cette variable dans le fichier hitman.py pour qu'Hitman tente d'assassiner sa cible sur d'autres environnements.
# ----------ATTENTION---------- #

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
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------#
              SAT
# -------------------------------#

Modélisation SAT :
n : nombre de lignes
m : nombre de colonnes
Soit un monde composé de n*m cases numérotées de (1,1) à (n,m).
Soit x un nombre compris entre 1 et n et y compris entre 1 et m.


Variables propositionnelles :
H(x,y) : Le personnage Hitman se trouve à la position (x, y)
G(x,y) : il y a un garde à la position (x, y)
C(x,y) : il y a un civil à la position (x, y)
T(x,y) : La cible se trouve à la position (x, y)
W(x,y) : il y a un mur à la position (x, y)
P(x,y) : il y a la corde de piano à la position (x, y)
C(x,y) : il y a le costume à la position (x, y)

Contraintes:
Contraintes at_least_one :
On veut qu'il existe au moins une clause vraie, c’est-à-dire qu’Hitman est présent dans au moins une case EMPTY.
On a donc : H(1,1) OR … OR H(n,m) -> True, et E(x,y) OU C(x,y) ((x,y) étant une case où il n’y a rien ou un civil qu’on peut traverser en s’excusant)
Contrainte unique : 
A OR -B OR -C OR -D
Si A est vrai, alors B, C et Dsont faux. 
Donc dans notre cas, si H(x,y), alors on a -H(i,j) pour tout i appartenant à [1;n] sauf x et pour tout j appartenant à [1;m] sauf y
Donc -H(1,1) OR … OR H(x,y) OR … OR -H(n,m), et E(x,y) OR CIVIL(x,y) ((x,y) étant une case où il n'y a rien)




# -------------------------------#
              STRIPS
# -------------------------------#
STRIPS:
Fluent : Hitman(x,y)
	 clear(x,y)
	 Cible(x,y)
	 Garde(x,y)
	 Civil(x,y)
	 Corde(x,y)
	 Suit(x,y)

prédicat : Mur(x,y)
 	   Succ(x,y)
	   PossedeSuit(x,y)
	   PossedeCorde(x,y)
	   Porter(x,y)
           DirectionT(x,y)
           DirectionB(x,y)
           DirectionL(x,y)
           DirectionR(x,y)

Actions :
TournerHoraire (T, B, L, R) : Fait tourner Hitman de 90 degrés dans le sens horaire.

TournerAntiHoraire (T, B, L, R) : Fait tourner Hitman de 90 degrés dans le sens anti-horaire.

Avancer (T, B, L, R) : Fait avancer Hitman d'une case dans la direction actuelle.

TuerCible (T, B, L, R) : Hitman utilise la corde de piano pour tuer la cible.

NeutraliserGarde (T, B, L, R) : Hitman neutralise un garde en le rendant incapable de le voir.

NeutraliserCivil (T, B, L, R) : Hitman neutralise un civil en le rendant incapable de le voir.

PasserCostume : Hitman passe le costume de serveur pour se fondre parmi les invités.

PrendreCostume : Hitman prend le costume de serveur à sa position actuelle.

PrendreArme : Hitman prend la corde de piano à sa position actuelle.


États initiaux :
Hitman est à une position initiale donnée (0, 0), le costume de serveur est à une position spécifique (ex (x', y')), la corde de piano est à une position spécifique (ex (x'', y'')) et la cible est à une position spécifique (ex (x, y)).
Init(Hitman(0,0) ^ Cible(x, y) ^ Corde(x'', y'') ^ Suit(x', y'))


États finaux (objectifs) :
Hitman est à la position initiale (0, 0) et la cible est tuée.
Goal(Hitman(0, 0) ^ TuerCible(x, y))


Préconditions et effets des actions :

------------------------------------------------------------------------------------------------------- TournerHoraire
TournerHoraire_T(x, y) :
	Préconditions : Hitman(x, y) ^ DirectionT(x, y) (Hitman regarde au nord et tourne dans le sens horaire (est))
	Effets : Hitman(x, y) ^ DirectionR(x, y)

TournerHoraire_B(x, y) :
	Préconditions : Hitman(x, y) ^ DirectionB(x, y) (Hitman regarde le sud et tourne dans le sens horaire (ouest))
	Effets : Hitman(x, y) ^ DirectionL(x, y)

TournerHoraire_L(x, y) :
	Préconditions : Hitman(x, y) ^ DirectionL(x, y) (Hitman regarde l'ouest et tourne dans le sens horaire (nord))
	Effets : Hitman(x, y) ^ DirectionT(x, y)

TournerHoraire_R(x, y) :
	Préconditions : Hitman(x, y) ^ DirectionR(x, y) (Hitman regarde l'est et tourne dans le sens horaire (sud))
	Effets : Hitman(x, y) ^ DirectionB(x, y)


------------------------------------------------------------------------------------------------------- TournerAntiHoraire
TournerAntiHoraire_T(x, y) :
	Préconditions : Hitman(x, y) ^ DirectionT(x, y) (Hitman regarde au nord et tourne dans le sens anti horaire (ouest))
	Effets : Hitman(x, y) ^ DirectionL(x, y)

TournerAntiHoraire_B(x, y) :
	Préconditions : Hitman(x, y) ^ DirectionB(x, y) (Hitman regarde au sud et tourne dans le sens anti horaire (est))
	Effets : Hitman(x, y) ^ DirectionR(x, y)

TournerAntiHoraire_L(x, y) :
	Préconditions : Hitman(x, y) ^ DirectionL(x, y) (Hitman regarde l'ouest et tourne dans le sens anti horaire (sud))
	Effets : Hitman(x, y) ^ DirectionB(x, y)

TournerAntiHoraire_R(x, y) :
	Préconditions : Hitman(x, y) ^ DirectionR(x, y) (Hitman regarde l'est et tourne dans le sens anti horaire (nord))
	Effets : Hitman(x, y) ^ DirectionT(x, y)


------------------------------------------------------------------------------------------------------- Avancer
Avancer_T(x, y, x', y') : 
	Préconditions : Hitman(x, y) ^ -Mur(x', y') ^ DirectionT(x, y) (il n'y a pas de mur, Hitman avance devant lui)
	Effets : Hitman(x', y') ^ DirectionT(x, y)

Avancer_B(x, y, x', y') : 
	Préconditions : Hitman(x, y) ^ -Mur(x', y') ^ DirectionB(x, y) (il n'y a pas de mur, Hitman avance devant lui)
	Effets : Hitman(x', y') ^ DirectionB(x, y)

Avancer_L(x, y, x', y') : 
	Préconditions : Hitman(x, y) ^ -Mur(x', y') ^ DirectionL(x, y) (il n'y a pas de mur, Hitman avance devant lui)
	Effets : Hitman(x', y') ^ DirectionL(x, y)

Avancer_R(x, y, x', y') : 
	Préconditions : Hitman(x, y) ^ -Mur(x', y') ^ DirectionR(x, y) (il n'y a pas de mur, Hitman avance devant lui)
	Effets : Hitman(x', y') ^ DirectionR(x, y)


------------------------------------------------------------------------------------------------------- TuerCible
TuerCible_T(x, y, x', y') :
	Préconditions : Cible(x', y') ^ Hitman(x, y) ^ PossedeCorde(x, y) ^ Succ(y, y') ^ DirectionT(x, y) (Hitman est devant la cible et a la corde de piano)
	Effets : clear(x', y') ^ Hitman(x', y') ^ DirectionT(x, y) (La cible est tuée)

TuerCible_B(x, y, x', y') :
	Préconditions : Cible(x', y') ^ Hitman(x, y) ^ PossedeCorde(x,y) ^ Succ(x, x') ^ DirectionB(x, y) (Hitman est devant la cible et a la corde de piano)
	Effets : clear(x', y') ^ Hitman(x', y') ^ DirectionB(x, y) (La cible est tuée)

TuerCible_L(x, y, x', y') :
	Préconditions : Cible(x', y') ^ Hitman(x, y) ^ PossedeCorde(x,y) ^ Succ(x, x') ^ DirectionL(x, y) (Hitman est devant la cible et a la corde de piano)
	Effets : clear(x', y') ^ Hitman(x', y') ^ DirectionL(x, y) (La cible est tuée)

TuerCible_R(x, y, x', y') :
	Préconditions : Cible(x', y') ^ Hitman(x, y) ^ PossedeCorde(x,y) ^ Succ(x, x') ^ DirectionR(x, y) (Hitman est devant la cible et a la corde de piano)
	Effets : clear(x', y') ^ Hitman(x', y') ^ DirectionR((x, y) (La cible est tuée)


------------------------------------------------------------------------------------------------------- NeutraliserGarde
NeutraliserGarde_T(x, y, xg, yg) :
	Préconditions : Hitman(x, y) ^ Garde(xg, yg) ^ Succ(y, yg) ^ VisionGarde(x, y, xg, yg) ^ DirectionT(x, y) (Hitman est au-dessus du garde, regarde le garde et le garde ne le regarde pas)
	Effets : clear(xg, yg) ^ Hitman(xg, yg) ^ DirectionT(y, yg) (Le garde est neutralisé et ne peut plus voir Hitman)

NeutraliserGarde_B(x, y, xg, yg) :
	Préconditions : Hitman(x, y) ^ Garde(xg, yg) ^ Succ(y, yg) ^ VisionGarde(x, y, xg, yg) ^ DirectionB(x, y) (Hitman est en-dessous du garde, regarde le garde et le garde ne le regarde pas)
	Effets : clear(xg, yg) ^ Hitman(xg, yg) ^ DirectionB(x, y) (Le garde est neutralisé et ne peut plus voir Hitman)

NeutraliserGarde_L(x, y, xg, yg) :
	Préconditions : Hitman(x, y) ^ Garde(xg, yg) ^ Succ(x, xg) ^ VisionGarde(x, y, xg, yg) ^ DirectionL(x, y) (Hitman est à gauche du garde, regarde le garde et le garde ne le regarde pas)
	Effets : clear(xg, yg) ^ Hitman(xg, yg) ^ DirectionL(x, y) (Le garde est neutralisé et ne peut plus voir Hitman)

NeutraliserGarde_R(x, y, xg, yg) :
	Préconditions : Hitman(x, y) ^ Garde(xg, yg) ^ Succ(x, xg) ^ VisionGarde(x, y, xg, yg) ^ DirectionR(x, y) (Hitman est à droite du garde, regarde le garde et le garde ne le regarde pas)
	Effets : clear(xg, yg) ^ Hitman(xg, yg) ^ DirectionR(x, y) (Le garde est neutralisé et ne peut plus voir Hitman)


------------------------------------------------------------------------------------------------------- NeutraliserCivil
NeutraliserCivil_T(x, y, xc, yc) :
	Préconditions : Hitman(x, y) ^ Civil(xc, yc) ^ Succ(y, yc) ^ VisionCivil(x, y, xc, yc) ^ DirectionT(x, y) (Hitman est au-dessus du civil, regarde le civil et le civil ne le regarde pas)
	Effets : clear(xc, yc) ^ Hitman(xc, yc) ^ DirectionT(x, y) (Le civil est neutralisé et ne peut plus voir Hitman)

NeutraliserCivil_B(x, y, xc, yc) :
	Préconditions : Hitman(x, y) ^ Civil(xc, yc) ^ Succ(y, yc) ^ VisionCivil(x, y, xc, yc) ^ DirectionB(x, y) (Hitman est en-dessous du civil, regarde le civil et le civil ne le regarde pas)
	Effets : clear(xc, yc) ^ Hitman(xc, yc) ^ DirectionB(x, y) (Le civil est neutralisé et ne peut plus voir Hitman)

NeutraliserCivil_L(x, y, xc, yc) :
	Préconditions : Hitman(x, y) ^ Civil(xc, yc) ^ Succ(x, xc) ^ VisionCivil(x, y, xc, yc) ^ DirectionL(x, y) (Hitman est à gauche du civil, regarde le civil et le civil ne le regarde pas)
	Effets : clear(xc, yc) ^ Hitman(xc, yc) ^ DirectionL(x, y) (Le civil est neutralisé et ne peut plus voir Hitman)

NeutraliserCivil_R(x, y, xc, yc) :
	Préconditions : Hitman(x, y) ^ Civil(xc, yc) ^ VisionCivil(x, y) ^ DirectionR(x, y) (Hitman est à droite du civil, regarde le civil et le civil ne le regarde pas)
	Effets : clear(xc, yc) ^ Hitman(xc, yc) ^ DirectionR(x, y) (Le civil est neutralisé et ne peut plus voir Hitman)


------------------------------------------------------------------------------------------------------- PasserCostume
PasserCostume(x, y) :
	Préconditions : Hitman(x, y) ^ PossedeSuit(x, y) (Hitman a le costume de serveur)
	Effets : Porter(x, y) ^ Hitman(x, y) (Hitman porte le costume de serveur)


------------------------------------------------------------------------------------------------------- PrendreCostume
PrendreCostume(x, y) :
	Préconditions : Hitman(x, y) ^ Suit(x, y) (Hitman est à la même position que le costume de serveur)
	Effets : clear(x, y) ^ PossedeSuit(x, y) ^ Hitman(x, y) (Hitman a le costume de serveur)


------------------------------------------------------------------------------------------------------- PrendreArme
PrendreArme(x, y) :
	Préconditions : Hitman(x, y) ^ Corde(x, y) (Hitman est à la même position que la corde de piano)
	Effets : clear(x, y) ^ PossedeCorde(x, y) ^ Hitman(x, y) (Hitman a la corde de piano)
