import pygame
import math
from constantes import COULEURS, RAYON_BALLE, XMIN, XMAX, YMIN, YMAX, FPS, width, screen, jouer_son
from raquette import Raquette

class Balle:
    def vitesse_par_angle(self, angle):
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def __init__(self):
        self.x, self.y = (400,400)
        self.vitesse = width/2.1/FPS
        self.vitesse_par_angle(60)
        self.sur_raquette = True
        self.loose = False
    
    def afficher(self):
        pygame.draw.rect(screen, COULEURS["BLANC"], (int(self.x-RAYON_BALLE), int(self.y-RAYON_BALLE),2*RAYON_BALLE, 2*RAYON_BALLE))
        #pygame.draw.circle(screen, COULEURS["BLANC"], (int(self.x), int(self.y)),RAYON_BALLE)
    
    def rebond_raquette(self, raquette):
        diff = raquette.x - self.x
        longueur_totale = raquette.longueur/2 + RAYON_BALLE
        angle = 90 + 80 * diff/longueur_totale
        self.vitesse_par_angle(angle)

    def deplacer(self, raquette):
        if self.sur_raquette:
            self.y = raquette.y - 2*RAYON_BALLE
            self.x = raquette.x
        else :
            self.x += self.vx
            self.y += self.vy
            if raquette.collision_balle(self) and self.vy > 0:
                self.rebond_raquette(raquette)
            if self.x + RAYON_BALLE > XMAX:
                self.vx = -self.vx
            if self.x - RAYON_BALLE < XMIN:
                self.vx = -self.vx
            if self.y + RAYON_BALLE > YMAX:
                self.sur_raquette = True
                self.loose = True
                jouer_son("perte_vie")
            if self.y - RAYON_BALLE < YMIN:
                self.vy = -self.vy
