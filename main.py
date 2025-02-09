
# Made by @atialtunbayrak on github
# Enjoy!

import pygame
import random
import time
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE
)

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

HADAMART_ON = False
NORMAL_ON = False
NOT_ON = True


# Set up the display
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0,255,0)


SYSTEM_TEXT = "Good Luck :)"

SYSTEM_COLOR = GREEN

PAUSE = False
# Define the Player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center = [0,SCREEN_HEIGHT])

    def update(self, pressed_keys):
        if not HADAMART_ON and not PAUSE:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

            # Keep player on the screen
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

            if self.rect.bottom >= SCREEN_HEIGHT//2 and NORMAL_ON:
                 self.rect.bottom = SCREEN_HEIGHT//2 +1
            if self.rect.top <= SCREEN_HEIGHT//2 and NOT_ON :
                 self.rect.top = SCREEN_HEIGHT//2 -1
            # # if self.rect.bottom >= SCREEN_HEIGHT//2  and self.rect.top <= SCREEN_HEIGHT//2 : 
            # #     self.rect.bottom = (SCREEN_HEIGHT//2 -2) +  5
            # if self.rect.top <= SCREEN_HEIGHT//2  and self.rect.bottom >= SCREEN_HEIGHT//2 : 
            #     self.rect.top = (SCREEN_HEIGHT//2) -10

# Define the Enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 10)

    def update(self):
        if  not PAUSE:
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                for i in entangleds:
                    if self in i:
                        entangleds.remove(i)
            if HADAMART_ON:
                if pressed_keys[K_UP]:
                    self.rect.move_ip(0, -5)
                if pressed_keys[K_DOWN]:
                    self.rect.move_ip(0, 5)

                # Keep bullet on the screen
                if self.rect.top <= 0:
                    self.rect.top = 0
                if self.rect.bottom >= SCREEN_HEIGHT:
                    self.rect.bottom = SCREEN_HEIGHT

