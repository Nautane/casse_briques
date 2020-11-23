import pygame
import pygame.freetype
from constantes import *
from balle import Balle

class Brique:
    def __init__(self, x, y, vies = 1, couleur = COULEURS["BLANC"]):
        self.x = x
        self.y = y
        self.vie = vies
        self.couleur = couleur
        self.longueur = LONGUEUR_BRIQUE
        self.largeur = LARGEUR_BRIQUE

    def en_vie(self):
        return self.vie > 0

    def afficher(self):
        if self.en_vie():
            if self.vie == 3 :
                pygame.draw.rect(screen, self.couleur, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, self.largeur))
            elif self.vie == 2 :
                pygame.draw.rect(screen, (int(self.couleur[0]/5*4), int(self.couleur[1]/5*2), int(self.couleur[2]/5*2)), (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, self.largeur))
            elif self.vie == 1 : 
                pygame.draw.rect(screen, COULEURS["ROUGE"], (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, self.largeur))
            pygame.draw.rect(screen, COULEURS["ANTHRACITE"], (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, self.largeur), 2)
            pygame.draw.rect(screen, COULEURS["ANTHRACITE"], (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, int(self.largeur/3)), 2)
            pygame.draw.rect(screen, COULEURS["ANTHRACITE"], (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, int(self.largeur/3*2)), 2)
            pygame.draw.rect(screen, COULEURS["ANTHRACITE"], (int(self.x-self.longueur/2), int(self.y-self.largeur/2), int(self.longueur/3), int(self.largeur/3)), 2)
            pygame.draw.rect(screen, COULEURS["ANTHRACITE"], (int(self.x-self.longueur/2), int(self.y-self.largeur/2), int(self.longueur/3*2), int(self.largeur/3)), 2)
            pygame.draw.rect(screen, COULEURS["ANTHRACITE"], (int(self.x-self.longueur/2+self.longueur/6), int(self.y-self.largeur/6)-1, int(self.longueur/3)+1, int(self.largeur/3)+1), 2)
            pygame.draw.rect(screen, COULEURS["ANTHRACITE"], (int(self.x), int(self.y-self.largeur/6)-1, int(self.longueur/3), int(self.largeur/3)+1), 2)
            pygame.draw.rect(screen, COULEURS["ANTHRACITE"], (int(self.x-self.longueur/2), int(self.y+self.largeur/6)-1, int(self.longueur/3), int(self.largeur/3)+1), 2)     
            pygame.draw.rect(screen, COULEURS["ANTHRACITE"], (int(self.x-self.longueur/2), int(self.y+self.largeur/6)-1, int(self.longueur/3*2), int(self.largeur/3)+1), 2)   

    def collision_balle(self, balle, prec):
        marge = self.largeur/2 + RAYON_BALLE
        dy = balle.y - self.y
        touche = False
        if balle.x > self.x:
            dx = balle.x - (self.x + self.longueur/2 - self.largeur/2)
            if abs(dy) <= marge and dx <= marge:
                touche = True
                if not(prec):
                    if dx < abs(dy):
                        balle.vy = -balle.vy
                    else:
                        balle.vx = -balle.vx
        else:
            dx = balle.x - (self.x - self.longueur/2 + self.largeur/2)
            if abs(dy) <= marge and -dx <= marge:
                touche = True
                if not(prec):
                    if -dx < abs(dy):
                        balle.vy = -balle.vy
                    else:
                        balle.vx = -balle.vx
        if touche :
            self.vie -= 1
        return touche and not(self.en_vie())

    def type_de_brique(self):
        print("Brique")

class Brique_indestructible(Brique):
    def __init__(self, x, y, vies = 1000,couleur = COULEURS["GRIS"]):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.vie = vies
        self.longueur = LONGUEUR_BRIQUE
        self.largeur = LARGEUR_BRIQUE
    
    def en_vie(self):
        return True

    def type_de_brique(self):
        print("Brique_indestructible")
