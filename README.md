# Projet 2 LIPPS

## Nom
[Simulation Robots et Incendies](https://drive.google.com/file/d/1i94PlvtSGv57BrwtZ7rXYKXhi4MbjQTA/view)

## Description
Ce projet est une simulation de gestion d'incendies et de robots pompiers. Il utilise Python et diverses bibliothèques pour créer une interface graphique interactive et des algorithmes de simulation réalistes. L'utilisateur peut décider de lancer des fichiers instructions qu'il a lui-même conçu ou lancer un fichier instructions pré-existant ou encore lancer un mode de jeu permettant de choisir les actions à effectuer à chaque tour en utilisant la méthode `next()`. 

## Prérequis
Pour exécuter ce projet, vous devez avoir Python installé sur votre machine. Vous pouvez télécharger Python [ici](https://www.python.org/downloads/).

## Installation des Bibliothèques
Avant de lancer le projet, assurez-vous d'installer les bibliothèques nécessaires. Vous pouvez les installer en utilisant pip, par exemple :

`pip install pygame`\
`pip install tkinter`

## Lancer le projet
Pour lancer le projet, télécharger le dossier zip contenant les fichiers du dépôt "Projet 2 LIPPS".
Ensuite, après en avoir extrait les fichiers sur votre ordinateur, lancer le fichier mainInterface.py. Assurez d'avoir bien téléchargé toutes les bibliothèques nécessaires, en suivant la même procédure que dans Installation des Bibliothèques.  

## Fichiers et Répertoires
- **main.py** : Le fichier principal pour lancer la simulation.
- **Robots.py** : Contient les classes et les méthodes liées aux robots pompiers.
- **incendie__carte_case.py** : Contient les classes et les méthodes liées aux incendies, à la carte et aux cases.
- **README.md** : Ce fichier.
- **instructions** : Répertoire contenant les fichiers instructions sous la forme 'instructions_nomDeLaCarte'.
- **images** : Répertoire contenant toutes les images libres de droit nécessaires pour l'exécution du code du projet.

## Comment évoluer dans le jeu ?
3 modes de jeu sont disponibles sur le menu principal qui s'affiche lors de l'exécution de main.py :
- **Suivre un scénario prédéfini**
- **Jeu avec le vent**
- **Jeu solo**

Pour naviguer entre ces différents modes de jeu, il est nécessaire d'utiliser les flèches haut et bas du clavier. Puis pour sélectionner une carte, il faut se placer dessus à l'aide des flèches de direction et ensuite presser sur la touche Entrée.

Après avoir choisi un mode de jeu, un sous_menu comportant les différentes cartes disponibles apparaît.

Pour naviguer entre ces différentes cartes, on se comporte de la même manière que sur le menu principal.

Pour le **premier mode de jeu** : 'Suivre un scénario prédéfini', il faut s'assurer qu'un fichier txt dont le nom est de la forme 'instructions_nomDeLaCarte' est présent dans le dossier instructions.

Ce fichier instructions comporte une ligne par robot présent sur la carte avec sur chaque ligne le nom du robot parmi DRONE, ROUES, PATTES et CHENILLES suivi des actions que le robot doit effectuer parmi N, S, E, O qui représentent une direction vers les 4 points cardinaux respectivement Nord, Sud, Est et Ouest. Deux autres actions possibles sont représentées par les lettres L et R respectivement pour largage et remplissage. Voici un exemple de ligne dans un fichier instructions :\
DRONE,O,O,O,S,S,S,L,E,E,E,R,S,O,O,L,O,L,N,E,L

Le **deuxième mode de jeu** permet à l'utilisateur de voir la propagation du vent. Il se joue comme le troisième mode de jeu mais à chaque appel de la méthode `next()`, le feu peut se propager, il est possible de modifier la difficulté du jeu avec le vent en modulant la difficulté de 1 à 3 (du plus facile au plus dur) ce qui influence la probabilité que le vent se propage.
La chiffre à modifier se situe dans la classe choisir, dans la fonction lancer_jeu_vent (peut être trouvé à l'aide d'un CTRL+F) :\
`a = jeux_avec_vent(self.sous_menu.options[choix], 1)`\
Après avoir choisi ce mode de jeu, il faudra choisir la direction de la propagation du vent en utilisant les flèches directionnels ainsi que la touche Entrée.
En complément des touches disponibles et expliquées dans le paragraphe ci-dessous, dans le deuxième mode de jeu, il est possible d'appuyer sur la touche B pour faire appel à une boussole.

Le **troisième mode de jeu** permet à l'utilisateur de décider des instructions qu'il souhaite lancer. Voici les différentes touches pour manipuler ce jeu :

- **1, 2, 3, etc.** : Choisir un robot parmi ceux disponibles. Le robot choisi apparaîtra dans la console.
- **Z, Q, S, D** : Après avoir choisi un robot, utilisez les flèches pour assigner les directions (N, O, S, E) que vous souhaitez que le robot suive. Vous pouvez donner autant d'instructions que vous le souhaitez à chaque robot.
- **Touche Bas** : Exécuter les instructions données en appelant la méthode `next()`. Certaines instructions nécessitent plusieurs appels de la méthode `next()` dû à la vitesse différente d'exécution des actions par les différents robots.
- **Touche Haut** : Réinitialiser la simulation en appelant la méthode `restart()`.
- **Touche Gauche (Left)** : Larguer l'eau du robot.
- **Touche Droite (Right)** : Remplir le réservoir du robot.
- **Touche A** : Ouvrir une fenêtre d'attributs affichant tous les attributs du robot sélectionné. Cette fenêtre peut être fermée en appuyant de nouveau sur la touche A ou en appuyant sur la touche Entrée.
- **Touche R** : Afficher la barre de remplissage d'eau du robot sélectionné.
- **Touche M** : Retourner au menu principal.
- **Touche V** : Permet d'accéder à toutes les commandes liées à la musique (contrôle du volume : flèches haut et bas, changer de musique : flèches droite et gauche, mettre sur pause : touche Espace).
- **Touche H** : Afficher une fenêtre d'aide listant toutes les actions possibles.

## Auteurs
JOLY Tristan\
UTHAYAKUMAR Tharushan

## Support
Pour toute question ou suggestion, veuillez contacter les auteurs via leurs adresses email respectives :\
tristan.joly@universite-paris-saclay.fr\
tharushan.uthayakumar@universite-paris-saclay.fr

Merci d'avoir utilisé notre simulation d'incendies et de robots. Nous espérons que vous trouverez ce projet utile et éducatif !

P.S. : Un petit easter egg peut être trouvé sur le menu principal !!
