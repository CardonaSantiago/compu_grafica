import pygame,sys, random,math

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
win = pygame.display.set_mode([width,height])

def recorteSimple (imagenArecortar, x, y):
    imagen = pygame.image.load(imagenArecortar)
    limites = imagen.get_rect()
    lx = limites[2] / x
    newlx= int(lx)
    ly = limites[3] / y
    newly=int(ly)
    m=[]
    for i in range(0,newlx):
        for j in range(0, newly):
            cuadro=imagen.subsurface(i*x,j*y,x,y)
            m.append(cuadro)
    return m


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet,point):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 0
        self.action = 0
        self.limit = 0
        self.lim = [1, 1, 5, 5, 2, 2]
        self.vida = 100
        self.sheet = sheet
        self.image = self.sheet[self.action][self.limit]
        self.rect = self.image.get_rect()
        self.rect.x = point[0]
        self.rect.y = point[1]
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

        elif  self.cantidadVida < 0:
            self.cantidadVida = 0
            self.image=pygame.Surface([self.cantidadVida,10])

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
        self.radius = 50
        self.health = 100
        self.sheet = sheet
        self.image = self.sheet[self.action][self.limit]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame = pygame.time.Clock()
        self.distance_above_player = 5
        self.speed = 4

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
        self.temp = 10
        self.health = 100
        self.sheet = sheet
        self.image = self.sheet[self.action][self.limit]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame = pygame.time.Clock()

    def update(self):

        self.temp -= 1

        if (self.limit > self.lim[self.action]):
            self.limit = 0

        elif self.action == 0 or self.action == 1:
            self.image = self.sheet[self.action][self.limit]
            self.limit += 1
            self.frame.tick(10)


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
    #nivel2()
    bgm = pygame.mixer.Sound('stage 1.ogg')
    bg1=pygame.image.load('mapa/dungeon.png')
    bgm.play(-1)
    Idle = recorteSimple('Dungeon/WizardIdle.png',12,15)
    Idle2 = recorteSimple('Dungeon/WizardIdle2.png',12,15)
    Walk = recorteSimple('Dungeon/WizardWalk.png',12,15)
    Walk2 = recorteSimple('Dungeon/WizardWalk2.png',12,15)
    Attack = recorteSimple('Dungeon/WizardAttack.png',12,15)
    Attack2 = recorteSimple('Dungeon/WizardAttack2.png',12,15)
    Wizard = [Idle, Idle2, Walk, Walk2, Attack, Attack2]

    Ball = recorteSimple('Dungeon/Fire.png',12,12)
    FireShoot = Ball

    BallPlus = recorteSimple('Dungeon/Fire+.png',19,14)
    SuperFireShoot = BallPlus

    Potion = pygame.image.load('Dungeon/Potion.png').convert_alpha()

    Key = pygame.image.load('Dungeon/Key.png').convert_alpha()

    MonsterEye = recorteSimple('Dungeon/MonsterOne.png', 16, 14)
    MonsterEye2 = recorteSimple('Dungeon/MonsterOneI.png', 16, 14)
    EvilEye = [MonsterEye, MonsterEye2]

    MonsterBot = recorteSimple('Dungeon/MonsterTwo.png', 22, 20)
    MonsterBot2 = recorteSimple('Dungeon/MonsterTwoI.png', 22, 20)
    KillBot = [MonsterBot, MonsterBot2]

    Beam = recorteSimple('Dungeon/Laser.png', 12, 12)
    LaserShoot = Beam

    #Vida
    vida=green
    v=0
    #Grupos
    playerList = pygame.sprite.Group()
    player = Player(Wizard,  [48,96])
    playerList.add(player)

    indicadores = pygame.sprite.Group()
    sPlayer = Salud()
    sPlayer.rect.x = 40
    sPlayer.rect.y = 16
    sPlayer.update(player.vida)
    indicadores.add(sPlayer)

    ModifierOne = pygame.sprite.Group()
    ModifierTwo = pygame.sprite.Group()


    KeyModifier = Modifier(Key, 448, 448)
    ModifierTwo.add(KeyModifier)



    Haunters = pygame.sprite.Group()
    Shooters = pygame.sprite.Group()
    enemyEye = Haunter(EvilEye, 6, 6, 128, 432)
    enemyBot = Shooter(KillBot, 384, 256)
    enemyEye2 = Haunter(EvilEye, 6, 6, 240, 96)
    Haunters.add(enemyEye)
    Shooters.add(enemyBot)
    Haunters.add(enemyEye2)
    enemyEye.action = 0
    enemyBot.action = 1
    enemyEye2.action = 1

    score = 0
    enemyNumber=3

    FireBalls = pygame.sprite.Group()
    LaserBeams = pygame.sprite.Group()

    meta=pygame.sprite.Group()
    met=Meta([448,32],[16,16])
    meta.add(met)

    muro=pygame.sprite.Group()
    #muros VERTICALES
    m1=Block([0,32],[440,16])
    m2=Block([0,48],[16,448])
    m3=Block([0,464],[480,16])
    m4=Block([468,32],[16,448])
    m5=Block([160,48],[16,200])
    m6=Block([304,48],[32,92])
    m7=Block([160,278],[16,132])
    m8=Block([336,304],[16,122])
    m9=Block([96,384],[16,96])
    m10=Block([208,352],[16,64])
    m11=Block([272,352],[16,80])
    m12=Block([288,416],[16,48])
    m13=Block([320,164],[16,44])
    m14=Block([160,432],[16,32])
    m15=Block([16,368],[16,32])
    m16=Block([336,448],[16,16])
    m17=Block([84,384],[16,16])
    #muros horizontales
    m18=Block([16,176],[60,16])
    m19=Block([100,176],[64,16])
    m20=Block([16,320],[60,16])
    m21=Block([100,320],[64,16])
    m22=Block([176,208],[76,16])
    m23=Block([278,208],[208,16])
    m24=Block([176,304],[76,16])
    m25=Block([278,304],[70,16])
    m26=Block([224,352],[48,16])
    m27=Block([224,400],[28,16])
    m28=Block([352,384],[60,16])
    m29=Block([436,384],[32,16])
    m30=Block([336,128],[60,12])
    m31=Block([336,164],[60,12])
    m32=Block([370,96],[96,12])
    m33=Block([32,384],[28,16])

    muro.add(m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30,m31,m32,m33)

    reloj=pygame.time.Clock()
    #booleanos
    fin=False
    finMeta=False
    game_over = False
    KeyObtained=False
    PowerObtained=False
    while not fin:
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

        lc=pygame.sprite.spritecollide(player,muro,False)
        for b in lc:
            #p.sound.play()
            if player.rect.right > b.rect.left and player.vel_x > 0:
                player.rect.right = b.rect.left
                player.vel_x = 0
            if player.rect.left < b.rect.right and player.vel_x < 0:
                player.rect.left = b.rect.right
                player.vel_x = 0
            if player.rect.bottom > b.rect.top and player.vel_y > 0:
                player.rect.bottom = b.rect.top
                player.vel_y = 0
            if player.rect.top < b.rect.bottom and player.vel_y < 0:
                player.rect.top = b.rect.bottom
                player.vel_y = 0

        '''
        for h in Haunters:
            enemy_lc=pygame.sprite.spritecollide(h,muro,False)
            for b in enemy_lc:
                if h.rect.right > b.rect.left:
                    h.rect.right = b.rect.left

                if h.rect.left < b.rect.right :
                    h.rect.left = b.rect.right

                if h.rect.bottom > b.rect.top :
                    h.rect.bottom = b.rect.top

                if h.rect.top < b.rect.bottom :
                    h.rect.top = b.rect.bottom
            '''


        for f in FireBalls:
            f_lc=pygame.sprite.spritecollide(f,muro,False)
            for b in f_lc:
                #p.sound.play()
                if f.rect.right > b.rect.left:
                    FireBalls.remove(f)
                if f.rect.left < b.rect.right:
                    FireBalls.remove(f)
                if f.rect.bottom > b.rect.top:
                    FireBalls.remove(f)
                if f.rect.top < b.rect.bottom:
                    FireBalls.remove(f)

        for l in LaserBeams:
            l_lc=pygame.sprite.spritecollide(l,muro,False)
            for b in l_lc:
                #p.sound.play()
                if l.rect.right > b.rect.left:
                    LaserBeams.remove(l)
                if l.rect.left < b.rect.right:
                    LaserBeams.remove(l)
                if l.rect.bottom > b.rect.top:
                    LaserBeams.remove(l)
                if l.rect.top < b.rect.bottom:
                    LaserBeams.remove(l)


        for f in FireBalls:
            f_col = pygame.sprite.spritecollide(f, Haunters, False)

            for e in f_col:
                FireBalls.remove(f)
                if e.health != 0:
                    e.health -= 50

                if e.health == 0:
                    enemyNumber-=1
                    score+=250
                    Haunters.remove(e)
                    PotionModifier = Modifier(Potion, e.rect.x, e.rect.y)
                    ModifierOne.add(PotionModifier)

        for f in FireBalls:
            f_col = pygame.sprite.spritecollide(f, Shooters, False)

            for e in f_col:
                FireBalls.remove(f)
                if e.health != 0:
                    e.health -= 25

                if e.health == 0:
                    enemyNumber-=1
                    score+=500
                    Shooters.remove(e)



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
                s.temp = 10
                if (Laser.rect.x < 0 and Laser.rect.y < 0 and Laser.rect.y > 640 and Laser.rect.y > 480):
                    LaserBeams.remove(Laser)

        for h in Haunters:
            h_col = pygame.sprite.spritecollide(h, playerList, False)
            for e in h_col:
                player.vida -= 20
                sPlayer.update(player.vida)

                if player.vida == 0:
                    game_over = True

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

        mt=pygame.sprite.spritecollide(player,meta,False)
        for b in mt:
            if(enemyNumber==0 or KeyObtained==True):

                finMeta=True
            else:
                lc=pygame.sprite.spritecollide(player,meta,False)
                for b in lc:

                    if player.rect.top < b.rect.bottom and player.vel_y < 0:
                        player.rect.top = b.rect.bottom
                        player.vel_y = 0


        if not game_over:
            player.update()
            ModifierOne.update()
            ModifierTwo.update()
            Haunters.update()
            Shooters.update()
            FireBalls.update()
            LaserBeams.update()

            win.blit(bg1,[0,0])
            texto1=fuente.render("Health: ",True,white)
            win.blit(texto1,[0,16])

            texto2=fuente.render("Score: ",True,white)
            texto3=fuente.render(str(score),True,white)
            win.blit(texto2,[416,16])
            win.blit(texto3,[453,16])

            playerList.draw(win)
            indicadores.draw(win)
            ModifierOne.draw(win)
            ModifierTwo.draw(win)

            Haunters.draw(win)
            Shooters.draw(win)
            FireBalls.draw(win)
            LaserBeams.draw(win)
            pygame.display.flip()

            #muro.draw(win)
            #meta.draw(win)
            if finMeta == True:
                bgm.stop()
                fin=True
                finMeta=False
                nivel2()

            pygame.display.flip()
            reloj.tick(60)

        else:
           texto=fuente.render("GAME OVER", True, white)
           win.fill(black)
           win.blit(texto,[200, 240])
           bgm.stop()
           fin=True
           pygame.display.flip()


