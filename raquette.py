import pygame
from constantes import COULEURS, RAYON_BALLE, XMIN, XMAX, YMIN, YMAX, TICK, ARC_EN_CIEL, FPS, screen

class Raquette:
    def __init__(self):
        self.x =(XMIN+XMAX)/2
        self.y = YMAX- RAYON_BALLE
        self.couleur = "BLANC"
        self.longueur = 10*RAYON_BALLE
        self.arc_en_ciel = False
        self.tick = 0
    
    def afficher(self):
        if self.arc_en_ciel:
            self.tick += TICK
            if self.tick >= 1/2:
                self.tick = 0
                self.arc_en_ciel = False
            self.couleur = ARC_EN_CIEL[int(self.tick*FPS*2)]
        else:
            self.couleur = COULEURS["BLANC"]
        pygame.draw.rect(screen, self.couleur, (int(self.x-self.longueur/2), int(self.y-RAYON_BALLE), self.longueur, 2*RAYON_BALLE), 0)
    
    def deplacer(self, x):
        if x-self.longueur/2 < XMIN :
            self.x = XMIN + self.longueur/2
        elif x + self.longueur/2 > XMAX :
            self.x = XMAX - self.longueur/2
        else :
            self.x = x

    def collision_balle(self, balle):
            vertical = abs(self.y - balle.y) < 2*RAYON_BALLE
            horizontal = abs(self.x - balle.x) < self.longueur/2 + RAYON_BALLE
            return vertical and horizontal
