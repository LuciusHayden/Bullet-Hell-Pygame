import pygame
import random
import math
import time

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

screen_width = 1600
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
projectiles = pygame.sprite.Group()
projectiles2 = pygame.sprite.Group()
projectiles3 = pygame.sprite.Group()
enemies = pygame.sprite.Group()

difficulty = "easy"
if difficulty == "easy":
    health = 100
    lives = 3
elif difficulty == "medium":
    health = 75
    lives = 2
else:
    health = 50
    lives = 1

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, health, damage, speed):
        super().__init__()
        self.health = health
        self.damage = damage
        self.speed = speed
        self.character = pygame.Rect(x, y, 30, 30)

class Player(Character):
    def __init__(self, x, y, health, damage, speed, lives):
        super().__init__(x, y, health, damage, speed)
        self.lives = lives
    

class Enemy(Character):
    def __init__(self, x, y, health, damage, speed, direction):
        super().__init__(x, y, health, damage, speed)
        self.direction = direction

    def move_up_down(self):
        if self.direction == "down":
            self.character.move_ip(0, self.speed)
            if self.character.y >= screen_height - 100:
                self.direction = "up"
        elif self.direction == "up":
            self.character.move_ip(0, -self.speed)
            if self.character.y <= 100:
                self.direction = "down"
        
    def move_left_right(self):
        if self.direction == "right":
            self.character.move_ip(self.speed, 0)
            if self.character.x >= screen_width - 100:
                self.direction = "left"
        elif self.direction == "left":
            self.character.move_ip(-self.speed, 0)
            if self.character.x <= 100:
                self.direction = "right"

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, size, damage, speed, target):
        super().__init__()
        self.damage = damage
        self.size = size
        self.character = pygame.Rect(x, y, size, size) 
        self.speed = speed
        self.target = target
        self.pos = pygame.math.Vector2(x, y) 

        direction_vector = pygame.math.Vector2(player.character.x - x, player.character.y - y)
        self.velocity = direction_vector.normalize() * self.speed

    def update(self):
        self.pos += self.velocity
        self.character.topleft = (int(self.pos.x), int(self.pos.y))
        if self.character.x > screen_width or self.character.x < 0 or self.character.y > screen_height or self.character.y < 0:
            self.kill()
def game_end():
    global lost_start_time
    global show_player
    
    screen.blit(lost_text, (screen_width - lost_text.get_width() - 675, 450))
    lost_start_time = pygame.time.get_ticks()
    for enemy in enemies:
        enemy.kill()
    for projectile in projectiles:
        projectile.kill()
    for projectile in projectiles2:
        projectile.kill()
    for projectile in projectiles3:
        projectile.kill()
    show_player = False      
player = Player(800, 500, health, 5, 0.5, lives)

enemy1 = Enemy(random.randint(100, 300), random.randint(600, 1000), health * 1.2, 7, 1, random.choice(["up", "down", "left", "right"]))
enemy2 = Enemy(random.randint(1200, 1500), random.randint(200, 500), health * 1.2, 7, 1, random.choice(["up", "down", "left", "right"]))
enemy3 = Enemy(random.randint(100, 300), random.randint(600, 1000), health * 1.2, 7, 1, random.choice(["up", "down", "left", "right"]))
enemy4 = Enemy(random.randint(1200, 1500), random.randint(200, 500), health * 1.2, 7, 1, random.choice(["up", "down", "left", "right"]))
enemies.add(enemy1,enemy2,enemy3,enemy4)

display_lost_life = False
show_projectiles = True
damage_cd = False
life_cd = False
cd_start = None 
lost = False
run = True
show_player = True
while run:
    run_time = pygame.time.get_ticks()
    
    screen.fill((0, 0, 0)) 

    live_lost_text = font.render(f'You have lost a live', True, (255, 0, 0))
    health_text = font.render(f'Health: {player.health}', True, (255, 0, 0))
    lives_text = font.render(f'Lives: {player.lives}', True, (255, 0, 0))
    timer_text = font.render(f'Time: {run_time // 1000}', True, (255, 0, 0))

    lost_text = font.render(f'You loose', True, (255, 0, 0))
    screen.blit(health_text, (screen_width - health_text.get_width() - 10, 10))
    screen.blit(timer_text, (10, 10))
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 200, 10))

    if not damage_cd and not life_cd:
        for enemy in enemies:
            if player.character.colliderect(enemy.character):
                player.health -= enemy.damage
                damage_cd = True
                cd_start = pygame.time.get_ticks()
        for projectile in projectiles:
            if player.character.colliderect(projectile.character):
                player.health -= projectile.damage
                projectiles.remove(projectile)
                damage_cd = True
                cd_start = pygame.time.get_ticks()
    if damage_cd:
        if pygame.time.get_ticks() - cd_start > 100:
            damage_cd = False

    if player.health <= 0:
        player.lives -= 1
        player.health = health
        lost_start_time = pygame.time.get_ticks()
        display_lost_life = True
        
    if display_lost_life == True:
        screen.blit(live_lost_text, (screen_width // 2 - live_lost_text.get_width() // 2, screen_height // 2 - live_lost_text.get_height() // 2))
        life_cd = True
        
    if display_lost_life:
        if player.lives == 0:
            life_cd = False
            display_lost_life = False
        if pygame.time.get_ticks() - lost_start_time > 3000:
            display_lost_life = False
            life_cd = False
        
    for enemy in enemies:
        if run_time % 1000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 15,10, 0.3, (player.character.x, player.character.y))
            projectiles.add(projectile)
        if run_time > 15000 and run_time % 2000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 20,15, 0.5, (player.character.x, player.character.y))
            projectiles2.add(projectile)
            enemy.damage += 1
        if run_time > 30000 and run_time % 3000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 30,20, 0.7, (player.character.x, player.character.y))
            projectiles3.add(projectile)
            enemy.damage += 2
        if run_time > 45000 and run_time % 2000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 15,10, 0.3, (player.character.x, player.character.y))
            projectiles.add(projectile)
        if run_time > 60000 and run_time % 3000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 20,15, 0.5, (player.character.x, player.character.y))
            projectiles2.add(projectile)
        if run_time > 75000 and run_time % 3000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 30,20, 0.7, (player.character.x, player.character.y))
            projectiles3.add(projectile)
    if show_player == True:
        pygame.draw.rect(screen, (0, 255, 0), player.character)
    if show_projectiles == True:
        projectiles.update()
        projectiles2.update()
        projectiles3.update()
        for projectile in projectiles:
            pygame.draw.rect(screen, (0, 0, 255), projectile.character)
        for projectile in projectiles2:
            pygame.draw.rect(screen, (100, 100, 255), projectile.character)
        for projectile in projectiles3:
            pygame.draw.rect(screen, (255, 255, 255), projectile.character)

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.character.move_ip(-1 , 0)
    if key[pygame.K_d]:
        player.character.move_ip(1, 0)
    if key[pygame.K_w]:
        player.character.move_ip(0, -1)
    if key[pygame.K_s]:
        player.character.move_ip(0, 1)
    
    for enemy in enemies:
        pygame.draw.rect(screen , (255, 0, 0), enemy.character)
        if enemy.direction in ["up", "down"]:
            enemy.move_up_down()
        elif enemy.direction in ["left", "right"]:
            enemy.move_left_right()
    
    if player.lives <= 0:
        game_end()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    pygame.display.update()

pygame.quit()
