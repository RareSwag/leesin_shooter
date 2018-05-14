import pygame
import random

# Initialize game engine
pygame.init()

# Stages
START = 0
PLAYING = 1
END = 2

# Window
WIDTH = 1000
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
TITLE = "League of Lee"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Images
ship_img = pygame.image.load('assets/images/ship.png')
ship2_img = pygame.image.load('assets/images/ship_hurt.png')
ship3_img = pygame.image.load('assets/images/ship_hurty.png')
lasers_img = pygame.image.load('assets/images/comet.png')
crit_img = pygame.image.load('assets/images/crit.png')
enemy_img = pygame.image.load('assets/images/vel.png')
bomb_img = pygame.image.load('assets/images/bomb.png')
bomb1_img = pygame.image.load('assets/images/bomb1.png')
bomb2_img = pygame.image.load('assets/images/bomb2.png')
bomb3_img = pygame.image.load('assets/images/bomb3.png')
splash = pygame.image.load('assets/images/start.jpg')
back = pygame.image.load('assets/images/back.jpg')
end = pygame.image.load('assets/images/end.jpg')
ship_images = [ship_img, ship2_img, ship3_img]

# Sound
wavestart = pygame.mixer.Sound("assets/sound/wave.ogg")
explosion = pygame.mixer.Sound("assets/sound/hitvel.ogg")
grunt = pygame.mixer.Sound("assets/sound/grunt.ogg")
hitlee = pygame.mixer.Sound("assets/sound/hitlee.ogg")
hitvel = pygame.mixer.Sound("assets/sound/fart1.ogg")
shippow = pygame.mixer.Sound("assets/sound/pow.ogg")
firegirl = pygame.mixer.Sound("assets/sound/shootgirl.ogg")
firecrit = pygame.mixer.Sound("assets/sound/firecrit.ogg")

#Fonts
SCORE = pygame.font.Font("assets/fonts/score.ttf", 32)
ENDSCORE = pygame.font.Font("assets/fonts/endscore.ttf", 34)

# Setup
def setup():
    global stage, score, wave, ship

    stage = START
    soundef()
    pygame.mixer.music.play(-1)
    score = 0
    wave = 1
    ship = Ship(384, 536, ship_images)

def start(wave):
    global fleet, bombs, mobs, player, lasers
    
    if score != 0:
        wavestart.play()
    
    if wave == 1 or wave == 2:
        mob1 = Mob(128, 64, enemy_img)
        mob2 = Mob(256, 64, enemy_img)
        mob3 = Mob(384, 64, enemy_img)
        
        mobs = pygame.sprite.Group()
        mobs.add(mob1,mob2,mob3)
        
    elif wave == 3 or wave == 4:
        mob1 = Mob(128, 64, enemy_img)
        mob2 = Mob(256, 64, enemy_img)
        mob3 = Mob(384, 64, enemy_img)
        mob4 = Mob(256, 180, enemy_img)
        
        mobs = pygame.sprite.Group()
        mobs.add(mob1,mob2,mob3,mob4)
        
    elif wave == 5 or wave == 6:
        mob1 = Mob(128, 64, enemy_img)
        mob2 = Mob(256, 64, enemy_img)
        mob3 = Mob(384, 64, enemy_img)
        mob4 = Mob(192, 180, enemy_img)
        mob5 = Mob(320, 180, enemy_img)
        
        mobs = pygame.sprite.Group()
        mobs.add(mob1,mob2,mob3,mob4,mob5)

    else:
        mob1 = Mob(128, 64, enemy_img)
        mob2 = Mob(256, 64, enemy_img)
        mob3 = Mob(384, 64, enemy_img)
        mob4 = Mob(192, 180, enemy_img)
        mob5 = Mob(320, 180, enemy_img)
        
        mobs = pygame.sprite.Group()
        mobs.add(mob1,mob2,mob3,mob4,mob5)

        

    #Make sprite groups
    player = pygame.sprite.GroupSingle()
    player.add(ship)

    lasers = pygame.sprite.Group()

    bombs = pygame.sprite.Group()

    fleet = Fleet(mobs)

    

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, ship_images):
        super().__init__()

        self.speed = 3
        self.shield = 5
        shiphealth = self.shield
        
        #self.mask = pygame.mask.from_surface(self.image)
        self.image = ship_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.critcount = 0

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        crit = False
        if self.critcount <= 9:
            laser_image = lasers_img
            crit = False
            sound = shippow
        elif self.critcount >= 10:
            laser_image = crit_img
            crit = True
            sound = firecrit
        laser = Laser(laser_image, crit)
        laser.rect.centerx = self.rect.centerx - 9
        laser.rect.centery = self.rect.top
        lasers.add(laser)
        self.critcount += 1
        sound.play()
        if self.critcount > 10:
            self.critcount = 0

    def update(self, bombs):
        #Health Bars
        location = (self.rect.x - 10, self.rect.y + 40, self.shield * 10, 15)
        location2 = (self.rect.x - 11, self.rect.y + 39, (5 * 10) + 2, 17)
        color = ( -1 * ((self.shield * 51) - 255), (self.shield * 51), (self.shield * 51))

        pygame.draw.rect(screen, BLACK, location2)
        pygame.draw.rect(screen, color, location)
        
        #Check if Hit
        hit_list = pygame.sprite.spritecollide(self, bombs, True)
        mobhit_list = pygame.sprite.spritecollide(self, mobs, True)

        for hit in hit_list:
            hitlee.play()
            self.shield -= 1
            
        for mob in mobhit_list:
            hitlee.play()
            self.shield = 0

        if self.shield == 0:
            explosion.play()
            self.kill()

        #Check The Edges
        if self.rect.x >= WIDTH - 32:
            self.rect.x =  WIDTH- 32
        elif self.rect.x <= 0:
            self.rect.x = 0

        #Change The Image
        if self.shield == 5 or self.shield == 4:
            self.image = ship_images[0]
        elif self.shield == 3 or self.shield == 2:
            self.image = ship_images[1]
        elif self.shield == 1:
            self.image = ship_images[2]
    
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image, crit):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 6
        self.crit = crit

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()


    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.shield = 255
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        bomblist = [bomb_img, bomb1_img, bomb2_img, bomb3_img]
        bomb = Bomb(bomblist[random.randrange(0,3)])
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        firegirl.play()

    def update(self, lasers):
        #Get Global
        global score, wave
        
        #Health Bars
        location = (self.rect.x, self.rect.y - 40, self.shield / 3, 15)
        location2 = (self.rect.x - 1, self.rect.y - 41, (255 / 3) + 2, 17)
        color = (-1 * (self.shield - 255), self.shield, 0)

        pygame.draw.rect(screen, BLACK, location2)
        pygame.draw.rect(screen, color, location)

        #Check if Hit
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            if hit.crit == False:
                hitvel.play()
                self.shield -= random.randrange(1, 3)
                score += random.randrange(1, 3)
            elif hit.crit == True:
                self.shield -= random.randrange(5, 8)
                score += random.randrange(4, 8)

        if self.shield <= 0:
            explosion.play()
            self.kill()
            score += random.randrange(50, 150)


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= 650:
            self.kill()
            
    
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = (wave / 2) + 4
        self.bomb_rate = (wave * 2) - 120 * -1

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <= 0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

