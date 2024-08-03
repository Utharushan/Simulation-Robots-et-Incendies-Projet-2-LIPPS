class Carte:
    def __init__(self, tableau, taille_case):
        """
        Prend en entrée une matrice contenant le type de chaque case
        ---------------------------------------------------------------
        Crée un objet carte qui est une matrice de case
        ---------------------------------------------------------------
        """
        assert len(tableau) == len (tableau[0]) #On s'assure que la carte est carrée
        self.tableau = [[0 for _ in range(len(tableau[0]))] for _ in range(len(tableau))]
        for i in range(len(tableau)):
            for j in range(len(tableau[0])):
                nature = tableau[i][j]
                self.tableau[i][j] = Case((i, j), nature)
        self.taille_case = taille_case
        
    def acceder(self, coordonnees):
        """
        Prend en entrée un tuple de coordonnées (x,y)
        ---------------------------------------------------------------
        Retourne la case à ces coordonnées
        ---------------------------------------------------------------
        """
        x, y = coordonnees
        return self.tableau[x][y]
    
    def checke_incendie(self):
        """
        Ne prend en entrée que la carte
        ---------------------------------------------------------------
        Parcourt la matrice, case par case, pour vérifier s'il y a une case incendie
        ---------------------------------------------------------------
        Renvoie True s'il y a au moins un incendie
        Renvoie False sinon
        ---------------------------------------------------------------
        """
        for i in range (len(self.tableau)):
            for j in range (len(self.tableau[i])):
                if self.tableau[i][j].est_incendie:
                    return True
        return False

    def trouve_voisin(self, positions, direction):
        """
        Prend en entree un tuple de coordonnées nommé positions, et un str nommé direction
        ---------------------------------------------------------------
        Retourne le voisin dans la direction indiqué
        ---------------------------------------------------------------
        """
        x, y = positions
        assert direction in ["N","E","S","O"],"La direction n'est pas standard"
        if direction == "O":
            return self.acceder((x-1, y))
        elif direction == "E":
            return self.acceder((x+1, y))
        elif direction == "N":
            return self.acceder((x, y-1))
        elif direction == "S":
            return self.acceder((x, y+1))
        else:
            raise ValueError 

class Case:
    def __init__(self, coordonnees, nature, est_incendie = False):
        """
        Prend en entrée un tuple coordonees, un str nature et un booléen est_incendie
        ---------------------------------------------------------------
        Crée un objet case avec un attribut incendie qui crée une instance de la classe Incendie si nécessaire 
        ---------------------------------------------------------------
        """
        self.coordonnees = coordonnees
        self.nature = nature
        self.longitude = coordonnees[1]
        self.lattitude = coordonnees[0]
        self.est_incendie = est_incendie
        if est_incendie:
            self.incendie = Incendie(coordonnees, 1000)
        else :
            self.incendie = False

class Incendie:
    def __init__(self, position, nb_litre_eau):
        """
        Prend en entrée un tuple positions et un int nb_litre_eau
        ---------------------------------------------------------------
        Crée un objet incendie
        ---------------------------------------------------------------
        """
        self.position = position
        self.nb_litre_eau = nb_litre_eau

    def check_incendie(self):
        """
        ---------------------------------------------------------------
        Vérifie si un incendie existe réellement
        ---------------------------------------------------------------
        """
        if self.nb_litre_eau == 0:
            self = None

    def intervention(self, eau):
        """
        ---------------------------------------------------------------
        Permet au robot d'intervenir
        ---------------------------------------------------------------
        """
        self.nb_litre_eau = self.nb_litre_eau - eau
        if self.nb_litre_eau <= 0:
            self = None
