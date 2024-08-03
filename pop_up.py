import tkinter as tk
from tkinter import ttk
import math
from tkinter import Scale, Button, Listbox, END, Label
import pygame
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class CompassPopup:
    def __init__(self, direction):
        """
        Prend en entrée un str indiquant une direction
    ----------------------------------------------------------------------------------------------
        Crée une classe permettant d'afficher une boussole avec les dessins de tkinter 
    ----------------------------------------------------------------------------------------------
        """
        self.root = tk.Tk()
        self.root.title("Boussole")
        self.root.geometry("500x500")
        title = tk.Label(self.root, text = "Boussole", font = ("Helvetica", 18, "bold"))
        title.pack(pady=10)
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.draw_compass(direction)# Dessiner la boussole
        # Pour fermer la fenetre tkinter
        self.root.bind('<Return>', lambda event: self.close())
        self.root.bind('<b>', lambda event: self.close())
        self.root.after(2000, self.close)
        self.root.mainloop()
    
    def draw_compass(self, direction):
        """
        Prend en entrée un str de taille 1 indiquant une direction
    --------------------------------------------------------------------------------------------
        Permet de dessiner le compas sur un canevas tkinter defini au prealable
    --------------------------------------------------------------------------------------------
        """
        assert len(direction) == 1
        center_x, center_y = 200, 200# Donne les coordonées du centre et rayon de la boussole
        radius = 150
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="black", width=2)# Permet de dessiner le cercle de la boussole
        points = {"N": (center_x, center_y - radius), "E": (center_x + radius, center_y), "S": (center_x, center_y + radius), "W": (center_x - radius, center_y)}     
        for point, (x, y) in points.items():
            self.canvas.create_text(x, y, text=point, font=("Helvetica", 14, "bold"))
        angles = {"N": 0, "E": 90, "S": 180, "W": 270}# Angles pour les directions
        angle = math.radians(angles.get(direction, 0))# Nous donne l'angle 
        arrow_length = 100
        arrow_x = center_x + arrow_length * math.sin(angle)
        arrow_y = center_y - arrow_length * math.cos(angle)
        
        self.canvas.create_line(center_x, center_y, arrow_x, arrow_y, fill="red", width=3, arrow=tk.LAST)
    
    def close(self):
        """
        Permet de fermer automatiquement la fenetre tkinter
        """
        self.root.destroy()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProgressBarPopup:
    def __init__(self, root, reservoir, reservoir_initial, nom):
        """
        Prend en entrée root, un int correspondant au reservoir du robot, un int correspondant au reservoir initial,
        un str correspondant au type du robot
        ----------------------------------------------------------------------------------------------
        Crée une classe permettant d'afficher la proportion du reservoir du robot qui est rempli 
        ----------------------------------------------------------------------------------------------
        """
        self.root = root
        self.nom = nom
        self.reservoir = reservoir
        self.reservoir_initial = reservoir_initial
        self.create_widgets()

    def create_widgets(self):
        """"
        Prend en entrée l'objet tkinter
        ----------------------------------------------------------------------------------------------
        Crée le dessin correspondant au réservoir vide
        ----------------------------------------------------------------------------------------------
        """
        self.root.title(f"{self.nom} reservoir")
        if self.reservoir == 'Poudre':
            progress_pourcentage = 100
        else:
            progress_pourcentage = (self.reservoir / self.reservoir_initial) * 100
        self.canvas = tk.Canvas(self.root, width=300, height=50, bg="white")
        self.canvas.pack(pady=20)
        self.draw_pixel_art_progress_bar(progress_pourcentage)
        self.label = tk.Label(self.root, text=f"{progress_pourcentage:.2f}%")
        self.label.pack(pady=10)
        self.root.after(5000, self.root.destroy)

    def draw_pixel_art_progress_bar(self, pourcentage):
        """"
        Prend en entrée l'objet tkinter et pourcentage , un flottant
        ----------------------------------------------------------------------------------------------
        Crée le dessin correspondant à la barre bleue de la proportion d'eau présente 
        ----------------------------------------------------------------------------------------------
        """
        assert pourcentage <= 100
        assert pourcentage >= 0 
        taille_pixel = 10
        num_pixels = int((pourcentage / 100) * (300 // taille_pixel))
        for i in range(num_pixels):
            x0 = i * taille_pixel
            y0 = 0
            x1 = x0 + taille_pixel
            y1 = 50
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline="")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class RulesPopup:
    def __init__(self):
        """"
        Ne prend rien en entrée
        ----------------------------------------------------------------------------------------------
        Crée une fenetre pop up indiquant toutes les aides du jeu, les commandes.
        ----------------------------------------------------------------------------------------------
        """
        self.root = tk.Tk()
        rules  = [
    "1. Appuyez sur Z pour que le robot sélectionné aille au NORD.",
    "2. Appuyez sur D pour que le robot sélectionné aille à l'EST.",
    "3. Appuyez sur Q pour que le robot sélectionné aille à l'OUEST.",
    "4. Appuyez sur S pour que le robot sélectionné aille au SUD.",
    "5. Appuyez sur M pour retourner au menu.",
    "6. Appuyez sur R pour afficher le réservoir du robot selectionné.",
    "7. Appuyez sur flèche du haut pour réinitialiser la partie.",
    "8. Appuyez sur flèche du bas pour passer au tour suivant.",
    "9. Appuyez sur flèche de gauche pour verser de l'eau.",
    "10.Appuyez sur flèche de droite pour remplir le robot sélectionné.",
    "11. Appuyez sur A pour afficher les attributs du robot.",
    "12. Appuyez sur B pour afficher la boussole si vous êtes dans un jeu avec vent",
    "13. Après avoir donné une liste d'instructions au robot, vous devez attendre la fin de ses instructions.",
    "14. Appuyez sur V pour contrôler la musique. Gauche/Droite : Changer de musique, Haut/Bas : Volume, Espace : Pause"]
        self.root.title("Règles")
        self.root.geometry("1000x600")
        self.text_widget = tk.Text(self.root, wrap='word', font=("Helvetica", 14))
        self.text_widget.pack(expand=True, fill='both')
        for rule in rules:
            self.text_widget.insert(tk.END, rule + '\n\n')
        self.text_widget.configure(state='disabled')
        self.root.bind("<Return>", self.close)
        self.root.mainloop()

    def close(self, event):
        self.root.destroy()

    


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class DirectionPopup:
    def __init__(self):
        """"
        Ne prend rien en entrée 
        ----------------------------------------------------------------------------------------------
        Crée le dessin d'une boussole et permet au joueur de decider de la direction initiale du vent
        ----------------------------------------------------------------------------------------------
        """
        self.root = tk.Tk()
        self.root.title("Choisir une direction")
        self.root.geometry("400x400")
        self.directions = [("Nord", "N"), ("Est", "E"), ("Sud", "S"), ("Ouest", "O")]
        self.current_index = 0
        self.selected_direction = None
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='white')
        self.canvas.pack(fill='both', expand=True)
        self.draw_compass()# Lance la fonction pour dessiner la boussole
        self.labels = []
        for direction, _ in self.directions:
            label = tk.Label(self.root, text=direction, font=("Helvetica", 24))
            self.labels.append(label)
        #on positionne les points cardinaux de la boussole
        self.labels[0].place(relx=0.5, rely=0.2, anchor='center')  # Nord
        self.labels[1].place(relx=0.8, rely=0.5, anchor='center')  # Est
        self.labels[2].place(relx=0.5, rely=0.8, anchor='center')  # Sud
        self.labels[3].place(relx=0.2, rely=0.5, anchor='center')  # Ouest
        self.update_labels()
        # Cette partie de la fonction sert a lier les touches directionnelles et la touche Entrée aux fonctions associe 
        self.root.bind("<Up>", self.up)
        self.root.bind("<Down>", self.down)
        self.root.bind("<Left>", self.left)
        self.root.bind("<Right>", self.right)
        self.root.bind("<Return>", self.select)
        self.root.mainloop()
    
    def draw_compass(self):
        # Cette fonction definie le centre de la boussole
        center_x = 200
        center_y = 200
        radius = 150
        # Dessiner le cercle de la boussole
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="black", width=2)
        # Dessiner les lignes des points cardinaux
        self.canvas.create_line(center_x, center_y - radius, center_x, center_y + radius, fill="black", width=2)  # Nord-Sud
        self.canvas.create_line(center_x - radius, center_y, center_x + radius, center_y, fill="black", width=2)  # Ouest-Est
    
    def update_labels(self):
        """
        Cette fonction permet de mettre a jour l'emplacement du choix de l'utilisateur, en rendant les choix actuels entourés de noir.
        """
        for i, label in enumerate(self.labels):
            if i == self.current_index:
                label.config(fg="white", bg="black")
            else:
                label.config(fg="black", bg="white")

    #les fonctions suivantes permettent d'initialiser les mouvement sur la boussole
    def up(self, event):
        self.current_index = 0  # Nord
        self.update_labels()
    
    def down(self, event):
        self.current_index = 2  # Sud
        self.update_labels()
    
    def left(self, event):
        self.current_index = 3  # Ouest
        self.update_labels()
    
    def right(self, event):
        self.current_index = 1  # Est
        self.update_labels()
    
    def select(self, event):
        """
        Cette fonction prend en entrée l'objet de la classe et le principe event indiquant que l'élément actuel a été choisi.
        Elle détruit également la fenetre tkinter. 
        """
        self.selected_direction = self.directions[self.current_index][1]
        self.root.destroy()
    
    def get_selected_direction(self):
        #Cette fonction renvoit la direction ainsi calculer
        return self.selected_direction

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class AttributePopup:
    def __init__(self, obj):
        self.root = tk.Tk()
        self.root.title(f"Attributs de {obj.__class__.__name__}")
        self.root.geometry("500x700")# Permet de definir la taille de la fenetre.
        title = tk.Label(self.root, text=f"Attributs de {obj.__class__.__name__}", font=("Helvetica", 18, "bold"))
        title.pack(pady=10)
        attr_frame = ttk.LabelFrame(self.root, text="Attributs")# création d'un cadre pour les attributs
        attr_frame.pack(fill="both", expand="yes", padx=20, pady=10)
        row = 0
        for attr, value in vars(obj).items():
            attr_name = attr.replace('_', ' ').title()# Remplacer les underscores par des espaces et capitaliser chaque mot
            # Ajouter des unités spécifiques de physique :) pour chaque attribut( m/s , s , L ou bien pourcentage)
            if 'vitesse' in attr.lower():
                value = f"{value} m/s"
            elif 'reservoir' in attr.lower():
                value = f"{value} Litre"
            elif 'duree' in attr.lower():
                value = f"{value} s"
            elif 'nerf' in attr.lower():
                value = f"{value} %"
            # Cette partit du code permet d'afficher le cote de l'attribut 
            attr_label = tk.Label(attr_frame, text=f"{attr_name}:", font=("Helvetica", 14))
            attr_label.grid(row=row, column=0, sticky='w', padx=10, pady=5)
            # Quand a celle-ci, elle affiche les valeurs des attributs.
            value_label = tk.Label(attr_frame, text=f"{value}", font=("Helvetica", 14))
            value_label.grid(row=row, column=1, sticky='w', padx=10, pady=5)
            row += 1
        close_button = tk.Button(self.root, text="Fermer", command=self.root.destroy)
        close_button.pack(pady=10)
        # Onassocie les touches 'a' et 'Entrée' à la fermeture de la fenêtre
        self.root.bind('<Return>', self.close)
        self.root.bind('<a>', self.close)
        self.root.mainloop()
    def close(self, event):
        """
        Cette fonction est la même pour tous les pop up, elle permet de fermer la fenetre.
        Cependant , elle diffère dans ce qu'elle prend en compte c'est pourquoi nous n'avons pas utilisé de classe supérieure à toutes les fenetres pop up.
        """
        self.root.destroy()




