import pygame
from constantes import COULEURS, LONGUEUR_BRIQUE, LARGEUR_BRIQUE, XMIN, XMAX, YMIN, YMAX, width, height
from briques import Brique, Brique_indestructible
from raquette import Raquette

class Niveau: 
    def __init__(self):
        self.en_cours = 1
        self.nombre_briques = 0
        self.brique_liste = []

    def creation_niveaux(self):
        self.brique_liste = []
        if self.en_cours == 1:
            for i in range(XMIN + 5*LONGUEUR_BRIQUE, XMIN + 6*LONGUEUR_BRIQUE, LONGUEUR_BRIQUE):
                for j in range(YMIN + 5*LARGEUR_BRIQUE, YMAX - 5*LARGEUR_BRIQUE, LARGEUR_BRIQUE):
                    self.brique_liste.append(Brique(i + LONGUEUR_BRIQUE/2, j))
            for i in range(XMIN + 16*LONGUEUR_BRIQUE, XMIN + 17*LONGUEUR_BRIQUE, LONGUEUR_BRIQUE):
                for j in range(YMIN + 5*LARGEUR_BRIQUE, YMAX - 5*LARGEUR_BRIQUE, LARGEUR_BRIQUE):
                    self.brique_liste.append(Brique(i + LONGUEUR_BRIQUE/2, j))
            for i in range(XMIN + 5*LONGUEUR_BRIQUE, XMAX - 7*LONGUEUR_BRIQUE, LONGUEUR_BRIQUE):
                for j in range(YMIN + 5*LARGEUR_BRIQUE, YMIN + 6*LARGEUR_BRIQUE, LARGEUR_BRIQUE):
                    self.brique_liste.append(Brique(i + LONGUEUR_BRIQUE/2, j))
            for i in range(XMIN + 5*LONGUEUR_BRIQUE, XMAX - 7*LONGUEUR_BRIQUE, LONGUEUR_BRIQUE):
                for j in range(YMIN + 17*LARGEUR_BRIQUE, YMIN + 18*LARGEUR_BRIQUE, LARGEUR_BRIQUE):
                    self.brique_liste.append(Brique(i + LONGUEUR_BRIQUE/2, j))
            for i in range(XMIN + 6*LONGUEUR_BRIQUE, XMIN + 16*LONGUEUR_BRIQUE, LONGUEUR_BRIQUE*2):
                for j in range(YMIN + 6*LARGEUR_BRIQUE, YMAX - 6*LARGEUR_BRIQUE, LARGEUR_BRIQUE*2):
                    self.brique_liste.append(Brique(i + LONGUEUR_BRIQUE, j+LARGEUR_BRIQUE, 2, COULEURS["VERT"]))
        elif self.en_cours == 2:
            inc = 0
            for i in range(XMIN + int(LONGUEUR_BRIQUE*3/2), XMAX, LONGUEUR_BRIQUE*2):
                if inc % 2 == 1:
                    for j in range(YMIN + int(LARGEUR_BRIQUE*3/2), int(YMAX / 3 * 2), LARGEUR_BRIQUE):
                        self.brique_liste.append(Brique_indestructible(i  , j, 1, COULEURS["ANTHRACITE"]))
                else:    
                    for j in range(YMIN + int(LARGEUR_BRIQUE*3/2), int(YMAX / 3 * 2), LARGEUR_BRIQUE):
                        if inc < 1 :
                            self.brique_liste.append(Brique(i  , j))
                        elif inc < 3 :
                            self.brique_liste.append(Brique(i  , j, 2, COULEURS["CYAN"]))
                        elif inc < 5 :
                            self.brique_liste.append(Brique(i  , j, 3, COULEURS["BLEU"]))
                        elif inc < 7 :
                            self.brique_liste.append(Brique(i  , j, 3, COULEURS["BLEU"]))
                        elif inc < 9 :
                            self.brique_liste.append(Brique(i  , j, 2, COULEURS["CYAN"]))
                        elif inc < 11 :
                            self.brique_liste.append(Brique(i  , j))
                inc += 1
        elif self.en_cours == 3 : 
            for i in range(int(XMIN + LONGUEUR_BRIQUE/2), int(XMAX - LONGUEUR_BRIQUE / 2), 2*LONGUEUR_BRIQUE):
                for j in range(int(YMIN + LARGEUR_BRIQUE/2), int(YMAX / 2), 2*LARGEUR_BRIQUE):
                    self.brique_liste.append(Brique(i , j + int(LARGEUR_BRIQUE / 2)))
        self.nombre_briques = 0
        for brique in self.brique_liste:
            if brique.type_de_brique() != "Brique_indestructible":
                    self.nombre_briques += 1
    def afficher(self):
        for brique in self.brique_liste:
            brique.afficher()
