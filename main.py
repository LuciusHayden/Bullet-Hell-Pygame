import pygame
import random
import math


pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

screen_width = 1800
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
projectiles = pygame.sprite.Group()
projectiles2 = pygame.sprite.Group()
projectiles3 = pygame.sprite.Group()
projectiles4 = pygame.sprite.Group()
projectiles5 = pygame.sprite.Group()
allProjectiles = pygame.sprite.Group()

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
    for projectile in projectiles4:
        projectile.kill()
    for projectile in projectiles5:
        projectile.kill()
    show_player = False      

player = Player(screen_height // 2, screen_width // 2, health, 5, 1, lives)

enemy1 = Enemy(random.randint(100, 300), random.randint(600, 1000), health * 1.2, 7, 1, random.choice(["up", "down", "left", "right"]))
enemy2 = Enemy(random.randint(1200, 1500), random.randint(200, 500), health * 1.2, 7, 1, random.choice(["up", "down", "left", "right"]))
enemy3 = Enemy(random.randint(100, 300), random.randint(600, 1000), health * 1.2, 7, 1, random.choice(["up", "down", "left", "right"]))
enemy4 = Enemy(random.randint(1200, 1500), random.randint(200, 500), health * 1.2, 7, 1, random.choice(["up", "down", "left", "right"]))
enemy5 = Enemy(random.randint(750, 850), random.randint(450, 550), health * 1.2, 7, 1, random.choice(["up", "down", "left", "right"]))
enemies.add(enemy1,enemy2,enemy3,enemy4, enemy5)

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
#Draws needed text
    live_lost_text = font.render(f'You have lost a live', True, (255, 0, 0))
    health_text = font.render(f'Health: {player.health}', True, (255, 0, 0))
    lives_text = font.render(f'Lives: {player.lives}', True, (255, 0, 0))
    timer_text = font.render(f'Time: {run_time // 1000}', True, (255, 0, 0))

    lost_text = font.render(f'You loose', True, (255, 0, 0))
    screen.blit(health_text, (screen_width - health_text.get_width() - 10, 10))
    screen.blit(timer_text, (10, 10))
    screen.blit(lives_text, (screen_width - lives_text.get_width() - 200, 10))

#Handles not taking damage to quickly after taking damage
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
        if player.character.x > screen_width or player.character.x < 0 or player.character.y > screen_height or player.character.y < 0:
            player.health -= 1
            damage_cd = True
            cd_start = pygame.time.get_ticks()
    if damage_cd:
        if pygame.time.get_ticks() - cd_start > 200:
            damage_cd = False
#Handles losing lives
    if player.health <= 0:
        player.lives -= 1
        player.health = health
        lost_start_time = pygame.time.get_ticks()
        display_lost_life = True
#Prints the text for losing life      
    if display_lost_life == True:
        screen.blit(live_lost_text, (screen_width // 2 - live_lost_text.get_width() // 2, screen_height // 2 - live_lost_text.get_height() // 2))
        life_cd = True
#Handles stopping the text for losing life after 3 seconds or if your game is over    
    if display_lost_life:
        if player.lives == 0:
            life_cd = False
            display_lost_life = False
        if pygame.time.get_ticks() - lost_start_time > 3000:
            display_lost_life = False
            life_cd = False



#Handles the projectiles
#multiple projectile types at the same time from all enemies


    for enemy in enemies:
        if run_time % 1000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 15,10, 0.8, (player.character.x, player.character.y))
            projectiles.add(projectile)
            allProjectiles.add(projectile)
        if run_time > 15000 and run_time % 2000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 20,15, 0.5, (player.character.x, player.character.y))
            projectiles2.add(projectile)
            allProjectiles.add(projectile)
            enemy.damage += 1
        if run_time > 30000 and run_time % 3000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 30,20, 0.5, (player.character.x, player.character.y))
            projectiles3.add(projectile)
            allProjectiles.add(projectile)
            enemy.damage += 2
        if run_time > 45000 and run_time % 2000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 15,10, 0.3, (player.character.x, player.character.y))
            projectiles.add(projectile)
            allProjectiles.add(projectile)
        if run_time > 60000 and run_time % 3000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 20,15, 0.5, (player.character.x, player.character.y))
            projectiles2.add(projectile)
            allProjectiles.add(projectile)
        if run_time > 75000 and run_time % 3000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 30,20, 0.7, (player.character.x, player.character.y))
            projectiles3.add(projectile)
            allProjectiles.add(projectile)
        if run_time > 90000 and run_time % 5000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 15,3, 1.3, (player.character.x, player.character.y))
            projectiles4.add(projectile)
            allProjectiles.add(projectile)
        if run_time > 90000 and run_time % 1000 == 0:
            projectile = Projectile(enemy.character.x, enemy.character.y, 10,5, 0.8, (player.character.x, player.character.y))
            projectiles5.add(projectile)
            allProjectiles.add(projectile)
#handles showing the player and the projectiles which is useful for other functions
    if show_player == True:
        pygame.draw.rect(screen, (0, 255, 0), player.character)
# updates the projectile locations and draws them into the screen ONLY if show_projectiles is true
    if show_projectiles == True:
        allProjectiles.update()
        for projectile in projectiles:
            pygame.draw.rect(screen, (0, 0, 255), projectile.character)
        for projectile in projectiles2:
            pygame.draw.rect(screen, (100, 100, 255), projectile.character)
        for projectile in projectiles3:
            pygame.draw.rect(screen, (255, 255, 255), projectile.character)
        for projectile in projectiles4:
            pygame.draw.rect(screen, (255, 100, 100), projectile.character)
        for projectile in projectiles5:
            pygame.draw.rect(screen, (100, 255, 255), projectile.character)


#handles the movement of the player
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.character.move_ip(-1 , 0)
    if key[pygame.K_d]:
        player.character.move_ip(1, 0)
    if key[pygame.K_w]:
        player.character.move_ip(0, -1)
    if key[pygame.K_s]:
        player.character.move_ip(0, 1)
#Draws the enemies and handles their movement
    for enemy in enemies:
        pygame.draw.rect(screen , (255, 0, 0), enemy.character)
        if enemy.direction in ["up", "down"]:
            enemy.move_up_down()
        elif enemy.direction in ["left", "right"]:
            enemy.move_left_right()

#Handles the game ending
    if player.lives <= 0:
        game_end()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    pygame.display.update()

pygame.quit()
