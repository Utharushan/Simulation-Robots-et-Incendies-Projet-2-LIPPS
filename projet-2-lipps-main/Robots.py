from incendie__carte_case import *

class Robot:
    def __init__(self, positions):
        """
        Prend en entrée un tuple positions
        ---------------------------------------------------------------
        Crée une instance robot qui servira surtout pour l'héritage
        ---------------------------------------------------------------
        """
        self.positions = positions 

    def connaitre_vitesse(self, carte):
        """
        Prend en entrée un robot et un objet carte
        ---------------------------------------------------------------
        Récupère la position du robot, puis regarde la nature de la case
        Calcule ensuite la vitesse du robot en fonction de la nature de la case
        ---------------------------------------------------------------
        Retourne un int ou un float
        """
        taille_case = carte.taille_case
        nature = acceder(carte, self.positions).nature
        assert nature in ["EAU",'TERRAIN_LIBRE',"ROCHE","FORET","HABITAT"],"Mauvaise nature"
        if nature in self.terrain_deplacement_possible:
            return taille_case / (self.vitesse / 3.6)  # Convertir vitesse en m/s
        elif nature in self.terrain_deplacement_complique:
            return taille_case / ((self.vitesse * self.nerf) / 3.6)
        elif nature in self.terrain_deplacement_impossible:
            print("Déplacement impossible sur cette case")
            return 0

    def intervention(self, case):
        """
        Prend en entrée un robot et une case
        ---------------------------------------------------------------
        Vérifie si la case est incendiée et si le robot a assez d'eau
        Puis soustrait au feu la quantité d'eau nécessaire
        ---------------------------------------------------------------
        Retourne un int correspondant au temps nécessaire
        """
        if not case.est_incendie: #Vérifie s'il y a un incendie sur la case 
            print("Pas d'incendie sur cette case")
            return 0
        if self.reservoir == 0:
            print("Réserve d'eau vide")
            return 600  # 10 minutes de pénalités
        if self.reservoir == "Poudre":
            temps_intervention = case.incendie.nb_litre_eau / self.duree_extinction
            case.incendie = None
            case.est_incendie = False
        else:
            temps_intervention = min(self.reservoir / self.duree_extinction, case.incendie.nb_litre_eau / self.duree_extinction)
            if self.reservoir >= case.incendie.nb_litre_eau:
                self.reservoir -= case.incendie.nb_litre_eau
                case.incendie = None
                case.est_incendie = False
            else:
                case.incendie.nb_litre_eau -= self.reservoir
                self.reservoir = 0
                self.rempli = False

        print("Intervention effectuée")
        return temps_intervention

    def remplissage(self, carte):
        """
        Prend en entrée un robot et une carte
        ---------------------------------------------------------------
        Vérifie si la case est jouxtante à l'eau afin se remplir, sinon renvoie une erreur
        ---------------------------------------------------------------
        Retourne un int correspondant au temps nécessaire
        """
        if self.reservoir == "Poudre":
            print("Non nécessaire")
            return 0
            
        coordonnees = self.positions
        biome = [carte.trouve_voisin(coordonnees, d).nature for d in ["N", "S", "E", "O"]]
        if "EAU" in biome:
            self.reservoir = self.reservoir_initial
            print(f"Remplissage effectué {self.nom}")
            return self.duree_remplissage
        else:
            print(f"Remplissage impossible, pas de source d'eau à proximité {self.nom}")
            return 0

    def deplacement_direction(self, direction, carte):
        """
        Prend en entrée un robot, une carte et une direction (str)
        ---------------------------------------------------------------
        Prend la direction, vérifie si le deplacement est possible, puis modifie les coordonnées du robot
        ---------------------------------------------------------------
        Retourne un int correspondant au temps nécessaire
        """
        directions = {
            "O": (0, -1), "E": (0, 1), "S": (1, 0), "N": (-1, 0)
        }
        new_positions = (self.positions[0] + directions[direction][0], self.positions[1] + directions[direction][1])
        case = acceder(carte, new_positions)
        if not case or case.nature in self.terrain_deplacement_impossible:#assert indiquant si le deplacement est possible ou pas 
            print("Déplacement impossible")
            return 0
        self.positions = new_positions
        tempo =  self.connaitre_vitesse(carte)
        assert type(tempo) == int or type (tempo) == float
        return tempo
     
def acceder(carte, coordonnees):
        x, y = coordonnees
        if x > len (carte.tableau[0])-1 or y> len(carte.tableau[0])-1 or x<0 or y<0:#assert permettant de verifier que la case a acceder est dans le tableau 
            return False
        else :
            return carte.tableau[x][y]
 
#-----------------------------------------------------------------------------------------------------------------------------------

