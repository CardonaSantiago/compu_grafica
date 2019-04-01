import pygame,sys,random

#------------------------
# Screen Size
Ancho = 400
Alto = 400
#colores
Negro=(0,0,0)
Rojo =(255,0,0)
Verde=(0,255,0)
Azul =(0,0,255)
Amarillo=(246,255,51)
Blanco=(255,255,255)
#-------------------------
#class

class Jugador(pygame.sprite.Sprite):
    """docstring for Jugador."""
    def __init__(self, an, al):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([an,al])
        self.image.fill(Blanco)
        self.rect =self.image.get_rect()
        self.vel_x=0
        self.salud=[50,Alto-20,100,10]

    def update(self):
        self.rect.x+=self.vel_x
        if self.rect.x>(Ancho-self.rect.width):
            self.vel_x= 0
        if self.rect.x<0:
            self.vel_x=0

class Rival(pygame.sprite.Sprite):
    """docstring for Rival."""
    def __init__(self, anc, alt):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([anc,alt])
        self.image.fill(Rojo)
        self.rect = self.image.get_rect()
        self.rect.y=0
        self.vel_x=0
        self.vel_y=1
        self.temporizador=random.randrange(1000)

    def update(self):
        if self.temporizador>0:
            self.temporizador-=1
        else:
            self.rect.y+=self.vel_y

class Linea(pygame.sprite.Sprite):
    def __init__(self,an,al):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([an,al])
        self.image.fill(Blanco)
        self.rect = self.image.get_rect()
        self.vel_x=0
        self.vel_y=0

class Bala(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([10,15])
        self.image.fill(Verde)
        self.rect=self.image.get_rect()
        self.vel_y=-4

    def update(self):
        self.rect.y += self.vel_y
#----------------------------------
#funtion
def main():
    pygame.init()
    pantalla=pygame.display.set_mode([Ancho, Alto])
    fuente=pygame.font.Font(None,24)
    #-------------
    #Constantes
    vida=Verde
    v=0
    eliminado=0
    #--------------
    #JUGADOR
    general = pygame.sprite.Group()
    jp=Jugador(100,20)
    jp.rect.x=200
    jp.rect.y=Alto-jp.rect.height-40
    general.add(jp)
    #-------------
    #linea de informacion
    line= pygame.sprite.Group()
    l=Linea(Ancho,5)
    line.add(l)
    l.rect.x=0
    l.rect.y=360
    #--------------
    #rivales
    rivales=pygame.sprite.Group()
    enemigos=10
    for i in range(enemigos):
        r=Rival(20,20)
        r.rect.x=random.randrange(10,Ancho-20)
        r.rect.y=(-400)
        rivales.add(r)
        general.add(r)
        line.add(r)
    #---------------------
    #Balas
    balas = pygame.sprite.Group()

    reloj=pygame.time.Clock()
    fin_juego=False
    fin=False

    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    jp.vel_x=10
                if event.key == pygame.K_LEFT:
                    jp.vel_x=-10
                if event.key == pygame.K_SPACE:
                    b =Bala()
                    b.rect.x=jp.rect.x+((jp.rect.width/2)-(b.rect.width/2))
                    b.rect.y= jp.rect.y
                    balas.add(b)

            if event.type == pygame.KEYUP:
                jp.vel_x=0

        ls_col=pygame.sprite.spritecollide(l,rivales,True)
        for r in ls_col:
            rivales.remove(r)

        for b in balas:
            b_col = pygame.sprite.spritecollide(b,rivales,True)
            for ba in b_col:
                balas.remove(b)
                eliminado+=1
            if b.rect.y<-10:
                balas.remove(b)

        lv_col=pygame.sprite.spritecollide(jp,rivales,True)
        for r in lv_col:
            rivales.remove(r)
            if v ==0:
                jp.salud[2]=66
                vida=Amarillo
            if v ==1:
                jp.salud[2]=33
                vida=Rojo
            if v ==2:
                jp.salud[2]=0
                vida=Negro
            v+=1
            print (v)
        if jp.salud[2]==0:
            fin=True
        if eliminado == enemigos:
            fin = False
        if enemigos ==0:
            fin = True

        #----------------------------
        #conditions

        #----------------------------
        # Refresco de pantalla
        general.update()
        rivales.update()
        line.update()
        balas.update()


        texto1=fuente.render("Vida: ",True,Blanco)
        pygame.draw.rect(pantalla,vida,jp.salud)
        pantalla.blit(texto1,[5,Alto-24])

        texto2=fuente.render("Score: ",True,Blanco)
        texto3=fuente.render(str(eliminado),True,Blanco)
        pantalla.blit(texto2,[240,Alto-24])
        pantalla.blit(texto3,[300,Alto-24])


        general.draw(pantalla)
        rivales.draw(pantalla)
        line.draw(pantalla)
        balas.draw(pantalla)


        pygame.display.flip()
        pantalla.fill(Negro)
        reloj.tick(40)
    #-----------------------
    #finish condition

    if eliminado==10:
        print ('you Win')
    else:
        print ('you Lose')
    pygame.time.wait(200)

if __name__ == '__main__':
    main()
