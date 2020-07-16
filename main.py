import pygame, math
from random import randint
pygame.font.init()
pygame.init()

win_width, win_height = 800, 600
WIN = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Space Invaders")
ICON = pygame.image.load("icon.png")
SHIP = pygame.image.load("spaceship.png")
ENEMY = pygame.image.load("ufo.png")
BULLET = pygame.transform.scale(pygame.image.load("bullet.png"), (30, 30))
pygame.display.set_icon(ICON)
BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (800, 600))


class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.cool_down = 0
        self.img = None

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.img = SHIP


class Enemy(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.img = ENEMY
        self.exist = True

    def move(self, vel):
        self.y += vel
        if self.y > 600:
            self.exist = False

class bullet:
    def __init__(self, x, y):
        self.x = x+15
        self.y = y
        self.exist = True
        self.img = BULLET
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y-=vel
        if self.y<0:
            self.exist = False


def game():

    ck = pygame.time.Clock()
    run = True

    lives = 5
    number_of_enemies = 0
    score = 0

    main_font = pygame.font.SysFont('comicsans', 50)
    p = Player(370, 460)

    player_vel = 10
    enemy_vel = 1
    bullet_vel = 2

    enemy_list = []
    bullet_list = []

    b_time = 0
    e_time = 0
    flag = 0
    level_check = 0

    def dist(ex, ey, px, py):
        return math.sqrt((ex-px)**2 + (ey-py)**2)

    def redraw():
        nonlocal number_of_enemies, lives, score, run
        #Background Draw
        WIN.blit(BG, (0, 0))

        #Font
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        number_of_enemies_label = main_font.render(f"E_Count: {number_of_enemies}", 1, (255, 255, 255))
        score_label = main_font.render(f"SCORE: {score}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(number_of_enemies_label, (win_width-number_of_enemies_label.get_width()-10, 10))
        WIN.blit(score_label, (330, 10))



        p.draw(WIN)
        print( p.x, p.y)
        
        for enemy in enemy_list:
            if dist(enemy.x+30, enemy.y+30, p.x+25, p.y+25) < 30:
                enemy_list.pop(enemy_list.index(enemy))
                score+=1
                lives-=1
                if lives == 0:
                    gameover_label = main_font.render(f"GAMEOVER", 1, (255, 255, 255))
                    WIN.blit(gameover_label, (330, 270))
                    print("gameover")
                    run = False
                    


            for bullet in bullet_list:
                if dist(bullet.x, bullet.y, enemy.x+30, enemy.y+30)<30:
                    bullet_list.pop(bullet_list.index(bullet))
                    enemy_list.pop(enemy_list.index(enemy))
                    score+=1

        if (enemy_list):
            for e in enemy_list:
                e.draw(WIN)
                e.move(enemy_vel)
                if not e.exist:
                    enemy_list.pop(enemy_list.index(e))

        if bullet_list:
            for b in bullet_list:
                b.draw(WIN)
                b.move(bullet_vel)
                if not b.exist:
                    bullet_list.pop(bullet_list.index(b))

        pygame.display.update()

    while run:
        ck.tick(60)

        if level_check!=number_of_enemies and number_of_enemies%20==0:
            level_check = number_of_enemies
            flag = 1
            
        if level_check and flag:
            enemy_vel += 1
            flag = 0

        if len(enemy_list)<5 and e_time<1:
            e = Enemy(randint(20, 750), randint(0, 100))
            enemy_list.append(e)
            number_of_enemies+=1
            e_time = 50

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if keys[pygame.K_SPACE] and b_time<1:
                b = bullet(p.x, p.y)
                bullet_list.append(b)
                b_time = 25

        b_time-=1
        e_time-=1
        
        if keys[pygame.K_LEFT] and p.x - player_vel>0:
            p.x -= player_vel
        if keys[pygame.K_RIGHT] and p.x + player_vel<750:
            p.x += player_vel
        if keys[pygame.K_UP] and p.y - player_vel>0:
            p.y -= player_vel
        if keys[pygame.K_DOWN] and p.y + player_vel<550:
            p.y += player_vel
        
        redraw()
        
game()
pygame.time.delay(3000)