def nivel2():
    bg1=pygame.image.load('mapa/dungeon2.png')
    bgm = pygame.mixer.Sound('stage 2.ogg')
    bgm.play(-1)
    Idle = recorteSimple('Dungeon/WizardIdle.png',12,15)
    Idle2 = recorteSimple('Dungeon/WizardIdle2.png',12,15)
    Walk = recorteSimple('Dungeon/WizardWalk.png',12,15)
    Walk2 = recorteSimple('Dungeon/WizardWalk2.png',12,15)
    Attack = recorteSimple('Dungeon/WizardAttack.png',12,15)
    Attack2 = recorteSimple('Dungeon/WizardAttack2.png',12,15)
    Wizard = [Idle, Idle2, Walk, Walk2, Attack, Attack2]

    Ball = recorteSimple('Dungeon/Fire.png',12,12)
    FireShoot = Ball

    BallPlus = recorteSimple('Dungeon/Fire+.png',19,14)
    SuperFireShoot = BallPlus

    Potion = pygame.image.load('Dungeon/Potion.png').convert_alpha()

    PowerUp = pygame.image.load('Dungeon/PowerUp.png').convert_alpha()

    MonsterEye = recorteSimple('Dungeon/MonsterOne.png', 16, 14)
    MonsterEye2 = recorteSimple('Dungeon/MonsterOneI.png', 16, 14)
    EvilEye = [MonsterEye, MonsterEye2]

    MonsterBot = recorteSimple('Dungeon/MonsterTwo.png', 22, 20)
    MonsterBot2 = recorteSimple('Dungeon/MonsterTwoI.png', 22, 20)
    KillBot = [MonsterBot, MonsterBot2]

    MonsterHand = recorteSimple('Dungeon/MonsterThree.png', 23, 19)
    MonsterHand2 = recorteSimple('Dungeon/MonsterThreeI.png', 23, 19)
    EvilHand = [MonsterHand, MonsterHand2]

    Beam = recorteSimple('Dungeon/Laser.png', 12, 12)
    LaserShoot = Beam

    #Vida
    vida=green
    v=0
    #Grupos
    playerList = pygame.sprite.Group()
    player = Player(Wizard,  [432,432])
    playerList.add(player)

    indicadores = pygame.sprite.Group()
    sPlayer = Salud()
    sPlayer.rect.x = 40
    sPlayer.rect.y = 16
    sPlayer.update(player.vida)
    indicadores.add(sPlayer)

    ModifierOne = pygame.sprite.Group()
    ModifierThree = pygame.sprite.Group()

    PowerUpModifier = Modifier(PowerUp, 16, 400)
    ModifierThree.add(PowerUpModifier)

    Haunters = pygame.sprite.Group()
    Shooters = pygame.sprite.Group()
    enemyEye = Haunter(EvilEye, 6, 6, 48, 432)
    enemyEye2 = Haunter(EvilEye, 6, 6, 192, 448)
    enemyEye3 = Haunter(EvilEye, 6, 6, 304, 144)
    enemyBot = Shooter(KillBot, 96, 352)
    enemyBot2 = Shooter(KillBot, 352, 240)
    enemyHand = Haunter(EvilHand, 1, 1, 96, 256)
    enemyHand2 = Haunter(EvilHand, 1, 1, 32, 80)
    enemyHand3 = Haunter(EvilHand, 1, 1, 144, 80)
    Haunters.add(enemyEye,enemyEye2,enemyEye3,enemyHand,enemyHand2,enemyHand3)
    Shooters.add(enemyBot,enemyBot2)
    enemyEye.action = 0
    enemyEye2.action = 0
    enemyBot.action = 0
    enemyBot2.action = 1

    score = 0
    enemyNumber = 8
    FireBalls = pygame.sprite.Group()
    LaserBeams = pygame.sprite.Group()
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
    game_over=False
    PowerObtained=False
    while not fin:
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

        lc=pygame.sprite.spritecollide(player,muro,False)
        for b in lc:
            #p.sound.play()
            if player.rect.right > b.rect.left and player.vel_x > 0 :
                player.rect.right = b.rect.left
                player.vel_x = 0
            if player.rect.left < b.rect.right and player.vel_x < 0:
                player.rect.left = b.rect.right
                player.vel_x = 0
            if player.rect.bottom > b.rect.top and player.vel_y > 0:
                player.rect.bottom = b.rect.top
                player.vel_y = 0
            if player.rect.top < b.rect.bottom and player.vel_y < 0:
                player.rect.top = b.rect.bottom
                player.vel_y = 0

        '''
        for h in Haunters:
            enemy_lc=pygame.sprite.spritecollide(h,muro,False)
            for b in enemy_lc:

                if h.rect.right > b.rect.left:
                    h.rect.right = b.rect.left

                if h.rect.left < b.rect.right :
                    h.rect.left = b.rect.right

                if h.rect.bottom > b.rect.top :
                    h.rect.bottom = b.rect.top

                if h.rect.top < b.rect.bottom :
                    h.rect.top = b.rect.bottom'''

            #------------------------------------------------------

        for f in FireBalls:
            f_lc=pygame.sprite.spritecollide(f,muro,False)
            for b in f_lc:
                #p.sound.play()
                if f.rect.right > b.rect.left:
                    FireBalls.remove(f)
                if f.rect.left < b.rect.right:
                    FireBalls.remove(f)
                if f.rect.bottom > b.rect.top:
                    FireBalls.remove(f)
                if f.rect.top < b.rect.bottom:
                    FireBalls.remove(f)

        for l in LaserBeams:
            l_lc=pygame.sprite.spritecollide(l,muro,False)
            for b in l_lc:
                #p.sound.play()
                if l.rect.right > b.rect.left:
                    LaserBeams.remove(l)
                if l.rect.left < b.rect.right:
                    LaserBeams.remove(l)
                if l.rect.bottom > b.rect.top:
                    LaserBeams.remove(l)
                if l.rect.top < b.rect.bottom:
                    LaserBeams.remove(l)


        for f in FireBalls:
            f_col = pygame.sprite.spritecollide(f, Haunters, False)

            for e in f_col:
                FireBalls.remove(f)
                if e.health != 0:
                    if PowerObtained == False:
                        e.health -= 50
                    elif PowerObtained == True:
                        enemyNumber-=1
                        score+=250
                        Haunters.remove(e)
                        PotionModifier = Modifier(Potion, e.rect.x, e.rect.y)
                        ModifierOne.add(PotionModifier)

                elif e.health == 0:
                    enemyNumber-=1
                    score+=250
                    Haunters.remove(e)
                    PotionModifier = Modifier(Potion, e.rect.x, e.rect.y)
                    ModifierOne.add(PotionModifier)

        for f in FireBalls:
            f_col = pygame.sprite.spritecollide(f, Shooters, False)

            for e in f_col:
                FireBalls.remove(f)
                if e.health != 0:
                    if PowerObtained == False:
                        e.health -= 25
                    elif PowerObtained == True:
                        e.health -= 50

                elif e.health == 0:
                    enemyNumber-=1
                    score+=500
                    Shooters.remove(e)


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
                if (s.action == 0):
                    Laser = Proyectile(LaserShoot)
                    Laser.vel_x = 7
                    Laser.rect.x = s.rect.x
                    Laser.rect.y = s.rect.y
                    LaserBeams.add(Laser)
                elif (s.action == 1):
                    Laser = Proyectile(LaserShoot)
                    Laser.vel_x = -7
                    Laser.rect.x = s.rect.x
                    Laser.rect.y = s.rect.y
                    LaserBeams.add(Laser)
                s.temp = 10
                if (Laser.rect.x < 0 and Laser.rect.y < 0 and Laser.rect.y > 480 and Laser.rect.y > 480):
                    LaserBeams.remove(Laser)

        for h in Haunters:
            h_col = pygame.sprite.spritecollide(h, playerList, False)
            for e in h_col:
                player.vida -= 20
                sPlayer.update(player.vida)

                if player.vida == 0:
                    game_over = True

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

        PowerUp_col = pygame.sprite.spritecollide(player, ModifierThree, True)
        for p in PowerUp_col:
            PowerObtained = True


        mt=pygame.sprite.spritecollide(player,meta,False)
        for b in mt:
            if(enemyNumber==0):
                finMeta=True
            else:
                lc=pygame.sprite.spritecollide(player,meta,False)
                for b in lc:

                    if player.rect.top < b.rect.bottom and player.vel_y < 0:
                        player.rect.top = b.rect.bottom
                        player.vel_y = 0


        if not game_over:
            player.update()
            ModifierOne.update()
            ModifierThree.update()
            Haunters.update()
            Shooters.update()
            FireBalls.update()
            LaserBeams.update()

            win.blit(bg1,[0,0])
            texto1=fuente.render("Health: ",True,white)
            win.blit(texto1,[0,16])

            texto2=fuente.render("Score: ",True,white)
            texto3=fuente.render(str(score),True,white)
            win.blit(texto2,[416,16])
            win.blit(texto3,[453,16])

            texto1=fuente.render("Vida: ",True,white)
            win.blit(texto1,[0,16])
            #muro.draw(win)
            #meta.draw(win)
            playerList.draw(win)
            indicadores.draw(win)
            ModifierOne.draw(win)
            ModifierThree.draw(win)
            Haunters.draw(win)
            Shooters.draw(win)
            FireBalls.draw(win)
            LaserBeams.draw(win)
            if finMeta == True:
                bgm.stop()
                fin=True
            pygame.display.flip()
            reloj.tick(60)

        else:
           texto=fuente.render("GAME OVER", True, white)
           win.fill(black)
           win.blit(texto,[200, 240])
           bgm.stop()
           fin=True
           pygame.display.flip()






if __name__ == '__main__':
    main()
