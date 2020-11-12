from mss import mss
import random
import sys
import pygame
import pygame.freetype
import math

pygame.init()

pygame.freetype.init()
myfont=pygame.freetype.SysFont("arialblack",20)

width, height = int(mss().monitors[1]["width"]/4*3), int(mss().monitors[1]["height"]/4*3)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ping")

FPS = 144
clock = pygame.time.Clock()

BLANC = (255,255,255)
NOIR = (0,0,0)

NOMBRE_NIVEAUX = 2
NOMBRE_VIES = 6
RAYON_BALLE = int(mss().monitors[1]["width"]/200)
XMIN, YMIN = int(width/20) , int(width/20)
XMAX , YMAX = int(width - width/20), height

class Balle:
    def vitesse_par_angle(self, angle):
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def __init__(self):
        self.x, self.y = (400,400)
        self.vitesse = 500/FPS
        self.vitesse_par_angle(60)
        self.sur_raquette = True
        self.loose = False
    
    def afficher(self):
        pygame.draw.rect(screen, BLANC, (int(self.x-RAYON_BALLE), int(self.y-RAYON_BALLE),2*RAYON_BALLE, 2*RAYON_BALLE), 0)
    
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
            if self.y - RAYON_BALLE < YMIN:
                self.vy = -self.vy

class Raquette:
    def __init__(self):
        self.x =(XMIN+XMAX)/2
        self.y = YMAX- RAYON_BALLE
        self.longueur = 10*RAYON_BALLE
    
    def afficher(self):
        pygame.draw.rect(screen, BLANC, (int(self.x-self.longueur/2), int(self.y-RAYON_BALLE), self.longueur, 2*RAYON_BALLE), 0)
    
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

class Brique:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 1
        self.longueur = 5 * RAYON_BALLE
        self.largeur = 3 * RAYON_BALLE

    def en_vie(self):
        return self.vie > 0

    def afficher(self):
        pygame.draw.rect(screen,BLANC, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, self.largeur), 0)

    def collision_balle(self, balle):
        marge = self.largeur/2 + RAYON_BALLE
        dy = balle.y - self.y
        touche = False
        if balle.x > self.x:
            dx = balle.x - (self.x + self.longueur/2 - self.largeur/2)
            if abs(dy) < marge and dx < marge:
                touche = True
                if dx <= abs(dy):
                    balle.vy = -balle.vy
                else:
                    balle.vx = -balle.vx
        else:
            dx = balle.x - (self.x - self.longueur/2 + self.largeur/2)
            if abs(dy) < marge and -dx < marge:
                touche = True
                if -dx <= abs(dy):
                    balle.vy = -balle.vy
                else:
                    balle.vx = -balle.vx
        if touche:
            self.vie -= 1
        return touche
        """margex = self.longueur/2
        margey = self.largeur/2
        if self.x - margex <= balle.x <= self.x + margex : 
            if self.y - margey <= balle.y <= self.y + margey:
                self.vie -=1
                if int(abs(self.x - balle.x)*3/5) < abs(self.y - balle.y):
                    balle.vy = -balle.vy
                else : 
                    balle.vx = -balle.vx"""
        #print(int(self.y - balle.y), int(self.x - balle.x), margex, margex)