#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class MusicPlayer:
    def __init__(self, initial_musique_list, initial_volume=0.5):
        """"
        Prend en entrée une liste initial_musique_liste, une liste de str, et peut prendre en entrée un flottant correspondant au volume.
        ----------------------------------------------------------------------------------------------
        Crée le dessin correspondant au réservoir vide
        ----------------------------------------------------------------------------------------------
        """
        assert type(initial_musique_list) == list
        assert type (initial_musique_list[0]) == str
        assert type  (initial_volume) == float
        self.musique_list = initial_musique_list
        self.musique_index = 0
        self.volume = initial_volume
        pygame.init()
        pygame.mixer.init()
        if self.musique_list:
            self.load_musique()
        
    
    def load_musique(self):
        """"
        Prend en entrée l'objet de la classe créé
        ----------------------------------------------------------------------------------------------
        Permet de charger la musique correspondant a l'index défini, initial
        Ou alors modifié lors d'un appel de fonction.
        ----------------------------------------------------------------------------------------------
        """
        pygame.mixer.music.load(self.musique_list[self.musique_index])
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loops=-1)  # -1 pour jouer en boucle infinie
    
    def set_volume(self, volume):
        """"
        Prend en entrée l'objet créé ainsi qu'un flottant correspondant à un nouveau volume.
        ----------------------------------------------------------------------------------------------
        Permet de modifier le volume de la musique. 
        ----------------------------------------------------------------------------------------------
        """
        self.volume = max(0.0, min(1.0, volume))#permet de s'assurer que le volume reste un floatant et ne depasse pas 1.
        pygame.mixer.music.set_volume(self.volume)
    
    def stop_musique(self):#Permet de arreter la musique
        pygame.mixer.music.stop()
    
    def pause_musique(self):#Permet de soit mettre en pause la musique , ou bien si elle l'est deja , de la remettre en route.
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    
    def next_musique(self):#Permet de passer à la musique suivante selon l'indexe, appele la fonction load
        self.musique_index = (self.musique_index + 1) % len(self.musique_list)
        self.load_musique()
    
    def previous_musique(self):#Permet de passer à la musique précédante selon l'indexe, appele la fonction load
        self.musique_index = (self.musique_index - 1) % len(self.musique_list)
        self.load_musique()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class MusicPlayerPopup:
    def __init__(self, musique_player):
        """"
        Prend en entrée l'objet musique_player
        ----------------------------------------------------------------------------------------------
        Initialise les controles pour modifier le volume de la musiqque(fleche haut et bas),
        pour changer de chanson(fleches gauche et droite) et pour stopper la musique(espace).
        ----------------------------------------------------------------------------------------------
        """
        self.musique_player = musique_player
        self.root = tk.Tk()
        self.root.title("Lecture de musique")
        self.pause_button = Button(self.root, text="Espace pour Pause", command=self.toggle_pause)
        self.pause_button.pack(pady=10)
        
        # Titre de la musique en cours de lecture
        self.current_musique_label = Label(self.root, text="Musique en cours : " + self.musique_player.musique_list[self.musique_player.musique_index])
        self.current_musique_label.pack(padx=20, pady=10)
        #On parametres les touches
        self.root.bind("<space>", lambda event: self.toggle_pause())
        self.root.bind("<Up>", lambda event: self.adjust_volume(0.1))
        self.root.bind("<Down>", lambda event: self.adjust_volume(-0.1))
        self.root.bind("<Left>", lambda event: self.musique_player.previous_musique())
        self.root.bind("<Right>", lambda event: self.musique_player.next_musique())
        self.root.mainloop()
    
    def toggle_pause(self):
        #permet de definir l'evenement pause de la musique pour un bouton ou bien pour la touche espace
        self.musique_player.pause_musique()
        if pygame.mixer.music.get_busy():
            self.pause_button.configure(text="Espace pour Pause")
        else:
            self.pause_button.configure(text="Espace pour Reprendre")
    
    def adjust_volume(self, increment):
        # Permet d'ajuster le volume de la musique
        new_volume = self.musique_player.volume + increment
        self.musique_player.set_volume(new_volume)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class StickFigureWindow:
    def __init__(self):
        """
        Surprise :)
        """
        self.root = tk.Tk()
        self.root.title("Stick Figures")
        self.root.geometry("800x400")
        label_hello = tk.Label(self.root, text="print('Hello world')", font=("Arial", 16))
        label_hello.pack(pady=20)
        frame_figures = tk.Frame(self.root)
        frame_figures.pack(pady=20)
        label_tristan = tk.Label(frame_figures, text="Tristan le goat", font=("Arial", 10))
        label_tristan.grid(row=1, column=1)
        canvas_tristan = tk.Canvas(frame_figures, width=100, height=200)
        canvas_tristan.grid(row=0, column=1)
        self.draw_stick_figure(canvas_tristan)
        label_tharushan = tk.Label(frame_figures, text="Tharushan le boss", font=("Arial", 10))
        label_tharushan.grid(row=1, column=2)
        canvas_tharushan = tk.Canvas(frame_figures, width=100, height=200)
        canvas_tharushan.grid(row=0, column=2)
        self.draw_stick_figure(canvas_tharushan)
        self.root.after(10000, self.close_window)  
        self.root.mainloop()
    
    def draw_stick_figure(self, canvas):
        canvas.create_oval(30, 10, 70, 50, outline="black", width=2)
        canvas.create_line(50, 50, 50, 120, fill="black", width=2)
        canvas.create_line(50, 70, 20, 90, fill="black", width=2)
        canvas.create_line(50, 70, 80, 90, fill="black", width=2)
        canvas.create_line(50, 120, 20, 170, fill="black", width=2)
        canvas.create_line(50, 120, 80, 170, fill="black", width=2)
    
    def close_window(self):
        self.root.destroy()
