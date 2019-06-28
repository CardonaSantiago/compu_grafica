#14/06/2019
#Colision con radio
#Color Alfa (un color que cambia con el fondo)
import pygame
import random
#from repositoriografi import *

NEGRO = [0, 0, 0]
VERDE = [0, 255, 0]
ROJO = [255, 0, 0]
BLANCO = [255, 255, 255]
ANCHO = 640
ALTO = 492

class Cuadro(pygame.sprite.Sprite):
    '''
    Clase cuadro
    '''
    def __init__(self, p):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40, 50])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = p[0]
        self.rect.y = p[1]
        self.click = False
        self.radius = 50



class Cuadro2(pygame.sprite.Sprite):
    '''
    Clase cuadro
    '''
    def __init__(self, p):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 25])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = p[0]
        self.rect.y = p[1]
        self.click = True
        self.velx = 0
        self.radius = 50


    def update(self):
        #Seguir al mouse o pegarce al mouse
        if self.click:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.rect.x += self.velx


if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    #Grupos
    cuadros = pygame.sprite.Group()
    cuadros2 = pygame.sprite.Group()
    c = Cuadro([200, 150])
    c2 = Cuadro2([400, 350])
    cuadros.add(c)
    cuadros2.add(c2)

    reloj = pygame.time.Clock()
    fin = False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True

        if pygame.sprite.collide_circle(c, c2):
            print ('cerca')

        #cuadros.update()
        cuadros2.update()
        pantalla.fill(NEGRO)
        cuadros.draw(pantalla)
        cuadros2.draw(pantalla)
        pygame.display.flip()
        reloj.tick(40)
