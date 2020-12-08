import sys
import pygame
import pygame.freetype
import math
from constantes import COULEURS, NOMBRE_VIES, NOMBRE_NIVEAUX, RAYON_BALLE, XMIN, XMAX, YMIN, YMAX, FPS, clock, screen, monitorwidth, width, height, myfont, jouer_son
from balle import Balle
from raquette import Raquette
from niveau import Niveau

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
                        self.balle.vitesse_par_angle(60)
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
                collision = brique.collision_balle(self.balle,prec)
                if collision[0]:
                    if not(prec):
                        if brique.vie > 0:
                            jouer_son("touche")
                        else:
                            jouer_son("score")
                    if collision[0] and not(collision[1]) :
                        self.score += 1
                        self.raquette.arc_en_ciel = True
                        self.briques_touchees += 1
                        if self.score % 50 == 0:
                            self.vie +=1
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
    #jeu.niveau.en_cours = 2
    jeu.niveau.creation_niveaux()
    while jeu.vie > 0 and jeu.briques_touchees < jeu.niveau.nombre_briques:
        jeu.gestion_evenements()
        jeu.mise_a_jour()
        jeu.affichage()
        pygame.display.flip()
        clock.tick(FPS)
    jeu.briques_touchees = 0
    jeu.niveau.en_cours += 1
    if jeu.vie == 0: 
        jouer_son("game_over")
    else:
        jouer_son("niveau_sup")
    while jeu.vie == 0 or jeu.niveau.en_cours > NOMBRE_NIVEAUX:
        jeu.raquette.arc_en_ciel = False
        jeu.gestion_evenements()
        jeu.game_over()
        pygame.display.flip()
        clock.tick(FPS)
    if jeu.vie != 0:
        jeu.vie += 1
    jeu.balle.sur_raquette = True
