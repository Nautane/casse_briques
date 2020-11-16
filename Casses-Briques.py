from mss import mss
import random
import sys
import pygame
import pygame.freetype
import math

pygame.init()

pygame.freetype.init()
myfont=pygame.freetype.SysFont("arialblack",20)

#monitorwidth, monitorheight = 1280, 720
monitorwidth, monitorheight =mss().monitors[1]["width"], mss().monitors[1]["height"]
width, height = int(monitorwidth/5*4), int(monitorheight/5*4)
#width, height = int(monitorwidth), int(monitorheight)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ping")

FPS = 60
TICK = 1/FPS
clock = pygame.time.Clock()

COULEURS = {"BLANC" : (255,255,255),"GRIS" : (100,100,100), "ANTHRACITE" : (50,50,50), "NOIR" : (0,0,0), "ROUGE" : (255,0,0), "VERT" : (0,255,0), "BLEU" : (0,0,255)}
COULEURSBRIQUES = [value for value in COULEURS.values() if value != (0,0,0)]

def arc_en_ciel():
    r, g, b = 255, 0, 0
    result = []
    increment = 255/FPS
    for i in range(FPS):
        if i < FPS/6:
            g += increment*6
        elif FPS/6 < i < FPS/6*2:
            r -= increment*6
        elif FPS/6*2 < i < FPS/6*3:
            b += increment*6
        elif FPS/6*3 < i < FPS/6*4:
            g -= increment*6
        elif FPS/6*4 < i < FPS/6*5:
            r += increment*6
        elif FPS/6*5 < i:
            b -= increment*6
        result.append((int(r),int(g),int(b)))
    return result

ARC_EN_CIEL = arc_en_ciel()

NOMBRE_NIVEAUX = 3
NOMBRE_VIES = 6
RAYON_BALLE = int(monitorwidth/150)
LONGUEUR_BRIQUE = int(5*RAYON_BALLE)
LARGEUR_BRIQUE = int(3*RAYON_BALLE)
XMIN, YMIN = int(width/20) , int(width/20)
XMAX , YMAX = int(width - width/20), height

class Balle:
    def vitesse_par_angle(self, angle):
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def __init__(self):
        self.x, self.y = (400,400)
        self.vitesse = 600/FPS
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
            if self.y - RAYON_BALLE < YMIN:
                self.vy = -self.vy

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
            pygame.draw.rect(screen, self.couleur, (int(self.x-self.longueur/2), int(self.y-self.largeur/2), self.longueur, self.largeur))
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

class Niveau: 
    def __init__(self):
        self.en_cours = 1
        self.nombre_briques = 0
        self.brique_liste = []

    def creation_niveaux(self):
        self.brique_liste = []
        if self.en_cours == 1:
            #self.brique_liste.append(Brique(width/2,height/2, 3))
            self.brique_liste.append(Brique(width/2,height/2))
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

class Jeu:
    def __init__(self):
        self.en_jeu = True
        self.balle = Balle()
        self.raquette = Raquette()
        self.niveau = Niveau()
        self.vie = NOMBRE_VIES
        self.score = 0
        self.briques_touchees = 0

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
                        self.niveau.en_cours = 1
                        self.score = 0
    
    def mise_a_jour(self):
        x, y = pygame.mouse.get_pos()
        self.balle.deplacer(self.raquette)
        if self.balle.loose:
            self.vie -= 1
            self.balle.loose = False
        prec = False
        for brique in self.niveau.brique_liste:
            if brique.en_vie():
                if brique.collision_balle(self.balle,prec) :
                    self.score += 1
                    self.raquette.arc_en_ciel = True
                    self.briques_touchees += 1
                    prec = True
        self.raquette.deplacer(x)
        self.en_jeu = True

    def affichage(self):
        screen.fill(COULEURS["NOIR"])
        afficher_murs()
        afficher_ATH(self)
        self.balle.afficher()
        self.raquette.afficher()
        self.niveau.afficher()

    def game_over(self):
        screen.fill(COULEURS["NOIR"])
        if jeu.vie == 0 :
            texte, rect = myfont.render("GAME OVER", (255,255,255), size = monitorwidth/15)
        else :
            texte, rect = myfont.render("GAME WIN", (255,255,255), size = monitorwidth/15)
        rect.center = (int(width/2), int(height/2))
        screen.blit(texte, rect)
        texte, rect = myfont.render("SCORE : " + str(self.score), (255,255,255), size = monitorwidth/38)
        rect.midtop = (int(width/2), int(height/5*3))
        screen.blit(texte, rect)
        texte, rect = myfont.render("NIVEAU : " + str(self.niveau.en_cours-1), (255,255,255), size = monitorwidth/38)
        rect.midbottom = (int(width/2), int(height/5*2))
        screen.blit(texte, rect)
        self.en_jeu = False
        
def afficher_ATH(jeu) :
    texte, rect = myfont.render("Vies : "+str(jeu.vie), (255,255,255), size = RAYON_BALLE*2)
    rect.midleft = (XMIN, int(YMIN/2))
    screen.blit(texte, rect)
    texte, rect = myfont.render("Score : "+str(jeu.score), (255,255,255), size = RAYON_BALLE*2)
    rect.midright = (XMAX, int(YMIN/2))
    screen.blit(texte, rect)
    texte, rect = myfont.render("Niveau : "+str(jeu.niveau.en_cours), (255,255,255), size = RAYON_BALLE*3)
    rect.center = (int(XMAX/2), int(YMIN/2))
    screen.blit(texte, rect)

def afficher_murs():
    pygame.draw.rect(screen, COULEURS["BLANC"], (XMIN-RAYON_BALLE, YMIN-RAYON_BALLE, RAYON_BALLE, YMAX-YMIN+RAYON_BALLE), 0)
    pygame.draw.rect(screen, COULEURS["BLANC"], (XMAX, YMIN-RAYON_BALLE, RAYON_BALLE, YMAX-YMIN+RAYON_BALLE), 0)
    pygame.draw.rect(screen, COULEURS["BLANC"], (XMIN, YMIN-RAYON_BALLE, XMAX - XMIN + RAYON_BALLE, RAYON_BALLE), 0)

jeu = Jeu()

while True:
    jeu.niveau.creation_niveaux()
    while jeu.vie > 0 and jeu.briques_touchees < jeu.niveau.nombre_briques:
        jeu.gestion_evenements()
        jeu.mise_a_jour()
        jeu.affichage()
        pygame.display.flip()
        clock.tick(FPS)
    jeu.briques_touchees = 0
    jeu.niveau.en_cours += 1
    while jeu.vie == 0 or jeu.niveau.en_cours > NOMBRE_NIVEAUX:
        jeu.raquette.arc_en_ciel = False
        jeu.gestion_evenements()
        jeu.game_over()
        pygame.display.flip()
        clock.tick(FPS)
    jeu.balle.sur_raquette = True

