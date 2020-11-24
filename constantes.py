import pip
import pygame
import pygame.freetype
pip._internal.main(['install', "mss"])
from mss import mss

pygame.init()

pygame.freetype.init()

pygame.mixer.init()

myfont=pygame.freetype.SysFont("arialblack",20)

#monitorwidth, monitorheight = 1280, 720
monitorwidth, monitorheight =mss().monitors[1]["width"], mss().monitors[1]["height"]
width, height = int(monitorwidth/5*4), int(monitorheight/5*4)
#width, height = int(monitorwidth), int(monitorheight)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ping")

FPS = 144
TICK = 1/FPS
clock = pygame.time.Clock()

SONS = {"touche" : "sounds\\hit5.wav", "score" : "sounds\\score.wav", "perte_vie" : "sounds\\error5.wav", "niveau_sup" : "sounds\\upgrade4.wav", "game_over" : "sounds\\fall3.wav"}
def jouer_son(nom_son):
    son = pygame.mixer.Sound(SONS[nom_son])
    son.set_volume(0.2)
    son.play()

COULEURS = {"BLANC" : (255,255,255),"GRIS" : (100,100,100), "ANTHRACITE" : (50,50,50), "NOIR" : (0,0,0), "ROUGE" : (255,0,0), "VERT" : (0,255,0), "BLEU" : (0,0,255), "ORANGE" : (255,255,0)}

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
NOMBRE_VIES = 3
RAYON_BALLE = int(monitorwidth/150)
LONGUEUR_BRIQUE = 5*RAYON_BALLE
LARGEUR_BRIQUE = 3*RAYON_BALLE
XMIN, YMIN = int(width/20) , int(width/20)
XMAX , YMAX = int(width - width/20), height
