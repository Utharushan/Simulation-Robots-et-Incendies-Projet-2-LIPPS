import pygame
import sys
from Robots import *
from pop_up import *
from incendie__carte_case import *
from pygame.locals import *
import time
import random
from random import randint as rnt
import tkinter as tk
from tkinter import ttk
pygame.init()

# Dimensions de la fenêtre
fenetre = pygame.display.set_mode((700, 700))

#On charge toutes les images nécessaires dans un  dictionnaire afin qu'on n'aie à les charger qu'une seule fois.
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
IMAGES = {
    "TERRAIN_LIBRE": pygame.image.load("images/terrain_libre.png").convert_alpha(),
    "FORET": pygame.image.load("images/foret.png").convert_alpha(),
    "ROCHE": pygame.image.load("images/roche.png").convert_alpha(),
    "EAU": pygame.image.load("images/eau.png").convert_alpha(),
    "HABITAT": pygame.image.load("images/habitat.png").convert_alpha(),
    "ROUES": pygame.image.load("images/roues.png").convert_alpha(),
    "CHENILLES": pygame.image.load("images/chenilles.png").convert_alpha(),
    "PATTES": pygame.image.load("images/pattes.png").convert_alpha(),
    "DRONE": pygame.image.load("images/drone.png").convert_alpha(),
    "INCENDIE": pygame.image.load("images/incendie.png").convert_alpha(),
    "DRONE_verser" : pygame.image.load("images/drone_verser.png").convert_alpha(),
    "PATTES_verser" : pygame.image.load("images/pattes_verser.png").convert_alpha(),
    "CHENILLES_verser":pygame.image.load("images/chenilles_verser.png").convert_alpha(),
    "ROUES_verser":pygame.image.load("images/roues_verser.png").convert_alpha()
}

#-----------------------------------------------------------------------------------------------------------------------------------------------------------    
def checke_liste_de_A(tab):
    """
    Prend en entrée une liste tab
    --------------------------------------------------------------------------------------------------------------------------------------------------------
    Vérifie que les actions dans tab sont uniquement des A, pour attente
    --------------------------------------------------------------------------------------------------------------------------------------------------------
    Retourne un booléen False s'il y a un élément différent de A, et True sinon
    """
    assert type(tab) == list
    for i in range(len(tab)):
        if tab[i]!='A':
            return False
    return True

def charger_donnees(fichier):
    """
    Prend en entrée un str indiquant le nom d'un fichier .txt ou .map
    --------------------------------------------------------------------------------------------------------------------------------------------------------
    Parcourt tout le dossier, ligne par ligne, et transforme le dossier en un tableau bi-dimensionnel, comportant des éléments clés à certains endroits
    --------------------------------------------------------------------------------------------------------------------------------------------------------
    Renvoie:
        un tableau bi-dimensionnel carte
        une liste incendies
        une liste robots
        un int pour la largeur d'une case
        un int pour la hauteur d'une case
        un int pour taille case
    """
    with open(fichier, 'r') as f:
        lignes = f.readlines()
    i = 0
    while lignes[i].strip().startswith("#"):
        i += 1
    dimensions = lignes[i].strip().split()
    largeur, hauteur, taille_case = int(dimensions[0]), int(dimensions[1]), int(dimensions[2])
    i += 1
    tableau = []
    for _ in range(hauteur):
        while lignes[i].strip().startswith("#") or lignes[i].strip() == "":
            i += 1
        ligne = []
        for _ in range(largeur):
            ligne.append(lignes[i].strip())
            i += 1
        tableau.append(ligne)
        i += 1

    carte = Carte(tableau, taille_case)
    while lignes[i].strip().startswith("#") or lignes[i].strip() == "":
        i += 1
    nb_incendies = int(lignes[i].strip())
    i += 1
    incendies = []
    for _ in range(nb_incendies):
        while lignes[i].strip().startswith("#") or lignes[i].strip() == "":
            i += 1
        x, y, eau = map(int, lignes[i].strip().split())
        incendies.append(Incendie((x, y), eau))
        carte.tableau[x][y].est_incendie = True
        carte.tableau[x][y].incendie = Incendie((x, y), eau)
        i += 1
    
    # Charger les robots
    while lignes[i].strip().startswith("#") or lignes[i].strip() == "":
        i += 1
    nb_robots = int(lignes[i].strip())
    i += 1
    robots = []
    for _ in range(nb_robots):
        while lignes[i].strip().startswith("#") or lignes[i].strip() == "":
            i += 1
        data = lignes[i].strip().split()
        x, y = map(int, data[:2])
        type_robot = data[2]
        if type_robot == "DRONE":
            vitesse = int(data[3]) if len(data) > 3 else 100
            # Permet de préciser une vitesse dans le fichier instructions
            robots.append(Drone((x, y), vitesse))
        elif type_robot == "ROUES":
            robots.append(Robot_a_Roues((x, y)))
        elif type_robot == "CHENILLES":
            robots.append(Robot_a_chenilles((x, y)))
        elif type_robot == "PATTES":
            robots.append(Robot_a_pattes((x, y)))
        i += 1
    assert type(carte) == Carte,"Problème sur la carte"
    assert type(robots) == list,"Problème sur la liste robots"
    assert type (incendies) == list,"Problème sur la liste incendies"
    assert type (taille_case) == int,"Problème sur le type de la taille de la case"
    return carte, incendies, robots, largeur, hauteur, taille_case

