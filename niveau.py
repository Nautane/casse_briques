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
                    self.brique_liste.append(Brique_indestructible(i + LONGUEUR_BRIQUE/2, j, 1, COULEURS["ANTHRACITE"]))
            for i in range(XMIN + 16*LONGUEUR_BRIQUE, XMIN + 17*LONGUEUR_BRIQUE, LONGUEUR_BRIQUE):
                for j in range(YMIN + 5*LARGEUR_BRIQUE, YMAX - 5*LARGEUR_BRIQUE, LARGEUR_BRIQUE):
                    self.brique_liste.append(Brique_indestructible(i + LONGUEUR_BRIQUE/2, j, 1, COULEURS["ANTHRACITE"]))
            for i in range(XMIN + 5*LONGUEUR_BRIQUE, XMAX - 7*LONGUEUR_BRIQUE, LONGUEUR_BRIQUE):
                for j in range(YMIN + 5*LARGEUR_BRIQUE, YMIN + 6*LARGEUR_BRIQUE, LARGEUR_BRIQUE):
                    self.brique_liste.append(Brique_indestructible(i + LONGUEUR_BRIQUE/2, j, 1, COULEURS["ANTHRACITE"]))
            for i in range(XMIN, XMAX-LONGUEUR_BRIQUE, LONGUEUR_BRIQUE):
                for j in range(YMIN + 17*LARGEUR_BRIQUE, YMIN + 18*LARGEUR_BRIQUE, LARGEUR_BRIQUE):
                    if not(XMIN + 5*LONGUEUR_BRIQUE < i < XMAX - 8*LONGUEUR_BRIQUE):
                        self.brique_liste.append(Brique_indestructible(i + LONGUEUR_BRIQUE/2, j, 1, COULEURS["ANTHRACITE"]))
            for i in range(XMIN + 6*LONGUEUR_BRIQUE, XMIN + 16*LONGUEUR_BRIQUE, LONGUEUR_BRIQUE*2):
                for j in range(YMIN + 6*LARGEUR_BRIQUE, YMAX - 5*LARGEUR_BRIQUE, LARGEUR_BRIQUE*2):
                    self.brique_liste.append(Brique(i + LONGUEUR_BRIQUE/2, j))
        elif self.en_cours == 2:
            for i in range(int(XMIN + LONGUEUR_BRIQUE*3), int(XMAX - LONGUEUR_BRIQUE*4), LONGUEUR_BRIQUE):
                for j in range(int(YMIN + LARGEUR_BRIQUE*3), int(YMAX / 3 * 2), LARGEUR_BRIQUE):
                    if XMIN + LONGUEUR_BRIQUE *8 < i < XMAX - LONGUEUR_BRIQUE*10 and YMIN + LARGEUR_BRIQUE*6 < j < YMAX - LARGEUR_BRIQUE*12:
                        self.brique_liste.append(Brique(i + LONGUEUR_BRIQUE/2  + LARGEUR_BRIQUE/2, j, 3, COULEURS["VERT"]))
                    elif XMIN + LONGUEUR_BRIQUE *4 < i < XMAX - LONGUEUR_BRIQUE*6 and YMIN + LARGEUR_BRIQUE*4 < j < YMAX - LARGEUR_BRIQUE*10:
                        self.brique_liste.append(Brique(i + LONGUEUR_BRIQUE/2  + LARGEUR_BRIQUE/2, j, 2, COULEURS["BLEU"]))
                    else:
                        self.brique_liste.append(Brique(i + LONGUEUR_BRIQUE/2  + LARGEUR_BRIQUE/2, j))
        elif self.en_cours == 3 : 
            for i in range(int(XMIN + LONGUEUR_BRIQUE/2), int(XMAX - LONGUEUR_BRIQUE / 2), 2*LONGUEUR_BRIQUE):
                for j in range(int(YMIN + LARGEUR_BRIQUE/2), int(YMAX / 2), 2*LARGEUR_BRIQUE):
                    self.brique_liste.append(Brique(i , j + int(LARGEUR_BRIQUE / 2)))
        self.nombre_briques = 0
        for brique in self.brique_liste:
            if brique.type_de_brique() != "Brique_indestructible":
                    self.nombre_briques += 1
        #self.nombre_briques = 1
    def afficher(self):
        for brique in self.brique_liste:
            brique.afficher()
