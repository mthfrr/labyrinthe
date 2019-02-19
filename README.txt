Principe du projet
Le joueur se déplace en vue subjective dans un labyrinthe. Il cherche la sortie en essayant de
survivre.

Fonctionnalités du programme (par ordre de priorité décroissant)
- Le joueur peut voir la salle dans laquelle il se trouve en vue subjective.
- Le joueur doit déplacer de case en case pour visiter le labyrinthe et trouver la sortie.
- Chaque partie est unique et se déroule dans un labyrinthe différent.
- Le labyrinthe a toujours une solution et on ne peut pas être bloqué sans possibilité d’atteindre la
sortie
- Un système de clé permet d’ouvrir des portes de couleurs différentes pour avancer dans le
labyrinthe.
- Le personnage peut mourir de faim. Il faut donc trouver de la nourriture pour pouvoir survivre.
- Le joueur peut fuir ou attaquer les monstres se déplaçant dans le labyrinthe, afin de ne pas être
blessé ou tué.
- Des potions présentes dans le labyrinthe permettent de se soigner.
- La faim et la vie du personnage sont visible sur l’écran sous forme de barres.
- Une musique d’ambiance accompagne l’aventure du joueur.

Éléments de conception
Module d'entrées/sorties
Il comprend la boucle principale du programme sous Pygame:
‒ à partir du plan du labyrinthe et de la position du joueur, on calcule les images à afficher
(rotation pour tenir compte de l'orientation du joueur, choix de la bonne représentation des
objets et murs en fonctions de la position relative)
‒ affichage des bonnes images pour construire la vue subjective
(l'ordre d'affichage permet le bon masquage des objets les uns par les autres)
‒ gestion de la souris pour cliquer sur des boutons d'actions
‒ gestion du clavier pour les raccourcis et le déplacement
Module de construction du labyrinthe
‒ construction d'un labyrinthe aléatoire.
‒ parcours systématique du labyrinthe pour vérifier qu'il y a bien toujours un accès à la sortie; à
défaut, ajouter des connections entre les salles (algorithme de parcours en largeur d’un graphe)
‒ ajout d'éléments esthétiques dans les pièces
‒ dans une version avec clés, placer les portes colorées et les clés avant de vérifier que le trajet est
possible (même algorithme de parcours, avec plusieurs étapes : trouver la clé, trouver la porte,
etc.)
‒ ajout des objets du jeu (nourriture, potions, monstres, …)

Module de fabrication des images
‒ fabrication de scripts sous Povray

Module de gestion du joueur
‒ gestion des paramètres niveau de faim et points de vie du joueur

Module gestion des montres et combats
‒ déplacements aléatoire des montres « bêtes »
‒ déplacements vers le joueur des monstres « rusés »
‒ combats simplistes (par exemple victoire si « force du joueur + nb_aléatoire_entre_1_et_6 >
force du monstre + nb_aléatoire_entre_1_et_6 »)
