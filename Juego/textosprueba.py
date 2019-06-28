'''
import pygame
from pygame.locals import *

pygame.init()

pantalla = pygame.display.set_mode((450,300),0,32)
pygame.display.set_caption("Modulo de fuentes")

reloj = pygame.time.Clock()

fuente = pygame.font.Font(None, 16)
texto1 = fuente.render("Texto de pruebas", 0, (255, 255, 255))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    reloj.tick(20)
    pantalla.blit(texto1, (100,100))
    pygame.display.update()
'''
import pygame,sys, random

width=480
height=480

red=[255,0,0]
green=[0,255,0]
blue=[0,0,255]
yellow=[255,255,0]
black=[0,0,0]
white=[255,255,255]
pygame.init()
fuente=pygame.font.Font(None,16)

class Player(pygame.sprite.Sprite):
    """docstring for Player."""
    def __init__(self, point):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([16,16])
        self.image.fill(white)
        self.rect=self.image.get_rect()
        self.rect.x=point[0]
        self.rect.y=point[1]
        self.velx=0
        self.vely=0
        self.salud=[32,16,100,10]
        self.sound = pygame.mixer.Sound('Wilhelm_Scream.ogg')
    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

        if (self.rect.x>width or self.rect.x<0 or self.rect.y>height or self.rect.y<32):
            self.rect.x=64
            self.rect.y=96


class Block(pygame.sprite.Sprite):
    """Clase jugador"""
    def __init__(self, point, dimensions):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dimensions)
        self.image.fill(blue)
        # rect posiciona el objeto
        self.rect = self.image.get_rect()
        self.rect.x = point[0]
        self.rect.y = point[1]
class Meta(pygame.sprite.Sprite):
    """Clase jugador"""
    def __init__(self, point, dimensions):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dimensions)
        self.image.fill(red)
        # rect posiciona el objeto
        self.rect = self.image.get_rect()
        self.rect.x = point[0]
        self.rect.y = point[1]
def main():
    pantalla=pygame.display.set_mode([width,height])
    #bgm = pygame.mixer.Sound('Common Fight.ogg')
    bg1=pygame.image.load('mapa/dungeon2.png')
    #bgm.play(-1)
    #Vida
    vida=green
    v=0
    jugador=pygame.sprite.Group()
    #p=Player([432,432])
    p=Player([352,160])
    jugador.add(p)
    meta=pygame.sprite.Group()
    met=Meta([356,128],[28,16])
    meta.add(met)

    muro=pygame.sprite.Group()
    #muros VERTICALES
    m1=Block([0,32],[470,16])
    m2=Block([0,48],[16,448])
    m3=Block([0,470],[480,16])
    m4=Block([468,32],[16,448])
    #muros
    m5=Block([112,48],[16,108])
    m6=Block([128,144],[108,12])
    m7=Block([222,145],[16,30])
    m8=Block([224,160],[44,16])
    m9=Block([176,96],[112,16])
    m10=Block([272,84],[80,12])
    m11=Block([336,96],[16,128])
    m12=Block([64,208],[272,16])
    m13=Block([64,224],[16,112])
    m14=Block([64,340],[400,10])
    m15=Block([352,112],[48,16])
    m16=Block([384,128],[16,48])
    m17=Block([400,160],[16,80])
    #muros horizontales
    m18=Block([384,224],[16,64])
    m19=Block([192,272],[192,16])
    m20=Block([192,288],[16,28])
    m21=Block([272,352],[16,96])
    m22=Block([176,384],[96,12])
    m23=Block([288,432],[64,16])
    m24=Block([320,384],[80,16])
    m25=Block([384,400],[32,16])
    m26=Block([400,416],[16,48])
    m27=Block([16,384],[64,16])
    m28=Block([64,400],[16,32])
    m29=Block([112,384],[16,80])
    m30=Block([128,416],[112,16])
    m31=Block([112,180],[16,32])
    m32=Block([336,48],[16,12])

    muro.add(m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30,m31,m32)

    reloj=pygame.time.Clock()
    fin=False
    finMeta=False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    p.velx=1
                if event.key == pygame.K_LEFT:
                    p.velx=-1
                if event.key == pygame.K_UP:
                    p.vely=-1
                if event.key == pygame.K_DOWN:
                    p.vely=1
            if event.type == pygame.KEYUP:
                p.velx=0
                p.vely=0
        lc=pygame.sprite.spritecollide(p,muro,False)
        for b in lc:
            p.sound.play()
            if p.rect.right > b.rect.left and p.velx > 0 :
                p.salud[2]=66
                vida=yellow
                p.rect.right = b.rect.left
                p.velx = 0
            if p.rect.left < b.rect.right and p.velx < 0:
                p.rect.left = b.rect.right
                p.velx = 0
            if p.rect.bottom > b.rect.top and p.vely > 0:
                p.rect.bottom = b.rect.top
                p.vely = 0
            if p.rect.top < b.rect.bottom and p.vely < 0:
                p.rect.top = b.rect.bottom
                p.vely = 0


        mt=pygame.sprite.spritecollide(p,meta,False)
        for b in mt:
            finMeta=True

        jugador.update()

        pantalla.blit(bg1,[0,0])

        jugador.draw(pantalla)
        texto1=fuente.render("Vida: ",True,white)
        pygame.draw.rect(pantalla,vida,p.salud)
        pantalla.blit(texto1,[0,16])
        muro.draw(pantalla)
        meta.draw(pantalla)
        if finMeta == True:
            #bgm.stop()
            fin=True
            finMeta=False
        pygame.display.flip()
        reloj.tick(60)



if __name__ == '__main__':
    main()