class Jeu:
    def __init__(self):
        self.en_jeu = True
        self.niveau = 1
        self.balle = Balle()
        self.raquette = Raquette()
        self.vie = NOMBRE_VIES
        self.score = 0
        self.briques_touchees = 0
        self.brique_liste = []
        self.creation_niveaux()

    def gestion_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.balle.sur_raquette:
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(90)
                    if self.en_jeu == False:
                        self.vie = NOMBRE_VIES
                        self.niveau = 1
                        self.score = 0


    
    def mise_a_jour(self):
        x, y = pygame.mouse.get_pos()
        self.balle.deplacer(self.raquette)
        if self.balle.loose:
            self.vie -= 1
            self.balle.loose = False
        for brique in self.brique_liste:
            if brique.en_vie():
                if brique.collision_balle(self.balle):
                    self.score += 1
                    self.briques_touchees += 1
        self.raquette.deplacer(x)
        self.en_jeu = True

    def affichage(self):
        screen.fill(NOIR)
        afficher_murs()
        afficher_ATH(self)
        self.balle.afficher()
        self.raquette.afficher()
        for brique in self.brique_liste:
            if brique.en_vie():
                brique.afficher()

    def game_over(self):
        screen.fill(NOIR)
        if jeu.vie == 0 :
            texte, rect = myfont.render("GAME OVER", (255,255,255), size = RAYON_BALLE*10)
        else :
            texte, rect = myfont.render("GAME WIN", (255,255,255), size = RAYON_BALLE*10)
        rect.center = (int(width/2), int(height/2))
        screen.blit(texte, rect)
        texte, rect = myfont.render("SCORE : " + str(self.score), (255,255,255), size = RAYON_BALLE*4)
        rect.midtop = (int(width/2), int(height/5*3))
        screen.blit(texte, rect)
        self.en_jeu = False

    def creation_niveaux(self):
        if self.niveau == 1:
            self.brique_liste.append(Brique(500,500))
        elif self.niveau == 2:
            for i in range(int(XMIN + 2.5*RAYON_BALLE), int((XMAX - 2.5*RAYON_BALLE)/2), int(15*RAYON_BALLE)):
                for j in range(int(YMIN + 1.5*RAYON_BALLE), int((YMAX/2 - 1.5*RAYON_BALLE)/2), int(9*RAYON_BALLE)):
                    self.brique_liste.append(Brique(i + int(2.5*RAYON_BALLE),j + int(1.5*RAYON_BALLE) ))
        elif self.niveau == 2 : 
            for i in range(int(XMIN + 2.5*RAYON_BALLE), int(XMAX - 2.5*RAYON_BALLE), int(15*RAYON_BALLE)):
                for j in range(int(YMIN + 1.5*RAYON_BALLE), int(YMAX/2 - 1.5*RAYON_BALLE), int(9*RAYON_BALLE)):
                    self.brique_liste.append(Brique(i + int(2.5*RAYON_BALLE),j + int(1.5*RAYON_BALLE) ))
        


def afficher_ATH(jeu) :
    texte, rect = myfont.render("Vies : "+str(jeu.vie), (255,255,255), size = RAYON_BALLE*2)
    rect.midleft = (XMIN, int(YMIN/2))
    screen.blit(texte, rect)
    texte, rect = myfont.render("Score : "+str(jeu.score), (255,255,255), size = RAYON_BALLE*2)
    rect.midright = (XMAX, int(YMIN/2))
    screen.blit(texte, rect)
    texte, rect = myfont.render("Niveau : "+str(jeu.niveau), (255,255,255), size = RAYON_BALLE*3)
    rect.center = (int(XMAX/2), int(YMIN/2))
    screen.blit(texte, rect)

def afficher_murs():
    pygame.draw.rect(screen, BLANC, (XMIN-RAYON_BALLE, YMIN-RAYON_BALLE, RAYON_BALLE, YMAX-YMIN+RAYON_BALLE), 0)
    pygame.draw.rect(screen, BLANC, (XMAX, YMIN-RAYON_BALLE, RAYON_BALLE, YMAX-YMIN+RAYON_BALLE), 0)
    pygame.draw.rect(screen, BLANC, (XMIN, YMIN-RAYON_BALLE, XMAX - XMIN + RAYON_BALLE, RAYON_BALLE), 0)

jeu = Jeu()

while True:
    jeu.brique_liste = []
    jeu.creation_niveaux()
    while jeu.vie > 0 and jeu.briques_touchees < len(jeu.brique_liste):
        jeu.gestion_evenements()
        jeu.mise_a_jour()
        jeu.affichage()
        pygame.display.flip()
        clock.tick(FPS)
    jeu.briques_touchees = 0
    jeu.niveau += 1
    while jeu.vie == 0:
        jeu.gestion_evenements()
        jeu.game_over()
        pygame.display.flip()
        clock.tick(FPS)
    while jeu.niveau > NOMBRE_NIVEAUX:
        jeu.gestion_evenements()
        jeu.game_over()
        pygame.display.flip()
        clock.tick(FPS)
    jeu.balle.sur_raquette = True

