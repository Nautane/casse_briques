import pygame
import pygame.freetype
from constantes import COULEURS, RAYON_BALLE, XMIN, XMAX, YMIN, YMAX, TICK, LONGUEUR_BRIQUE, LARGEUR_BRIQUE, screen, myfont, width, jouer_son
from balle import Balle

bfont=pygame.freetype.SysFont("cambria",20)

class Brique:
    def __init__(self, x, y, vies = 1, couleur = COULEURS["BLANC"]):
        self.origx = x
        self.x = x
        self.origy = y
        self.y = y
        self.precdx = 0
        self.precdy = 0
        self.vie = vies
        self.vies_max = vies
        self.couleur = couleur
        self.longueur = LONGUEUR_BRIQUE
        self.largeur = LARGEUR_BRIQUE
        self.touchee = False
        self.tick = 0

    def en_vie(self):
        return self.vie > 0

    def afficher(self):
        if self.en_vie():
            couleur = (int(self.couleur[0]+(255-self.couleur[0])/self.vie),int(self.couleur[1]/self.vies_max*self.vie),int(self.couleur[2]/self.vies_max*self.vie))
            couleur_bord = (int(couleur[0]/5),int(couleur[1]/5),int(couleur[2]/5))
            if self.touchee:
                self.tick += TICK
                if self.tick < 1/6:
                    self.x = self.origx + int(width/1000)  
                elif self.tick < 1/3:
                    self.x = self.origx - int(width/1000) 
                else : 
                    self.x = self.origx
                    self.touchee = False
                    self.tick = 0
            pygame.draw.rect(screen, couleur, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, self.largeur))
            pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, self.largeur), 2)
            pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, int(self.largeur/3)), 2)
            pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, int(self.largeur/3*2)), 2)
            pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), int(self.longueur/3), int(self.largeur/3)), 2)
            pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), int(self.longueur/3*2), int(self.largeur/3)), 2)
            pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2+self.longueur/6), int(self.y-self.largeur/6)-1, int(self.longueur/3)+1, int(self.largeur/3)+1), 2)
            pygame.draw.rect(screen, couleur_bord, (int(self.x), int(self.y-self.largeur/6)-1, int(self.longueur/3), int(self.largeur/3)+1), 2)
            pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y+self.largeur/6)-1, int(self.longueur/3), int(self.largeur/3)+1), 2)     
            pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y+self.largeur/6)-1, int(self.longueur/3*2), int(self.largeur/3)+1), 2)   
            if self.vies_max > 1:
                texte, rect = myfont.render(str(self.vie), (255,255,255), size = LARGEUR_BRIQUE)
                rect.center = (self.x, self.y)
                screen.blit(texte, rect)

    def collision_balle(self, balle, prec):
        marge = self.largeur/2 + RAYON_BALLE
        dy = balle.y - self.y
        touche = False
        if balle.x >= self.x:
            dx = balle.x - (self.x + self.longueur/2 - self.largeur/2)
            if abs(dy) <= marge and dx <= marge:
                touche = True
                self.touchee = True
                if not(prec):
                    if self.precdx < abs(self.precdy):
                        balle.vy = -balle.vy
                    else:
                        balle.vx = -balle.vx
        else:
            dx = balle.x - (self.x - self.longueur/2 + self.largeur/2)
            if abs(dy) <= marge and -dx <= marge:
                touche = True
                self.touchee = True
                if not(prec):
                    if -self.precdx < abs(self.precdy):
                        balle.vy = -balle.vy
                    else:
                        balle.vx = -balle.vx
        self.precdy = dy
        self.precdx = dx
        if touche :
            self.vie -= 1
        return touche, self.en_vie()

    def type_de_brique(self):
        return "Brique"

    def __str__(self):
        return "Brique x: " + str(self.x) + " y: " + str(self.y)

class Brique_indestructible(Brique):
    def en_vie(self):
        return True

    def collision_balle(self, balle, prec):
        marge = self.largeur/2 + RAYON_BALLE
        dy = balle.y - self.y
        touche = False
        if balle.x >= self.x:
            dx = balle.x - (self.x + self.longueur/2 - self.largeur/2)
            if abs(dy) <= marge and dx <= marge:
                touche = True
                self.touchee = True
                if not(prec):
                    if self.precdx < abs(self.precdy):
                        balle.vy = -balle.vy
                    else:
                        balle.vx = -balle.vx
        else:
            dx = balle.x - (self.x - self.longueur/2 + self.largeur/2)
            if abs(dy) <= marge and -dx <= marge:
                touche = True
                self.touchee = True
                if not(prec):
                    if -self.precdx < abs(self.precdy):
                        balle.vy = -balle.vy
                    else:
                        balle.vx = -balle.vx
        self.precdy = dy
        self.precdx = dx
        return touche, self.en_vie()

    def afficher(self):
        couleur_bord = (int(self.couleur[0]/5),int(self.couleur[1]/5),int(self.couleur[2]/5))
        pygame.draw.rect(screen, self.couleur, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, self.largeur))
        pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, self.largeur), 2)
        pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, int(self.largeur/3)), 2)
        pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, int(self.largeur/3*2)), 2)
        pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), int(self.longueur/3), int(self.largeur/3)), 2)
        pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), int(self.longueur/3*2), int(self.largeur/3)), 2)
        pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2+self.longueur/6), int(self.y-self.largeur/6)-1, int(self.longueur/3)+1, int(self.largeur/3)+1), 2)
        pygame.draw.rect(screen, couleur_bord, (int(self.x), int(self.y-self.largeur/6)-1, int(self.longueur/3), int(self.largeur/3)+1), 2)
        pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y+self.largeur/6)-1, int(self.longueur/3), int(self.largeur/3)+1), 2)     
        pygame.draw.rect(screen, couleur_bord, (int(self.x-self.longueur/2), int(self.y+self.largeur/6)-1, int(self.longueur/3*2), int(self.largeur/3)+1), 2)   

    def type_de_brique(self):
        return "Brique_indestructible"
    
    def __str__(self):
        return "Brique indestructible x: "+str(self.x)+" y: "+str(self.y)