def afficher_carte(fenetre, carte, largeur):
    """
    Prend en entrée un objet de type carte, un int largeur et un argument fenetre pygame
    --------------------------------------------------------------------------------------------------------------------------------------------------------
    Permet de redimensionner les images des cartes puis de les afficher
    --------------------------------------------------------------------------------------------------------------------------------------------------------
    Ne renvoie rien, affiche juste une image de la carte
    """
    assert type(carte) == Carte,"Problème avec le type de carte"
    if largeur <= 10:
        TAILLE_CASE = 88
    elif largeur <= 20:
        TAILLE_CASE = 35
    else:
        TAILLE_CASE = 14

    for ligne in carte.tableau:
        for case in ligne:
            image = pygame.transform.scale(IMAGES[case.nature], (TAILLE_CASE, TAILLE_CASE))
            fenetre.blit(image, (case.longitude * TAILLE_CASE, case.lattitude * TAILLE_CASE))

def afficher_incendies(fenetre, incendies, largeur, carte):
    """
    Prend en entrée un argument fenetre de pygame, une liste incendies, un int largeur et un objet de type carte
    --------------------------------------------------------------------------------------------------------------------------------------------------------
    Permet d'afficher les incendies sur la carte
    --------------------------------------------------------------------------------------------------------------------------------------------------------
    Ne renvoie rien mais permet d'afficher les incendies de la liste incendies
    """
    assert type(carte) == Carte,"Problème avec le type de la carte"
    assert type(incendies) == list,"Problème avec la liste incendies"
    if len (incendies) <<0 :
        assert type(incendies[0] ) == Incendie,"Problème avec le type d'un incendie dans la liste incendies"
    if largeur <= 10:
        TAILLE_CASE = 88
    elif largeur <= 20:
        TAILLE_CASE = 35
    else:
        TAILLE_CASE = 14
    incendie_nouveau = []
    for j in range(len(carte.tableau)):
        for k in range(len(carte.tableau[0])):
            if carte.tableau[j][k].est_incendie:
                incendie_nouveau.append(carte.tableau[j][k].incendie)
    for incendie in incendie_nouveau:
        x, y = incendie.position
        image = pygame.transform.scale(IMAGES["INCENDIE"], (TAILLE_CASE, TAILLE_CASE))
        fenetre.blit(image, (y * TAILLE_CASE, x * TAILLE_CASE))

def afficher_robots(fenetre, robots, largeur):
    """
    Prend en entrée un argument fenetre de pygame, une liste robots, un int largeur
    --------------------------------------------------------------------------------------------------------------------------------------------------------
    Permet d'afficher les robots sur la carte
    --------------------------------------------------------------------------------------------------------------------------------------------------------
    Ne renvoie rien mais permet d'afficher les robots de la liste robots
    """
    if largeur <= 10:
        TAILLE_CASE = 88
    elif largeur <= 20:
        TAILLE_CASE = 35
    else:
        TAILLE_CASE = 14

    for robot in robots:
        if robot.action == 'L':
            x, y = robot.positions
            image = pygame.transform.scale(IMAGES[robot.nom + '_verser'], (TAILLE_CASE, TAILLE_CASE))
            fenetre.blit(image, (y * TAILLE_CASE, x * TAILLE_CASE))
            pygame.display.flip()
        else:
            x, y = robot.positions
            image = pygame.transform.scale(IMAGES[robot.nom], (TAILLE_CASE, TAILLE_CASE))
            fenetre.blit(image, (y * TAILLE_CASE, x * TAILLE_CASE))