class Drone(Robot):
    def __init__(self, positions, vitesse = 100, reservoir = 10000,
                 duree_remplissage = 1800, duree_extinction = 334, rempli = True):
        """
        ---------------------------------------------------------------
        Permet de définir les attributs du robot de type DRONE
        ---------------------------------------------------------------
        """
        self.positions = positions
        assert vitesse <= 150,"Vitesse trop élevée"
        self.nom = "DRONE"
        self.vitesse = vitesse
        self.reservoir = reservoir
        self.action = None
        self.duree_remplissage = duree_remplissage # En secondes
        self.duree_extinction = duree_extinction # En litre/seconde
        self.terrain_deplacement_possible = ["EAU", "HABITAT", "FORET", "ROCHE", "TERRAIN_LIBRE"]
        self.terrain_deplacement_complique = []
        self.terrain_deplacement_impossible = []
        self.nerf = None
        assert type(reservoir)==int
        self.reservoir_initial  = reservoir
        self.rempli = rempli
        if rempli:
            self.reservoir = reservoir
        else:
            self.reservoir = 0

    def remplissage(self, Carte):
        """
        Prend en entrée un robot et une carte
        ---------------------------------------------------------------
        Vérifie si le robot est sur une case Eau, sinon renvoie 0
        ---------------------------------------------------------------
        Retourne un int correspondant au temps de remplissage nécessaire
        """
        coordonnees = self.positions
        Case_actuelle = Carte.acceder(coordonnees)
        if Case_actuelle.nature == "EAU":
            self.reservoir = self.reservoir_initial
            print("Remplissage effectué DRONE")
            return self.duree_remplissage
        else:
            print("Remplissage impossible, pas de source d'eau à proximité DRONE")#assert que le drone peut se remplir 
            return 0

class Robot_a_Roues(Robot):
    def __init__(self, positions, vitesse = 80, reservoir = 5000,
                 duree_remplissage = 600, duree_extinction = 20, rempli = True):
        """
        ---------------------------------------------------------------
        Permet de définir les attributs du robot de type ROUES
        ---------------------------------------------------------------
        """
        self.nom = "ROUES"
        self.positions = positions
        self.vitesse = vitesse
        self.reservoir = reservoir
        assert type(duree_remplissage)==int
        assert type(duree_extinction) == int
        self.action = None
        self.duree_remplissage = duree_remplissage # En secondes
        self.duree_extinction = duree_extinction # En litre/seconde
        self.terrain_deplacement_possible = ["HABITAT", "TERRAIN_LIBRE"]
        self.terrain_deplacement_complique = []
        self.terrain_deplacement_impossible = ["FORET", "ROCHE", "EAU"]
        self.nerf = None
        self.rempli = rempli
        self.reservoir_initial  = reservoir
        if rempli:
            self.reservoir = reservoir
        else:
            self.reservoir = 0

class Robot_a_chenilles(Robot):
    def __init__(self, positions, vitesse = 60, reservoir = 2000,
                 duree_remplissage = 300, duree_extinction = 12.5, rempli = True):
        """
        ---------------------------------------------------------------
        Permet de définir les attributs du robot de type CHENILLES
        ---------------------------------------------------------------
        """
        self.nom = "CHENILLES"
        self.positions = positions
        assert vitesse <= 80,'Vitesse trop élevée'
        self.action = None
        self.vitesse = vitesse
        self.reservoir = reservoir
        self.duree_remplissage = duree_remplissage # En secondes
        self.duree_extinction = duree_extinction # En litre/seconde
        self.terrain_deplacement_possible = ["HABITAT", "TERRAIN_LIBRE"]
        self.terrain_deplacement_complique = ["FORET"]
        self.terrain_deplacement_impossible = ["ROCHE", "EAU"]
        self.nerf = 0.5
        self.reservoir_initial  = reservoir
        self.rempli = rempli
        if rempli:
            self.reservoir = reservoir
        else:
            self.reservoir = 0

class Robot_a_pattes(Robot):
    def __init__(self, positions, vitesse = 30, reservoir = "Poudre",
                 duree_extinction = 10, rempli = True):
        """
        ---------------------------------------------------------------
        Permet de définir les attributs du robot de type PATTES
        ---------------------------------------------------------------
        """
        self.nom = "PATTES"
        self.positions = positions
        self.vitesse = vitesse
        self.reservoir = reservoir
        self.action = None
        self.reservoir_initial  = reservoir # En secondes
        self.duree_extinction = duree_extinction # En litre/seconde
        self.terrain_deplacement_possible = ["HABITAT", "TERRAIN_LIBRE", "FORET"]
        self.terrain_deplacement_complique = ["ROCHE"]
        self.terrain_deplacement_impossible = ["EAU"]
        self.nerf = 1/3
        self.rempli = rempli
        if rempli:
            self.reservoir = reservoir
        else:
            self.reservoir = 0