class Arc(pygame.sprite.Sprite):
    def __init__(self,Enemy1,Enemy2):
        super(Arc, self).__init__()
        self.surf = pygame.Surface((20, 10))
        
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        if not PAUSE:
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, playerx, playery):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect(
            center=(playerx, playery)
        )
        
        self.speed = 15  # Consistent bullet speed
    def rot_center(self,angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(angle)
        rot_rect = rot_image.get_rect(center= self.rect.center)
        return rot_image,rot_rect
    def update(self):
        if not PAUSE:
            self.rect.move_ip(self.speed, 0)
            # self.rot_center(45)
            if self.rect.right > SCREEN_WIDTH:

                self.kill()

# Create sprite groups
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


arcs = pygame.sprite.Group()
# Create Lighning

entangleds = []




# Create the player
player = Player()
all_sprites.add(player)

# Game variables
score = 0
start_time = time.time()
bullet_count = 10  # Start with 10 bullets
bullet_limit = 10 #max bullets
font = pygame.font.SysFont('Comic Sans MS', 28)

# Define game events
CREATING_ENEMY_TIME_INTERVAL = 150
EVENT_TIME_INTERVAL = 4000
ADD_BULLET_TIME = 5000
ADDENEMY = pygame.USEREVENT + 1
DOEVENT = pygame.USEREVENT + 2
ADDBULLET = pygame.USEREVENT +3

pygame.time.set_timer(ADDENEMY, CREATING_ENEMY_TIME_INTERVAL)
pygame.time.set_timer(DOEVENT, EVENT_TIME_INTERVAL)
pygame.time.set_timer(ADDBULLET, ADD_BULLET_TIME)

# Game loop
clock = pygame.time.Clock()
running = True
game_over_message_displayed = False  # Flag for game over message
falseplayer = None


cntr = 0
while running:

    if PAUSE:
        cntr += 1
        if cntr>60:
            PAUSE = False
            cntr = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDBULLET:
            bullet_count+=1
        elif event.type == DOEVENT:

            rng = random.randint(0,250)

            if rng<50:
                SYSTEM_TEXT = ""
                SYSTEM_COLOR = WHITE
                PAUSE = False

            else:
                PAUSE = True
                if not HADAMART_ON:
                    
                    if rng < 100:

                        SYSTEM_TEXT = "NOT"
                        SYSTEM_COLOR = WHITE

                        NOT_ON = not NOT_ON
                        player.rect.center = [player.rect.center[0], SCREEN_HEIGHT-player.rect.center[1]]


                    if rng >= 150 and rng <200:

                        SYSTEM_TEXT = "HADAMART!!!"
                        SYSTEM_COLOR = RED

                        HADAMART_ON = True
                        NORMAL_ON = False
                        falseplayer = Player()
                        all_sprites.add(falseplayer)

                        falseplayer.rect.center = [player.rect.center[0], (SCREEN_HEIGHT )- player.rect.center[1]]
                        #SYSTEM_TEXT = f"Falseplayer at {falseplayer.rect.centerx} and {falseplayer.rect.centery}"
                    else:

                        System_Text = "Entanglement!"
                        SYSTEM_COLOR = YELLOW
                        breakcount=  0


                        chosen = random.choice(list(enemies))
                        while chosen.rect.centerx< SCREEN_WIDTH//2:
                            chosen = random.choice(list(enemies))
                            breakcount += 1
                            if breakcount >50:
                                break

                        chosen2 = random.choice(list(enemies))

                        while chosen2 == None or chosen2 == chosen or chosen2.rect.centerx< SCREEN_WIDTH//2:
                            chosen2 = random.choice(list(enemies))
                            breakcount += 1
                            if breakcount>50:
                                break

                        chosens = (chosen,chosen2)
                        entangleds.append(chosens)


                else:
                    HADAMART_ON = False

                    SYSTEM_TEXT = "Back to Normal"
                    SYSTEM_COLOR = WHITE

                    if falseplayer != None:
                        falseplayer.kill()


    # Get pressed keys
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]:
        running = False
    if pressed_keys[K_SPACE] and bullet_count > 0:
        new_bullet = Bullet(player.rect.centerx, player.rect.centery)
        bullets.add(new_bullet)
        all_sprites.add(new_bullet)
        bullet_count -= 1

    # Update game objects
    player.update(pressed_keys)
    enemies.update()
    bullets.update()

    # Draw everything
    screen.fill(BLACK)

    pygame.draw.line(screen, (0,255,0), (0,SCREEN_HEIGHT//2), (SCREEN_WIDTH,SCREEN_HEIGHT//2), 3)



    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    entanglelines =[]
    for pairs in entangleds:

       a= pygame.draw.line(screen, (225, 255, 0),pairs[1].rect.center, pairs[0].rect.center , 2)
       entanglelines.append(a)

    # Display score and timer
    elapsed_time = int(time.time() - start_time)
    score_text = font.render(f"Score: {score}", True, YELLOW)
    time_text = font.render(f"Time: {elapsed_time}", True, YELLOW)
    bullet_text = font.render(f"Bullets: {bullet_count}", True, YELLOW)
    event_text = font.render(SYSTEM_TEXT, True, SYSTEM_COLOR)

    screen.blit(score_text, (10, 10))
    screen.blit(event_text, (SCREEN_WIDTH//2, 10))
    screen.blit(time_text, (SCREEN_WIDTH - 150, 10))
    screen.blit(bullet_text, (10, 50))


    # Check for collisions

    for i in entangleds:
        if player.rect.clipline((i[0].rect.center), (i[1].rect.center)) != ():
            if PAUSE:
                i[0].kill()
                i[1].kill()

            elif HADAMART_ON and random.randint(1,2)==1:
                SYSTEM_TEXT = "Superposition Saved You"
                PAUSE = True
                for i in enemies:
                    i.kill()
                entangleds.clear()
            else:
                player.kill()
                running = False
                game_over_message_displayed = True  # Set the flag
                game_over_text = font.render("Game Over :(", True, YELLOW)

                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25))
        


    if pygame.sprite.spritecollideany(player, enemies):
        enemy = pygame.sprite.spritecollideany(player, enemies)

        if PAUSE:
            enemy.kill()

        elif HADAMART_ON and random.randint(1,2)==1:
            SYSTEM_TEXT = "Superposition Saved You"
            for i in enemies:
                i.kill()
        else:
            player.kill()
            running = False
            game_over_message_displayed = True  # Set the flag
            game_over_text = font.render("Game Over :(", True, YELLOW)

            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25))
    

    if falseplayer !=None:
        if pygame.sprite.spritecollideany(falseplayer, enemies):
            enemy = pygame.sprite.spritecollideany(falseplayer, enemies)

            if PAUSE:
                enemy.kill()

            elif HADAMART_ON and random.randint(1,2)==1:
                SYSTEM_TEXT = "Superposition Saved You"
                for i in enemies:
                    i.kill()
            else:
                player.kill()
                running = False
                game_over_message_displayed = True  # Set the flag
                game_over_text = font.render("Game Over :(", True, YELLOW)

                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25))

    for bullet in bullets:
        enemy_hit = pygame.sprite.spritecollideany(bullet, enemies)
        if enemy_hit:
            for i in entangleds:
                    if enemy_hit in i:
                        entangleds.remove(i)
            enemy_hit.kill()
            bullet.kill()
            score += 1
            enemies.remove(enemy_hit)
            bullets.remove(bullet)


    pygame.display.flip()

    if game_over_message_displayed:  # Check the flag
        time.sleep(2)

    clock.tick(30)

pygame.quit()