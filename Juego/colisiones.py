import pygame
import  random
import sys
#sys.path.insert(0, 'G:/Mi unidad/Computación Gráfica')
#from graphic_repository import *
GREEN=[0,255,255]
YELLOW=[250,250,0]
BLACK=[0,0,0]
WIDTH=480
HEIGHT=480
# Pasos:
# crear clase, luego grupos de sprite, el objeto,
# mostrar objeto y actualizarlos

class Player(pygame.sprite.Sprite):
    """Clase jugador"""
    def __init__(self, point):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([40, 50])
        self.image.fill(GREEN)
        # rect posiciona el objeto
        self.rect = self.image.get_rect()
        self.rect.x = point[0]
        self.rect.y = point[1]
        self.velx = 0 # atributo velocidad
        self.vely = 0
        self.sound = pygame.mixer.Sound('Wilhelm_Scream.ogg')

    def update(self):
        self.rect.x += self.velx    # mueve el objeto
        self.rect.y += self.vely

class Block(pygame.sprite.Sprite):
    """Clase jugador"""
    def __init__(self, point, dimensions):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dimensions)
        self.image.fill(YELLOW)
        # rect posiciona el objeto
        self.rect = self.image.get_rect()
        self.rect.x = point[0]
        self.rect.y = point[1]


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    end = False
    end_game = False
    clock = pygame.time.Clock()
    points = 0
    bgm = pygame.mixer.Sound('Common Fight.ogg')
    cont_cuadros = 0
    tasa_cuadros = 60
    # GRUPOS -------------------------------------------------
    players = pygame.sprite.Group() # players es de tipo Group
    blocks = pygame.sprite.Group()
    # --------------------------------------------------------

    p = Player([100, 150]) # instancia la clase
    players.add(p) # aniade p al grupo de jugadores

    b = Block([300, 150], [100, 100])
    blocks.add(b)
    b1 = Block([400, 300], [100, 50])
    blocks.add(b1)
    bgm.play(-1)   # -1 to repeat indefinitely
    while not end and not end_game:
        segundo = cont_cuadros // tasa_cuadros
        print(segundo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            # TECLADO --------------------------------------------------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end = True
                if event.key == pygame.K_RIGHT:
                    p.velx = 5
                    p.vely = 0
                if event.key == pygame.K_LEFT:
                    p.velx = -5
                    p.vely = 0
                if event.key == pygame.K_UP:
                    p.velx = 0
                    p.vely = -5
                if event.key == pygame.K_DOWN:
                    p.velx = 0
                    p.vely = 5
            # -----------------------------------------------------------------


        # CONTROL DE ELEMENTOS
        # --------------------------------------------------------------------------


        for p in players:
            if p.rect.x < 0:
                p.rect.x = 0
            if p.rect.x > (WIDTH - p.rect.width):
                p.rect.x = WIDTH - p.rect.width


        lc = pygame.sprite.spritecollide(p, blocks, False)
        for b in lc:
            p.sound.play()
            # no deja que el jugador se super-ponga con el bloque
            if p.rect.right > b.rect.left and p.velx > 0:
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


        players.update() # cada vez q haya update se aumentara la velx
        # blocks.update()


        # Regresco de pantalla
        screen.fill(BLACK)

        players.draw(screen) # dibuja los elementos de players
        blocks.draw(screen)
        pygame.display.flip()
        clock.tick(tasa_cuadros)
        cont_cuadros += 1
