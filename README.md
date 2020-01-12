# Projet d'ISN (2019)
Mathieu FOURRÉ et Ulysse VILLANUEVA

L'objectif du projet était de créer un jeu en python en utilisant la librairie PyGame.

Cette librairie est conçue pour faire des jeux en 2D mais nous avons décider de tout de même faire un jeu avec un aspect 3D. L’astuce est de faire avancer le personnage de case en case sans transition.

Nous avons donc généré les images pour une porte dans chaque position possible.
Par exemple, voici une porte tournée à gauche :

![image of a door](/img/tiles/tunnel%2B3%2B1_1.png)

Puis, ayant fait de même avec le sol et les murs et nous avons superposer les images de manière à donner une illusion de 3D.

![image of a tunnel](/tunnel.jpg)
![image of a room](/room.jpg)

La carte est générée procédurallement.
![image of the map](/the_map.png)
