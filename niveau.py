import pygame
import pygame.freetype
from constantes import *
from briques import *
from balle import Balle
from raquette import Raquette

class Niveau: 
    def __init__(self):
        self.en_cours = 1
        self.nombre_briques = 0
        self.brique_liste = []

    def creation_niveaux(self):
        self.brique_liste = []
        if self.en_cours == 1:
            #self.brique_liste.append(Brique(width/2,height/2, 3))
            self.brique_liste.append(Brique(width/2, height/2, 3))
        elif self.en_cours == 2:
            for i in range(int(XMIN + LONGUEUR_BRIQUE/2), int(XMAX - LONGUEUR_BRIQUE / 2), 3*LONGUEUR_BRIQUE):
                for j in range(int(YMIN + LARGEUR_BRIQUE/2), int(YMAX / 2), 2*LARGEUR_BRIQUE):
                    self.brique_liste.append(Brique(i + int(LONGUEUR_BRIQUE / 2), j + int(LARGEUR_BRIQUE / 2)))
        elif self.en_cours == 3 : 
            for i in range(int(XMIN + LONGUEUR_BRIQUE/2), int(XMAX - LONGUEUR_BRIQUE / 2), 2*LONGUEUR_BRIQUE):
                for j in range(int(YMIN + LARGEUR_BRIQUE/2), int(YMAX / 2), 2*LARGEUR_BRIQUE):
                    self.brique_liste.append(Brique(i , j + int(LARGEUR_BRIQUE / 2)))
        self.nombre_briques = 0
        for brique in self.brique_liste:
            if brique.type_de_brique != "Brique_indestructrible":
                    self.nombre_briques += 1

    def afficher(self):
        for brique in self.brique_liste:
            brique.afficher()
