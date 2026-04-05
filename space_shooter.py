from pygame import *
import random
mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, x, y, speed):
        super().__init__()

        self.image = transform.scale(image.load(pl_image), (75,75))
        self.pl_image = pl_image
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.k = 0

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def im(self,x,y):
        self.image = transform.scale(image.load(self.pl_image), (x,y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_a]:
            if self.rect.x >= -35:
                self.rect.x -= self.speed
            else:
                self.rect.x = 675
        if keys[K_d]:
            if self.rect.x <= 675:
                self.rect.x += self.speed
            else:
                self.rect.x = -35
    
    def shot(self):
        global bullets
        global bullet_counter
        global recharge
        keys = key.get_pressed()
        if keys[K_SPACE] and self.k == 1 and not recharge:
            self.k = 0
            bullet = Bullet('bullet.png',self.rect.x+32.5,390,7)
            bullet.im(10,20)
            bullets.append(bullet)
            bullet_counter -= 1
            if bullet_counter == 0:
                recharge = True
                bullet_counter = 15
        elif keys[K_SPACE]:
            self.k = 0
        else:
            self.k = 1


class Enemy(GameSprite):
    def move(self):
        global miss_counter
        global damage
        global health
        if self.rect.y <= 650:
            self.rect.y += self.speed / 2
        else:
            self.reset()
            miss_counter += 1

        if sprite.collide_rect(self,player):
            health -= 1
            damage = True
            self.reset()

    def reset(self):
        global min_speed
        global max_speed
        self.speed = random.randint(min_speed, max_speed)
        self.rect.x = random.randint(50,650)
        self.rect.y = -50

class Asteroid(GameSprite):
    def move(self):
        global damage
        global health
        if self.rect.y <= 650:
            self.rect.y += self.speed / 2
        else:
            self.reset()

        if sprite.collide_rect(self,player):
            health -= round_counter
            damage = True
            self.reset()

    def shot(self):
        self.health -= 1
        if self.health == 0:
            self.reset()

    def reset(self):
        global round_counter
        self.speed = random.randint(2, 3)
        self.rect.x = random.randint(50,650)
        self.rect.y = -50
        self.health = round_counter

class Bullet(GameSprite):
    def __init__(self, pl_image, x, y, speed):
        super().__init__(pl_image, x, y, speed)
        self.image = transform.scale(image.load(pl_image),(75,6))

    def move(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            del self


def Tabf():
    global Tab, Tab2
    keys = key.get_pressed()
    if keys[K_TAB] and Tab2:
        Tab2 = False
        if Tab:
            Tab = False
        else:
            Tab = True
    elif keys[K_TAB]:
        Tab2 = False
    else:
        Tab2 = True

window = display.set_mode((700,500))
display.set_caption("Шутер")
wx = 700
wy = 500
background = transform.scale(image.load("galaxy.jpg"), (wx,wy))

vis1 = 0
vis2 = 0
vision = True
damage = False
death = False
recharge = False
rec = 0
health = 10
min_speed = 2
max_speed = 4
x1 = random.randint(50,650)
x2 = random.randint(50,650)
x3 = random.randint(50,650)
x4 = random.randint(50,650)
x5 = random.randint(50,650)
x6 = random.randint(50,650)
enemy_1 = Enemy('ufo.png',0,760,8)
enemy_2 = Enemy('ufo.png',0,760,8)
enemy_3 = Enemy('ufo.png',0,760,8)
enemy_4 = Enemy('ufo.png',0,760,8)
enemy_5 = Enemy('ufo.png',0,760,8)
enemies = sprite.Group()
enemies.add(enemy_1)
enemies.add(enemy_2)
enemies.add(enemy_3)
enemies.add(enemy_4)
enemies.add(enemy_5)
for i in enemies:
    i.im(75,40)

asteroid = Asteroid('asteroid.png',0,760,8)
player = Player('rocket.png',40,420,5)
bullets = []

Tab = True
Tab2 = False
shot_counter = 0
miss_counter = -5
round_counter = 1
bullet_counter = 15
msc = 50
mmc = 5
font1 = font.SysFont('Arial',20)
font2 = font.SysFont('Arial',40)
font3 = font.SysFont('Arial',60)
mixer.music.load('space.ogg')
mixer.music.play()
clock = time.Clock()

game = True
finish = False
while game:
    window.blit(background, (0,0))

    if recharge:
        rec += 1
        if rec == 30:
            recharge = False
            rec = 0
        window.blit(recharge_str,(0,480))

    if damage:
        if vis1 == 5:
            vis1 = 0
            vis2 += 1
        else:
            vis1 += 1
        
        if vis2 == 0 or vis2 == 2 or vis2 == 4 or vis2 == 6:
            vision = True
        else:
            vision = False
        
        if vis2 == 6:
            damage = False
            vis1 = 0
            vis2 = 0

    if health == 0:
        death = True
    
    if not death and vision:
        player.update()
    
    enemies.draw(window)
    asteroid.update()
    for i in bullets:
        i.update()

    shot_counter_str = font1.render('Cчёт: ' + str(shot_counter) + '/' + str(msc), True, (255,255,255))
    miss_counter_str = font1.render('Пропущено: ' + str(miss_counter) + '/' + str(mmc), True, (255,255,255))
    health_str = font1.render('Здоровье: ' + str(health) + '/10', True, (255, 255, 255))
    round_counter_str = font1.render('Раунд ' + str(round_counter) + '/3', True, (255, 255, 255))
    bullets_counter_str_1 = font1.render('До перезарядки', True, (255,255,255))
    bullets_counter_str_2 = font1.render('осталось:' + str(bullet_counter), True, (255,255,255))
    recharge_str = font1.render('Перезарядка...', True, (255,255,255))
    pause = font3.render('Пауза', True, (255,255,255))
    YOU_NEARLY_WIN_1 = font2.render('Вы почти выиграли....', True, (255,0,0))
    YOU_NEARLY_WIN_2 = font2.render('Я вижу ваши эмоции, так что...', True, (255,255,0))
    YOU_WINNER_1 = font2.render('ВЫ ВЫИГРАЛИ', True, (200,0,200))
    YOU_WINNER_2 = font2.render('БЕЗ ПРОПУСКОВ И УРОНА!', True, (200,0,200))
    YOU_WINNER_3 = font2.render('ВЫ ВЫИГРАЛИ БЕЗ ПРОПУСКОВ!', True, (200,0,200))
    YOU_WINNER_4 = font2.render('ВЫ ВЫИГРАЛИ БЕЗ УРОНА!', True, (200,0,200))
    YOU_WIN = font2.render('ВЫ ВЫИГРАЛИ!', True, (0,255,40))
    YOU_LOSE = font2.render('Вы проиграли...', True, (255,0,0))
    YOU_LOSER = font2.render('Господи, как так можно...', True, (0,0,0))
    YOU_DIED = font2.render('Вы умерли...', True, (255,0,0))
    YOU = font2.render('ВЫ СЕРЬЁЗНО?', True, (255,0,0))
    window.blit(shot_counter_str, (10, 30))
    window.blit(miss_counter_str, (10, 70))
    window.blit(health_str, (10, 110))
    window.blit(bullets_counter_str_1, (10, 150))
    window.blit(bullets_counter_str_2, (10, 175))
    window.blit(round_counter_str, (600, 30))

    if not finish:
        Tabf()
        if Tab:
            player.shot()
            player.move()
            asteroid.move()
            for j in enemies:
                j.move()
                for i in range(len(bullets)):
                    try:
                        bullets[i].move()
                        if sprite.collide_rect(bullets[i],j):
                            shot_counter += 1
                            j.reset()
                            del bullets[i]
                            bullets.pop(i)
                    except:
                        pass

            for i in range(len(bullets)):
                try:
                    if sprite.collide_rect(bullets[i],asteroid):
                        asteroid.shot()
                        del bullets[i]
                        bullets.pop(i)
                except:
                    pass
        else:
            window.blit(pause,(270,240))
    
    if shot_counter >= 50 and shot_counter < 100:
        round_counter = 2
        msc = 100
        mmc = 10
        min_speed = 3
        max_speed = 5
    if shot_counter >= 100 and shot_counter < 150:
        round_counter = 3
        msc = 150
        mmc = 15
        min_speed = 4
        max_speed = 6
    if shot_counter >= 150:
        if miss_counter == 0:
            if health == 3:
                window.blit(YOU_WINNER_1, (200, 200))
                window.blit(YOU_WINNER_2, (100,250))
            else:
                window.blit(YOU_WINNER_3, (50, 225))
        else:
            if health == 3:
                window.blit(YOU_WINNER_4, (100, 225))
            else:
                window.blit(YOU_WIN, (210, 225))
        finish = True
    
    if miss_counter >= mmc:
        if shot_counter == 0:
            window.blit(YOU_LOSER, (100,255))
        elif shot_counter == 199 or shot_counter == 198:
            window.blit(YOU_NEARLY_WIN_1, (160,170))
            window.blit(YOU_NEARLY_WIN_2, (90,225))
            window.blit(YOU_WIN, (210,280))
        else:
            window.blit(YOU_LOSE, (210, 225))
        finish = True
    if death:
        if shot_counter == 0:
            window.blit(YOU, (210,255))
        elif shot_counter == 199 or shot_counter == 198:
            window.blit(YOU_NEARLY_WIN_1, (160,170))
            window.blit(YOU_NEARLY_WIN_2, (90,225))
            window.blit(YOU_WIN, (210,280))
        else:
            window.blit(YOU_DIED, (210, 225))
        finish = True

    



    for e in event.get():
        if e.type == QUIT:
            game = False

    clock.tick(60)
    display.update()