def display_stats(screen):
    #Get Global
    global score, wave
    
    # Draw Box
    location = (0, 0, 202, 77)
    pygame.draw.rect(screen, WHITE, location)
    location = (1, 1, 200, 75)
    pygame.draw.rect(screen, BLACK, location)
    location = (202, 0, 50, 38)
    pygame.draw.rect(screen, WHITE, location)
    location = (200, 1, 50, 36)
    pygame.draw.rect(screen, BLACK, location)

    #Draw Score
    score_text = SCORE.render("Score = " + str(score), 1, WHITE)
    if score >= 15000:
        score_text = SCORE.render("Score = Ur Mom", 1, WHITE)
    screen.blit(score_text, [5, 2])

    #Draw Wave
    wave_text = SCORE.render("Wave = " + str(wave), 1, WHITE)
    screen.blit(wave_text, [15, 35])


# Sound effects
def soundef():
    if stage == START:
        return pygame.mixer.music.load("assets/sound/introsong.ogg")
    elif stage == PLAYING:
        return pygame.mixer.music.load("assets/sound/godfist.ogg")
    elif stage == END:
        return pygame.mixer.music.load("assets/sound/endsong.ogg")
        
# Game loop
done = False
setup()
start(wave)

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    soundef()
                    pygame.mixer.music.play(-1)

            elif stage == PLAYING:
                pass

            elif stage == END:
                if event.key == pygame.K_SPACE:
                    setup()
                    start(wave)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot()

    if stage == PLAYING:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot()
                
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
            

        #Fill In Background
        screen.blit(back, [0, 0])
        
        # Game logic (Check for collisions, update points, etc.)
        player.update(bombs)
        lasers.update()
        mobs.update(lasers)
        bombs.update()
        fleet.update()
        if len(mobs) == 0:
            wave += 1
            start(wave)

        if len(player) == 0:
            stage = END
            soundef()
            pygame.mixer.music.play(-1)
            
            
        # Drawing code (Describe the picture. It isn't actually drawn yet.)
        lasers.draw(screen)
        player.draw(screen)
        bombs.draw(screen)
        mobs.draw(screen)
        display_stats(screen)


    if stage == START:
        screen.fill(BLACK)
        screen.blit(splash, [0, 0])

    if stage == END:
        screen.fill(BLACK)
        screen.blit(end, [0, 0])
        end_score = ENDSCORE.render("Your Final Score Was: " + str(score), 1, WHITE)
        screen.blit(end_score, [15, 15])
        if wave == 1:
            wave_score = ENDSCORE.render("You Survived " + str(wave) + " Wave", 1, WHITE)
        else:    
            wave_score = ENDSCORE.render("You Survived " + str(wave) + " Waves", 1, WHITE)
        screen.blit(wave_score, [15, 65])

        restart = ENDSCORE.render("Press 'Space' To Play Again", 1, WHITE)
        text_rect = restart.get_rect(center=(WIDTH/2, HEIGHT/2 + 275))
        screen.blit(restart, text_rect)
    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