#-----------------------------------------------------------------------------------------------------------------------------------------------------------    

class Menu:
    def __init__(self, fenetre, options, image_de_fond):
        """
        Prend en entrée un Menu, une fenetre de pygame, les options qui s'affichent sur l'écran et l'image de fond
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de définir les attributs d'un menu
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        self.fenetre = fenetre
        self.options = options
        self.choisi = 0
        self.police = pygame.font.Font(None, 50)
        self.fond = pygame.image.load(image_de_fond).convert_alpha()

    def dessiner(self):
        """
        Prend en entrée un Menu
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de dessiner les options d'un Menu sur l'image de fond
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        image = pygame.transform.scale(self.fond, (700, 700))
        self.fenetre.blit(image, (0, 0))
        for i, option in enumerate(self.options):
            couleur = BLANC if i == self.choisi else NOIR
            texte = self.police.render(option, True, couleur)
            rect = texte.get_rect(center=(700 // 2, 700 // 2 + i * 60))
            self.fenetre.blit(texte, rect)
            

    def gerer_event(self, event):
        """
        Prend en entrée un Menu et un évènement
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de connaître l'option choisi
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Renvoie l'indice de l'option choisi
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.choisi = (self.choisi + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.choisi = (self.choisi - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.choisi
            elif event.key == pygame.K_t:
                a = StickFigureWindow()
            return None

#-----------------------------------------------------------------------------------------------------------------------------------------------------------    

class choisir:
    def __init__(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de définir les attributs des choix sur le menu
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        pygame.init()
        self.fenetre = pygame.display.set_mode((700, 700))
        pygame.display.set_caption('Menu')
        self.clock = pygame.time.Clock()
        self.etat = 'menu_principal'
        self.menu_principal = Menu(self.fenetre, ['Suivre un scénario prédéfini',
                        'Jeu avec le vent', 'Jeu Solo'], 'images/menu_background.png')
        self.sous_menu = Menu(self.fenetre, ['carteSujet', 'desertOfDeath-20x20', 'mushroomOfHell-20x20',
                        'spiralOfMadness-50x50', 'Retour au choix du mode'], 'images/menu_background.png') 

    def lancer(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de lancer le menu avec les différents choix possibles
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.etat == 'menu_principal':
                    choix = self.menu_principal.gerer_event(event)
                    if choix is not None:
                        if choix == 0:
                            self.etat = 'sous_menu_sim'
                            print(f"Début du jeu avec le mode : {self.menu_principal.options[choix]}")
                        if choix == 1:
                            self.etat = 'sous_menu_vent'
                            print(f"Début du jeu avec le mode : {self.menu_principal.options[choix]}")
                        if choix == 2:
                            self.etat = 'sous_menu_solo'
                            print(f"Début du jeu avec le mode : {self.menu_principal.options[choix]}")
                           
                elif self.etat == 'sous_menu_sim':
                    choix = self.sous_menu.gerer_event(event)
                    if choix is not None:
                        if choix != 4:
                            self.lancer_simulation(choix)
                        self.etat = 'menu_principal'
                elif self.etat == 'sous_menu_vent':
                    choix = self.sous_menu.gerer_event(event)
                    if choix is not None:
                        if choix != 4:
                            self.lancer_jeu_vent(choix)
                        self.etat = 'menu_principal'
                elif self.etat == 'sous_menu_solo':
                    choix = self.sous_menu.gerer_event(event)
                    if choix is not None:
                        if choix != 4:
                            self.lancer_jeu_solo(choix)
                        self.etat = 'menu_principal'
                    

            if self.etat == 'menu_principal':
                self.menu_principal.dessiner()
            elif self.etat in ['sous_menu_sim', 'sous_menu_vent', 'sous_menu_solo']:
                self.sous_menu.dessiner()

            pygame.display.flip()
            self.clock.tick(30)


    def lancer_simulation(self, choix):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de lancer le premier mode de jeu : 'Suivre un scénario prédéfini'
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        print(f"Début de la simulation avec la carte : {self.sous_menu.options[choix]}")
        a = scenario(f"instructions/instructions_{self.sous_menu.options[choix]}.txt", self.sous_menu.options[choix])

    def lancer_jeu_vent(self, choix):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de lancer le deuxième mode de jeu : 'Jeu avec vent'
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        print(f"Début du jeu avec le vent avec la carte : {self.sous_menu.options[choix]}")
        a = jeux_avec_vent(self.sous_menu.options[choix], 1)

    def lancer_jeu_solo(self, choix):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de lancer le troisième mode de jeu : 'Jeu solo'
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        print(f"Début du jeu avec la carte : {self.sous_menu.options[choix]}")
        a = jeux_solo(self.sous_menu.options[choix])
        
def acceder(Carte, coordonnees):
    """
    Prend en entrée une Carte et un tuple coordonnees
    ----------------------------------------------------------------------------------------------------------------------------------------------------
    Permet d'accéder à la case d'une carte
    ----------------------------------------------------------------------------------------------------------------------------------------------------
    Renvoie la case présente aux coordonnees donnees en entrée sur la Carte
    """
    x, y = coordonnees
    return Carte.tableau[x][y]

#-----------------------------------------------------------------------------------------------------------------------------------------------------------    

class scenario:
    def __init__(self, fichier, Carte):
        """
        Prend en entrée un fichier instructions et une carte 
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de lancer les instructions du fichier sur la carte donnée en argument
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        carte, incendies, robots, largeur, hauteur, taille_case = charger_donnees('cartes/' + Carte + '.map')
        self.carte = carte
        self.taille = len(self.carte.tableau) * len(self.carte.tableau[0])
        self.incendies = incendies
        self.robots = robots
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_case = taille_case
        self.fenetre = pygame.display.set_mode((700,700))
        robots2 = robots.copy()
        nouveau_dico = self.lire_fichier(fichier, robots2)
        self.jouer(nouveau_dico)

    def lire_fichier(self, fichier, robots):
        """
        Prend en entrée le fichier instructions et les robots présents sur cette carte
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de charger les instructions du fichier dans un dictionnaire
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Renvoie un dictionnaire nouveau_dico contenant toutes les instructions du fichier
        """
        nouveau_dico = {}
        robots2 = robots.copy()
        with open(fichier, 'r') as f:
            lignes = f.readlines()
            for ligne in lignes:
                actions = ligne.strip().split(',')
                robot_nom = actions.pop(0)
                
                # Trouver le robot correspondant dans la liste par son nom
                found_robot = None
                for i, robot in enumerate(robots2):
                    if robot.nom == robot_nom:
                        found_robot = robot
                        del robots2[i]  # Supprimer ce robot de la liste pour éviter les doublons
                        break
                assert found_robot.nom in ["DRONE", "PATTES", "CHENILLES", "ROUES"]
                if found_robot:
                    nouveau_dico[found_robot] = {
                        'actions': actions,
                        'en_mouvement': False,
                        'action_effectuee': 0
                    }
                    
        return nouveau_dico

    def next(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet d'avancer d'un pas de temps
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        self.fenetre.fill((255, 255, 255))
        afficher_carte(self.fenetre, self.carte, self.largeur)
        afficher_incendies(self.fenetre, self.incendies, self.largeur, self.carte)
        afficher_robots(self.fenetre, self.robots, self.largeur)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def jouer(self, nouveau_dico):
        """
        Prend en entrée nouveau_dico, le dictionnaire contenant toutes les instructions
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet d'effectuer toutes les actions présents dans nouveau_dico
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        temps_par_actualisation = (self.taille_case * self.taille)/10000
        action_effectuee = 0
        clock = pygame.time.Clock()
        tempo = True
        verif = True
        while tempo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            while verif:
                keys = list(nouveau_dico.keys())
                newdico = {}
                for rob in keys:
                    temps = 0
                    rob.action = None
                    if nouveau_dico[rob]['action_effectuee'] == 1:
                        action_effectuee += 1
                    action = nouveau_dico[rob]['actions']
                    if not action: 
                        nouveau_dico[rob]['action_effectuee'] = 1
                        action_effectuee += 1
                        continue
                    while temps < temps_par_actualisation:
                        if not action or len (action) == 0:
                            nouveau_dico[rob]['action_effectuee'] = 1
                            action = ['A' for i in range(int(temps_par_actualisation + 1 - temps))]
                            action_effectuee -=1

                        action_actuelle = action.pop(0)
                        if action_actuelle == 'R':
                            tempo =  rob.remplissage(self.carte)
                            temps += tempo
                        elif action_actuelle == 'L':
                            case = acceder(self.carte, rob.positions)
                            tempo = rob.intervention(case)
                            rob.action = 'L'
                            temps += tempo
                        elif action_actuelle == 'A':
                            temps += 1
                        elif action_actuelle in ['S', 'N', 'E', 'O']:
                            tempo = rob.deplacement_direction(action_actuelle, self.carte)
                            temps += tempo
                    if temps > temps_par_actualisation:
                        temps_restant = temps - temps_par_actualisation 
                        attente  = ['A' for i in range(int(temps_restant))]
                        temporaire = []
                        for i in range(len(attente)):
                            temporaire.append('A')
                        for j in range(len(action)):
                            temporaire.append(action[j])
                        action = temporaire.copy()
                        

                    nouveau_dico[rob]={'action_effectuee': nouveau_dico[rob]['action_effectuee'] , 'actions' : action}
                nouveau_dico = nouveau_dico.copy()
                self.next()
                clock.tick(3)
                tempo = False
                verif = self.carte.checke_incendie()
                checke = 0
                liste_de_nouvelle_clefs = list(nouveau_dico.keys())
                for i in range (len(liste_de_nouvelle_clefs)):
                    a=checke_liste_de_A(nouveau_dico[liste_de_nouvelle_clefs[i]]['actions'])
                    if a :
                        checke+=1
                if checke == len(liste_de_nouvelle_clefs):
                    verif = False
        self.fenetre.fill((0, 0, 42))
        pygame.display.flip()
        time.sleep(3)
        jeu = choisir()
        jeu.lancer()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

class jeux_solo:
    def __init__(self,Carte):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Prend en entrée une carte et permet à l'utilisateur de jouer sur cette dernière
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        self.Carte = Carte
        carte, incendies, robots, largeur, hauteur, taille_case = charger_donnees('cartes/' + Carte + '.map')
        self.carte = carte
        self.music = MusicPlayer(["musique/this_is_the_end.mp3", "musique/day.mp3","musique/lofi.mp3", "musique/air_tranquille.mp3"])
        self.incendies = incendies
        self.robots = robots
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_case = taille_case
        self.fenetre = pygame.display.set_mode((700,700))
        robot_en_mouvement = {}
        for i in robots :
            robot_en_mouvement[i] = {'en_mouvement' : False, 'actions' : []}
        self.next()
        self.jouer_solo(robot_en_mouvement)


    def next(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet d'avancer d'un pas de temps
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        self.fenetre.fill((255, 255, 255))
        afficher_carte(self.fenetre, self.carte, self.largeur)
        afficher_incendies(self.fenetre, self.incendies, self.largeur, self.carte)
        afficher_robots(self.fenetre, self.robots, self.largeur)
        pygame.display.flip()


    def tour(self,nouveau_dico):
        """
        Prend en entrée nouveau_dico contenant toutes les instructions à effectuer
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet d'effectuer les instructions de nouveau_dico
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """        
        temps_par_actualisation = 240#int(self.carte.taille_case/len(self.carte.tableau))
        keys = list(nouveau_dico.keys())
        new_dico = {}
        for rob in keys:
            temps = 0
            rob.action = None
            if len(nouveau_dico[rob]['actions'])==0:
                action =  ['A' for i in range(int(temps_par_actualisation))]
                action = nouveau_dico[rob]['actions']
            else :
                action = nouveau_dico[rob]['actions']
            while temps < temps_par_actualisation:
                if not action or len (action) == 0:
                    nouveau_dico[rob]['en_mouvement'] = False
                    action = ['A' for i in range(int(temps_par_actualisation + 1 - temps))]
                    

                action_actuelle = action.pop(0)
                if action_actuelle == 'R':
                    tempo =  rob.remplissage(self.carte)
                    temps += tempo
                elif action_actuelle == 'L':
                    case = acceder(self.carte, rob.positions)
                    tempo = rob.intervention(case)
                    rob.action = 'L'
                    temps += tempo
                elif action_actuelle == 'A':
                    temps += 1
                elif action_actuelle in ['S', 'N', 'E', 'O']:
                    tempo = rob.deplacement_direction(action_actuelle, self.carte)
                    temps += tempo
            if temps > temps_par_actualisation:
                temps_restant = temps - temps_par_actualisation 
                attente  = ['A' for i in range(int(temps_restant))]
                temporaire = []
                for i in range(len(attente)):
                    temporaire.append('A')
                for j in range(len(action)):
                    temporaire.append(action[j])
                action = temporaire.copy()
            tempo_action = action.copy()
            tempo_temps = 0
            for k in range (len (tempo_action)):
                if tempo_action != "A":
                    tempo_action = False
                tempo_action = True
            if tempo_action:
                nouveau_dico[rob]['en_mouvement'] = False
            new_dico[rob]={'en_mouvement': nouveau_dico[rob]['en_mouvement'] , 'actions' : action}
        nouveau_dico = new_dico.copy()
        return nouveau_dico

    def restart(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de réinitialiser le jeu
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        a = jeux_solo(self.Carte)
            
    def jouer_solo(self, robot_en_mouvement):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de lancer le troisième mode de jeu : 'Jeu solo'
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        tour_en_cours = True
        robot_selectionne = self.robots[0]
        while tour_en_cours:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0]:
                        index = event.key - pygame.K_1
                        if index < len(robot_en_mouvement):
                            robot_selectionne = self.robots[index]
                            print(f"Robot sélectionné: {robot_selectionne}")
                    if event.key == pygame.K_r:
                        root = tk.Tk()
                        ProgressBarPopup(root,robot_selectionne.reservoir,robot_selectionne.reservoir_initial,robot_selectionne.nom)
                        root.mainloop()
                        print(robot_selectionne.reservoir)
                    if not robot_en_mouvement[robot_selectionne]['en_mouvement'] or robot_en_mouvement[robot_selectionne]['en_mouvement'] == None :
                        keys = pygame.key.get_pressed()
                        if keys[K_z]:
                            robot_en_mouvement[robot_selectionne]['actions'] .append("N")
                            print("Déplacement Nord")
                        elif keys[K_d]:
                            robot_en_mouvement[robot_selectionne]['actions'] .append("E")
                            print("Déplacement Est")
                        elif keys[K_q]:
                            robot_en_mouvement[robot_selectionne]['actions'].append("O")
                            print("Déplacement Ouest")
                        elif keys[K_s]:
                            robot_en_mouvement[robot_selectionne]['actions'].append('S')
                            print("Déplacement Sud")
                        if keys[K_RIGHT]:
                            robot_en_mouvement[robot_selectionne]['actions'].append("R")
                            print("Remplissage")
                        if keys[K_LEFT]:
                            robot_en_mouvement[robot_selectionne]['actions'].append("L")
                            print("Largage")
                    if event.key == pygame.K_DOWN:
                        tour_en_cours = False
                        print ('Fin de tour')
                    if event.key == pygame.K_UP :
                        self.restart()
                    if event.key == pygame.K_m:
                        jeu = choisir()
                        jeu.lancer()
                    if event.key == pygame.K_h:
                        RulesPopup()
                    if event.key == pygame.K_a:
                        AttributePopup(robot_selectionne)
                    if event.key == pygame.K_v:
                        MusicPlayerPopup(self.music)
        liste_robot = list(robot_en_mouvement.keys())
        for i in range (len(liste_robot)):
            if len(robot_en_mouvement[robot_selectionne]['actions']) >0:
                robot_en_mouvement[robot_selectionne]['en_mouvement'] = True
            else :
                robot_en_mouvement[robot_selectionne]['en_mouvement'] = False
        new_dico = self.tour(robot_en_mouvement)
        self.next()
        if self.carte.checke_incendie():
            self.jouer_solo(new_dico)
        else :
            pygame.quit()
            sys.exit()
            self.fenetre = pygame.display.set_mode((700,700))
            image = pygame.image.load('images/menu_background.png').convert_alpha()
            self.fenetre.blit(image,(700,700))
            time.sleep(30)
            jeu = choisir()
            jeu.lancer()
            



#-----------------------------------------------------------------------------------------------------------------------------------------------------------
class jeux_avec_vent :
    def __init__(self, Carte, difficulte):
        """
        Prend en entrée une carte et permet à l'utilisateur de jouer sur cette dernière avec un autre difficulté qui correspond à la vitesse de propagation du feu
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet d'initialiser les attributs de notre jeu avec le vent
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        self.Carte = Carte
        carte, incendies, robots, largeur, hauteur, taille_case = charger_donnees('cartes/' + Carte + '.map')
        self.carte = carte
        self.incendies = incendies
        self.music = MusicPlayer(["musique/this_is_the_end.mp3", "musique/day.mp3","musique/lofi.mp3", "musique/air_tranquille.mp3"])
        self.robots = robots
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_case = taille_case
        popup = DirectionPopup()
        self.direction_vent = popup.get_selected_direction()
        self.fenetre = pygame.display.set_mode((700,700))
        robot_en_mouvement = {}
        for i in robots :
            robot_en_mouvement[i] = {'en_mouvement' : False, 'actions' : []}
        self.difficulte = difficulte
        if self.difficulte == 3:
            self.force_vent = 150
        elif self.difficulte == 2 :
            self.force_vent = 100
        else :
            self.force_vent = 50
        self.next()
        self.jouer_solo(robot_en_mouvement)

    def initialisation_du_vent(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet d'initialiser le vent
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        tempo = rnt(1,100)
        liste_direction = ["N", "S", "E", "O"]
        liste_direction.remove(self.direction_vent)
        if tempo<25:
            temporaire_2 = rnt(1,3)
            self.direction_vent = liste_direction[temporaire_2 - 1]
            CompassPopup(self.direction_vent)    
        self.deplacement_vent()

    def deplacement_vent(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de définir le déplacement du vent
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        assert len(self.carte.tableau[0]) == len(self.carte.tableau)
        force_vent = self.force_vent
        for i in range (len(self.carte.tableau)-1):
            for j in range(len(self.carte.tableau[0])-1):
                variable_temporaire = rnt(1,100)
                proba_deplacement_vent  = force_vent/10
                if variable_temporaire <= proba_deplacement_vent:
                    case_temporaire = acceder(self.carte,(i,j))
                    if case_temporaire.est_incendie :
                        if self.direction_vent == "N":
                            new_case = acceder(self.carte,(i-1,j))
                            new_case.est_incendie = True
                            new_case.incendie = Incendie((i-1,j), 1000)
                            self.incendies.append(Incendie((i-1,j), 1000))
                        elif self.direction_vent == "S":
                            new_case = acceder(self.carte,(i+1,j))
                            new_case.est_incendie = True
                            new_case.incendie = Incendie((i+1,j), 1000)
                            self.incendies.append(Incendie((i+1,j), 1000))
                        elif self.direction_vent == "E":
                            new_case = acceder(self.carte,(i,j+1))
                            new_case.est_incendie = True
                            new_case.incendie = Incendie((i,j+1), 1000)
                            self.incendies.append(Incendie((i,j+1), 1000))
                        else :
                            new_case = acceder(self.carte,(i,j-1))
                            new_case.est_incendie = True
                            new_case.incendie = Incendie((i,j-1), 1000)
                            self.incendies.append(Incendie((i,j-1), 1000))

        
            

    def next(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet d'avancer d'un pas de temps
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        self.fenetre.fill((255, 255, 255))
        afficher_carte(self.fenetre, self.carte, self.largeur)
        afficher_incendies(self.fenetre, self.incendies, self.largeur, self.carte)
        afficher_robots(self.fenetre, self.robots, self.largeur)
        pygame.display.flip()


    def tour(self,nouveau_dico):
        """
        Prend en entrée nouveau_dico contenant toutes les instructions à effectuer
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet d'effectuer les instructions de nouveau_dico
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """ 
        temps_par_actualisation = int(self.carte.taille_case/len(self.carte.tableau))
        keys = list(nouveau_dico.keys())
        new_dico = {}
        for rob in keys:
            temps = 0
            rob.action = None
            if len(nouveau_dico[rob]['actions'])==0:
                action =  ['A' for i in range(int(temps_par_actualisation))]
                action = nouveau_dico[rob]['actions']
            else :
                action = nouveau_dico[rob]['actions']
            while temps < temps_par_actualisation:
                if not action or len (action) == 0:
                    nouveau_dico[rob]['en_mouvement'] = False
                    action = ['A' for i in range(int(temps_par_actualisation + 1 - temps))]
                    

                action_actuelle = action.pop(0)
                if action_actuelle == 'R':
                    tempo =  rob.remplissage(self.carte)
                    temps += tempo
                elif action_actuelle == 'L':
                    case = acceder(self.carte, rob.positions)
                    tempo = rob.intervention(case)
                    rob.action = 'L'
                    temps += tempo
                elif action_actuelle == 'A':
                    temps += 1
                elif action_actuelle in ['S', 'N', 'E', 'O']:
                    tempo = rob.deplacement_direction(action_actuelle, self.carte)
                    temps += tempo
            if temps > temps_par_actualisation:
                temps_restant = temps - temps_par_actualisation 
                attente  = ['A' for i in range(int(temps_restant))]
                temporaire = []
                for i in range(len(attente)):
                    temporaire.append('A')
                for j in range(len(action)):
                    temporaire.append(action[j])
                action = temporaire.copy()
            tempo_action = action.copy()
            tempo_temps = 0
            for k in range (len (tempo_action)):
                if tempo_action != "A":
                    tempo_action = False
                tempo_action = True
            if tempo_action:
                nouveau_dico[rob]['en_mouvement'] = False
            new_dico[rob]={'en_mouvement': nouveau_dico[rob]['en_mouvement'] , 'actions' : action}
        nouveau_dico = new_dico.copy()
        return nouveau_dico

    def restart(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de réinitialiser le jeu
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        a = jeux_avec_vent(self.Carte,self.difficulte)
            
    def jouer_solo(self, robot_en_mouvement):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de lancer le troisième mode de jeu : 'Jeu solo' mais avec cette fois l'extension vent en plus
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        tour_en_cours = True
        robot_selectionne = self.robots[0]
        while tour_en_cours:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0]:
                        index = event.key - pygame.K_1
                        if index < len(robot_en_mouvement):
                            robot_selectionne = self.robots[index]
                            print(f"Robot sélectionné: {robot_selectionne}")
                    if event.key == pygame.K_r:
                        root = tk.Tk()
                        ProgressBarPopup(root,robot_selectionne.reservoir,robot_selectionne.reservoir_initial,robot_selectionne.nom)
                        root.mainloop()
                        print(robot_selectionne.reservoir)
                    if not robot_en_mouvement[robot_selectionne]['en_mouvement'] or robot_en_mouvement[robot_selectionne]['en_mouvement'] == None :
                        keys = pygame.key.get_pressed()
                        if keys[K_z]:
                            robot_en_mouvement[robot_selectionne]['actions'].append("N")
                            print("Déplacement Nord")
                        elif keys[K_d]:
                            robot_en_mouvement[robot_selectionne]['actions'].append("E")
                            print("Déplacement Est")
                        elif keys[K_q]:
                            robot_en_mouvement[robot_selectionne]['actions'].append("O")
                            print("Déplacement Ouest")
                        elif keys[K_s]:
                            robot_en_mouvement[robot_selectionne]['actions'].append('S')
                            print("Déplacement Sud")
                        if keys[K_RIGHT]:
                            robot_en_mouvement[robot_selectionne]['actions'].append("R")
                            print("Remplissage")
                        if keys[K_LEFT]:
                            robot_en_mouvement[robot_selectionne]['actions'].append("L")
                            print("Largage")
                    if event.key == pygame.K_DOWN:
                        tour_en_cours = False
                        print ('Fin de tour')
                    if event.key == pygame.K_UP :
                        self.restart()
                    if event.key == pygame.K_m:
                        jeu = choisir()
                        jeu.lancer()
                    if event.key == pygame.K_h:
                        RulesPopup()
                    if event.key == pygame.K_a:
                        AttributePopup(robot_selectionne)
                    if event.key == pygame.K_b:
                        CompassPopup(self.direction_vent)
                    if event.key == pygame.K_v:
                        MusicPlayerPopup(self.music)
        liste_robot = list(robot_en_mouvement.keys())
        for i in range (len(liste_robot)):
            if len(robot_en_mouvement[robot_selectionne]['actions']) >0:
                robot_en_mouvement[robot_selectionne]['en_mouvement'] = True
            else :
                robot_en_mouvement[robot_selectionne]['en_mouvement'] = False
        new_dico = self.tour(robot_en_mouvement)
        self.initialisation_du_vent()
        self.next()
        if self.carte.checke_incendie():
            self.initialisation_du_vent()
            self.jouer_solo(new_dico)
        else :
            pygame.quit()
            sys.exit()
            self.fenetre = pygame.display.set_mode((700,700))
            image = pygame.image.load('images/menu_background.png').convert_alpha()
            self.fenetre.blit(image,(700,700))
            time.sleep(30)
            pygame.quit()
            sys.exit()
    


    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
             jeu = choisir()
             jeu.lancer()


