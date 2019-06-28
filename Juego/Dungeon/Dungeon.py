import pygame
import math
import random
ancho=640
alto=480
centro = [320, 240]
White = [250,250,250]
Black = [0,0,0]

win = pygame.display.set_mode([ancho,alto])

def recorteSimple (imagenArecortar, x, y):
    imagen = pygame.image.load(imagenArecortar)
    limites = imagen.get_rect()
    newlx = limites[2] / x
    lx=int(newlx)
    newly = limites[3] / y
    ly=int(newly)
    m=[]
    for i in range(0,lx):
        for j in range(0, ly):
            cuadro=imagen.subsurface(i*x,j*y,x,y)
            m.append(cuadro)
    return m

def redrawWindonw():
    win.fill([0,0,0])
    playerList.draw(win)
    indicadores.draw(win)
    ModifierOne.draw(win)
    ModifierTwo.draw(win)
    ModifierThree.draw(win)
    Haunters.draw(win)
    Shooters.draw(win)
    FireBalls.draw(win)
    LaserBeams.draw(win)
    pygame.display.flip()

#--------------------------------------------------------------------------------------------------------------

#      CLASES

class Player(pygame.sprite.Sprite):
    def __init__(self, sheet):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 0
        self.action = 0
        self.limit = 0
        self.lim = [1, 1, 5, 5, 2, 2]
        self.vida = 100
        self.sheet = sheet
        self.image = self.sheet[self.action][self.limit]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 240
        self.vel_x = 0
        self.vel_y = 0
        self.frame = pygame.time.Clock()

    def update(self):

        if self.vida > 100:
            self.vida = 100

        elif (self.limit > self.lim[self.action]):
            self.limit = 0

        elif self.action == 0 or self.action == 1:
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(20)

        elif self.action == 2 or self.action == 3:
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(20)

        elif self.action == 4 or self.action == 5:
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            if (self.limit > self.lim[self.action]):
                self.action = 0
            self.frame.tick(5)


class Salud (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cantidadVida=0
        self.image = pygame.Surface([self.cantidadVida,10])
        self.image.fill([0,250,0])
        self.rect = self.image.get_rect()

    def update(self, VidaActual):

        self.cantidadVida = VidaActual
        if self.cantidadVida > 100:
            self.cantidadVida = 100
            self.image=pygame.Surface([self.cantidadVida,10])
            self.image.fill([0,250,0])

        else:
            self.image=pygame.Surface([self.cantidadVida,10])
            self.image.fill([0,250,0])


class Modifier(pygame.sprite.Sprite):
    def __init__(self, image, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame = pygame.time.Clock()

    def update(self):
        pass


class Proyectile(pygame.sprite.Sprite):
    def __init__(self, list):
        pygame.sprite.Sprite.__init__(self)
        self.limit = 0
        self.list = list
        self.image = self.list[self.limit]
        self.rect = self.image.get_rect()
        self.vel_x = 0
        self.vel_y = 0
        self.frame = pygame.time.Clock()

    def update(self):

        if (self.limit > 1):
            self.limit = 0

        else:
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            self.image = self.list[self.limit]
            self.limit += 1
            self.frame.tick(60)


class Haunter(pygame.sprite.Sprite):
    def __init__(self, sheet, lim1, lim2, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.action = 0
        self.limit = 0
        self.lim = [lim1, lim2]
        self.radius = 150
        self.sheet = sheet
        self.image = self.sheet[self.action][self.limit]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.frame = pygame.time.Clock()
        self.distance_above_player = 5
        self.speed = 2

    def pos_towards_player(self, player_rect):
        c = math.sqrt((player_rect.x - self.rect.x) ** 2 + (player_rect.y - self.distance_above_player  - self.rect.y) ** 2)
        try:
            x = (player_rect.x - self.rect.x) / c
            y = ((player_rect.y - self.distance_above_player)  - self.rect.y) / c
        except ZeroDivisionError:
            return False
        return (x,y)


    def followPlayer(self, player):

        new_pos = self.pos_towards_player(player.rect)
        if new_pos:
            self.rect.x, self.rect.y = (self.rect.x + new_pos[0] * self.speed, self.rect.y + new_pos[1] * self.speed)

        if (self.limit > self.lim[self.action]):
            self.limit = 0

        elif self.action == 0 or self.action == 1:
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(10)

    def update(self):

        if (self.limit > self.lim[self.action]):
            self.limit = 0

        elif self.action == 0 or self.action == 1:
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(10)


class Shooter(pygame.sprite.Sprite):
    def __init__(self, sheet, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.action = 0
        self.limit = 0
        self.lim = [6, 6]
        self.temp = 20
        self.sheet = sheet
        self.image = self.sheet[self.action][self.limit]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.frame = pygame.time.Clock()

    def update(self):

        self.temp -= 1

        if (self.limit > self.lim[self.action]):
            self.limit = 0

        elif self.action == 0 or self.action == 1:
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(10)
#------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    #inicializacion
    pygame.init()
    fin=False
    game_over=False
    KeyObtained=False
    PowerObtained=False
    fuente = pygame.font.Font(None,36)

    Indicador = [0, 255, 0]

    Idle = recorteSimple('WizardIdle.png',12,15)
    Idle2 = recorteSimple('WizardIdle2.png',12,15)
    Walk = recorteSimple('WizardWalk.png',12,15)
    Walk2 = recorteSimple('WizardWalk2.png',12,15)
    Attack = recorteSimple('WizardAttack.png',12,15)
    Attack2 = recorteSimple('WizardAttack2.png',12,15)
    Wizard = [Idle, Idle2, Walk, Walk2, Attack, Attack2]

    Ball = recorteSimple('Fire.png',12,12)
    FireShoot = Ball

    BallPlus = recorteSimple('Fire+.png',19,14)
    SuperFireShoot = BallPlus

    Potion = pygame.image.load('Potion.png').convert_alpha()

    Key = pygame.image.load('Key.png').convert_alpha()

    PowerUp = pygame.image.load('PowerUp.png').convert_alpha()

    MonsterEye = recorteSimple('MonsterOne.png', 16, 14)
    MonsterEye2 = recorteSimple('MonsterOneI.png', 16, 14)
    EvilEye = [MonsterEye, MonsterEye2]

    MonsterBot = recorteSimple('MonsterTwo.png', 22, 20)
    MonsterBot2 = recorteSimple('MonsterTwoI.png', 22, 20)
    KillBot = [MonsterBot, MonsterBot2]

    MonsterHand = recorteSimple('MonsterThree.png', 23, 19)
    MonsterHand2 = recorteSimple('MonsterThreeI.png', 23, 19)
    EvilHand = [MonsterHand, MonsterHand2]

    Beam = recorteSimple('Laser.png', 12, 12)
    LaserShoot = Beam

    playerList = pygame.sprite.Group()
    player = Player(Wizard)
    playerList.add(player)

    indicadores = pygame.sprite.Group()
    sPlayer = Salud()
    sPlayer.rect.x = 120
    sPlayer.rect.y = alto-30
    sPlayer.update(player.vida)
    indicadores.add(sPlayer)

    ModifierOne = pygame.sprite.Group()
    ModifierTwo = pygame.sprite.Group()
    ModifierThree = pygame.sprite.Group()

    KeyModifier = Modifier(Key, 50, 50)
    ModifierTwo.add(KeyModifier)

    PowerUpModifier = Modifier(PowerUp, 600, 440)
    ModifierThree.add(PowerUpModifier)

    Haunters = pygame.sprite.Group()
    Shooters = pygame.sprite.Group()
    enemyEye = Haunter(EvilEye, 6, 6, 320, 200)
    enemyBot = Shooter(KillBot, 600, 100)
    enemyHand = Haunter(EvilHand, 1, 1, 600, 50)
    Haunters.add(enemyEye)
    Shooters.add(enemyBot)
    Haunters.add(enemyHand)
    enemyEye.action = 1
    enemyBot.action = 1
    enemyHand.action = 1

    FireBalls = pygame.sprite.Group()
    LaserBeams = pygame.sprite.Group()

    while not fin:
        #captura de eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                fin=True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    player.vel_x = 7
                    player.vel_y = 0
                    player.direction = 0
                    player.action = 2

                if event.key == pygame.K_LEFT:
                    player.vel_x = -7
                    player.vel_y = 0
                    player.direction = 1
                    player.action = 3

                if event.key == pygame.K_UP:
                    player.vel_x = 0
                    player.vel_y = -7
                    player.direction = 2
                    player.action = 2

                if event.key == pygame.K_DOWN:
                    player.vel_x = 0
                    player.vel_y = 7
                    player.direction = 3
                    player.action = 3

                if event.key == pygame.K_SPACE:

                    if PowerObtained == False:
                        Fire = Proyectile(FireShoot)
                        Fire.rect.x = player.rect.x
                        Fire.rect.y = player.rect.y
                        FireBalls.add(Fire)
                        if player.direction == 0:
                            Fire.vel_x = 15
                            player.action = 4
                        elif player.direction == 1:
                            Fire.vel_x = -15
                            player.action = 5
                        elif player.direction == 2:
                            Fire.vel_y = -15
                            player.action = 0
                        elif player.direction == 3:
                            Fire.vel_y = 15
                            player.action = 1

                    elif PowerObtained == True:
                        FirePlus = Proyectile(SuperFireShoot)
                        FirePlus.rect.x = player.rect.x
                        FirePlus.rect.y = player.rect.y
                        FireBalls.add(FirePlus)
                        if player.direction == 0:
                            FirePlus.vel_x = 20
                            player.action = 4
                        elif player.direction == 1:
                            FirePlus.vel_x = -20
                            player.action = 5
                        elif player.direction == 2:
                            FirePlus.vel_y = -20
                            player.action = 0
                        elif player.direction == 3:
                            FirePlus.vel_y = 20
                            player.action = 1

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                    player.action = 0

                if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                    player.action = 1

#---------------------------------------------------------------------------------------------------

        for f in FireBalls:
            f_col = pygame.sprite.spritecollide(f, Haunters, True)
            for e in f_col:
                FireBalls.remove(f)
                PotionModifier = Modifier(Potion, e.rect.x, e.rect.y)
                ModifierOne.add(PotionModifier)
            if (f.rect.x < 0 and f.rect.y < 0 and f.rect.y > 640 and f.rect.y > 480):
                FireBalls.remove(f)

        for f in FireBalls:
            f_col = pygame.sprite.spritecollide(f, Shooters, True)
            for e in f_col:
                FireBalls.remove(f)
            if (f.rect.x < 0 and f.rect.y < 0 and f.rect.y > 640 and f.rect.y > 480):
                FireBalls.remove(f)


        for h in Haunters:
            Advise = pygame.sprite.collide_circle(player, h)
            if Advise:
                h.followPlayer(player)

        for h in Haunters:
            if h.rect.x < player.rect.x:
                h.action = 0

            elif h.rect.x > player.rect.x:
                h.action = 1


        for s in Shooters:
            if (s.temp == 0):
                Laser = Proyectile(LaserShoot)
                Laser.vel_x = -7
                Laser.rect.x = s.rect.x
                Laser.rect.y = s.rect.y
                LaserBeams.add(Laser)
                s.temp = 20
                if (Laser.rect.x < 0 and Laser.rect.y < 0 and Laser.rect.y > 640 and Laser.rect.y > 480):
                    LaserBeams.remove(Laser)


        for l in LaserBeams:
            l_col = pygame.sprite.spritecollide(l, playerList, False)
            for e in l_col:
                LaserBeams.remove(l)
                player.vida -= 20
                sPlayer.update(player.vida)

                if player.vida == 0:
                    game_over = True


        Potion_col = pygame.sprite.spritecollide(player, ModifierOne, True)
        for p in Potion_col:
            player.vida += 100
            sPlayer.update(player.vida)

        Key_col = pygame.sprite.spritecollide(player, ModifierTwo, True)
        for k in Key_col:
            KeyObtained = True

        PowerUp_col = pygame.sprite.spritecollide(player, ModifierThree, True)
        for p in PowerUp_col:
            PowerObtained = True

        if not game_over:
            player.update()
            ModifierOne.update()
            ModifierTwo.update()
            ModifierThree.update()
            Haunters.update()
            Shooters.update()
            FireBalls.update()
            LaserBeams.update()
            redrawWindonw()

        else:
           texto=fuente.render("GAME OVER", True, White)
           win.fill(Black)
           win.blit(texto,centro)
           pygame.display.flip()
