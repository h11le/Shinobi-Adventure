# This is Hien Le's culminating project of ICS 4U1 2020
# The due date was on June 12, 2020
# The game's name is SHINOBI ADVENTURE (inspired by Natuto)

import pygame, os, random, time
from pygame.locals import *

# set up the window
WINDOWWIDTH = 64*14
WINDOWHEIGHT = 64*10

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255,0,0)
YELLOW = (255,200,0)

# set up the frame rate
FRAMERATE = 35

# the player's properties
RUNSPEED = 20
BARLENGTH = 140

# OTHER PROPERTIES
MOVINGSPEED = 4
CHA_IMG_NUM = 10 #Number of images for character's motion 
BUL_IMG_NUM = 4 #Number of images for bullet's motion
MON_IMG_NUM = 2 #Number of images for monster's motion
BOSS_IMG_NUM = 3 #Number of images for boss's motion
COIN_IMG_NUM = 8 #Number of images for coin's motion
MAP_NUM = 5 #Number of maps
BAT_NUM = 20 #Number of bats

def terminate():
    """Shortcut to exit the game"""
    pygame.quit()
    os._exit(1)

def create_list(filename):
    """Return a list from a text file"""
    in_file = open(filename, "r")
    entire_list = in_file.readlines()
    for x in range(len(entire_list)):
        entire_list[x] = entire_list[x].strip()
    in_file.close()
    return entire_list

def record(score, alist, filename):
    """Record the high scores and rewrite the text file with new scores"""
    if score > alist[len(alist)-1]:
        for x in range(len(alist)):
            if score >= alist[len(alist)-1-x]:
                temp = len(alist)-1-x
        for x in range(len(alist)-temp):
            if x != len(alist) - 1:
                alist[len(alist)-1-x] = alist[len(alist)-1-x-1]
        alist[temp] = score

        out_file = open(filename, "w")
        for x in range(len(alist)):
            out_file.write(str(alist[x])+"\n")
        out_file.close()

def load_image(filename):
    """Shortcut to load an image"""
    image = pygame.image.load(filename)
    image = image.convert_alpha()  
    return image

def onscreen(windowSurface, image):
    """Display the image on the screen"""
    windowSurface.blit(image, (0,0))

def display_restart(windowSurface, won, score):
    """Display the ending screen before going back to Home"""
    if won:
        texts = ["You won! ;)", "Your score is " + str(score), "You're going back to Home in a few seconds"]
    if not won:
        texts = ["You died! :P", "Your score is " + str(score), "You're going back to Home in a few seconds"]
    basicFont = pygame.font.SysFont('calibri', 35)
    text = basicFont.render('', True, YELLOW, None)
    textRect = text.get_rect()
    textRect.centerx = windowSurface.get_rect().centerx - 100
    textRect.centery = windowSurface.get_rect().centery - 50
    for x in texts:
        text = basicFont.render(x, True, YELLOW, None)
        textRect.centery += 50
        windowSurface.blit(text, textRect)
    
class Button(pygame.sprite.Sprite):
    def __init__(self, image, top, left):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left
        self.inside = False
    
class Interact():
    def __init__(self, windowSurface):
        self.newgame = False
        self.menu = True
        self.info = False
        self.score = False
        self.mute = False

        # LOAD THE IMAGES
        self.menu_img = load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/Menu.png')
        self.info_img = load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/Instruction.png')
        self.score_img = load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/Scores.png')

        # LOAD THE IMAGES OF BUTTONS
        self.play1 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/PlayButt1.png'), (220//3,235//3))
        self.play2 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/PlayButt2.png'), (220//3,235//3))
        self.info1 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/InfoButt1.png'), (220//3,235//3))
        self.info2 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/InfoButt2.png'), (220//3,235//3))
        self.score1 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/ScoreButt1.png'), (220//3,235//3))
        self.score2 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/ScoreButt2.png'), (220//3,235//3))
        self.music1 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/MusicButt1.png'), (220//3,235//3))
        self.music2 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/MusicButt2.png'), (220//3,235//3))
        self.music3 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/MusicButt3.png'), (220//3,235//3))
        self.home1 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/HomeButt1.png'), (220//3,235//3))
        self.home2 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/HomeButt2.png'), (220//3,235//3))
        self.replay1 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/ReplayButt1.png'), (220//3,235//3))
        self.replay2 = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/ReplayButt2.png'), (220//3,235//3))
        
        self.buttons_list = pygame.sprite.Group()
        self.highscores = create_list('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/HighScore.txt')

    def update(self):
        if self.menu:
            # THE HOME PAGE, ONLY 4 BUTTONS ARE ALLOWED TO DISPLAYED
            self.buttons_images = [self.play1, self.info1, self.score1, self.music1]
            for x in range(len(self.buttons_images)):    
                if self.buttons_images[x] == self.music1 and self.mute == True:
                    # WHITE BUTTON FOR SOUND OFF 
                    button = Button(self.music3, 170, 425 + x*100)
                else:
                    button = Button(self.buttons_images[x], 170, 425 + x*100)
                self.buttons_list.add(button)

        elif self.info or self.score:
            # THE INSTRUCTION AND HIGH SCORES PAGES HAVE 1 BUTTON TO GO BACK TO HOME
            button = Button(self.home1, 55, 765)
            self.buttons_list.add(button)

    def process_events(self, windowSurface):
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons_list:        
                    if button.image == self.info2 and button.inside:
                        self.menu = False
                        self.score = False
                        self.info = True
                        self.buttons_list.empty()
                        
                    elif button.image == self.score2 and button.inside:
                        self.menu = False
                        self.score = True
                        self.info = False
                        self.buttons_list.empty()

                    elif button.image == self.home2 and button.inside:
                        self.menu = True
                        self.score = False
                        self.info = False
                        self.buttons_list.empty()

                    elif button.image == self.music2 and button.inside:
                        self.mute = not self.mute

                    if button.image == self.play2 and button.inside:
                        self.newgame = True
                        
    def run_logic(self):
        # GETTING THE MOUSE POSITION ON THE SCREEN AND DETERMINE IF IT IS ON THE BUTTON OR NOT
        mouse = pygame.mouse.get_pos()
        for button in self.buttons_list:
            if button.rect.left < mouse[0] < button.rect.right and button.rect.top < mouse[1] < button.rect.bottom:
                if button.image == self.play1:
                    button.image = self.play2
                elif button.image == self.info1:
                    button.image = self.info2
                elif button.image == self.score1:
                    button.image = self.score2
                elif button.image == self.music1 or button.image == self.music3:
                    button.image = self.music2
                elif button.image == self.home1:
                    button.image = self.home2
                elif button.image == self.replay1:
                    button.image = self.replay2         
                button.inside = True

            else:
                if button.image == self.play2:
                    button.image = self.play1
                elif button.image == self.info2:
                    button.image = self.info1
                elif button.image == self.score2:
                    button.image = self.score1
                elif button.image == self.home2:
                    button.image = self.home1
                elif button.image == self.replay2:
                    button.image = self.replay1
                elif self.mute and button.image == self.music2:
                    button.image = self.music3
                elif not self.mute and button.image == self.music2:
                    button.image = self.music1
                button.inside = False
                    
    def display(self, windowSurface):
        # DISPLAYING THE SCREENS WITH UPDATED INFO
        if self.menu:
            onscreen(windowSurface, self.menu_img)
        elif self.info:
            onscreen(windowSurface, self.info_img)
        elif self.score:
            onscreen(windowSurface, self.score_img)
            basicFont = pygame.font.SysFont('Arial', 70)
            score = basicFont.render('', True, BLACK, None)
            scoreRect = score.get_rect()
            scoreRect.top = 100
            scoreRect.left = WINDOWWIDTH//2 - 60
            for x in self.highscores:
                score = basicFont.render(x, True, BLACK, None)
                scoreRect.centery += 80
                windowSurface.blit(score, scoreRect)
        self.buttons_list.draw(windowSurface)
        pygame.display.update()

def movement(action):
    """Return a list of images describing a motion of the character"""
    alist = []
    if action == "Idle":
        width = 232
        height = 439
    elif action == "Run":
        width = 363
        height = 458
    elif action == "Dead":
        width = 482
        height = 498
    elif action == "Throw":
        width = 377
        height = 451
    for x in range(CHA_IMG_NUM):
        image = pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + str(action) + "_M_" + str(x) + ".png"), (int(width*0.25), int(height*0.25)))
        alist.append(image)
    return alist
        
class Player(pygame.sprite.Sprite):
    """Defining the motion of character"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.actions = ["Idle", "Run", "Throw", "Dead"]
        
        for x in range(len(self.actions)):
            self.actions[x] = movement(self.actions[x])

        # INDEX FOR EACH LIST OF MOVEMENTS IN SELF.ACTIONS
        # 0 - IDLING
        # 1 - RUN - right, left arrows
        # 2 - THROW - space bar
        # 3 - DEAD
        
        self.index = 0
        self.image = self.actions[0][self.index]
        
        self.rect = self.image.get_rect()
        self.rect.top = 320
        self.rect.left = 0

        self.change_x = 0
        self.change_y = 0

        self.runL = False
        self.runR = False
        self.jumpup = False
        self.idleR = True
        self.idleL = False
        self.throw = False
        self.killed = False

        self.bar = BARLENGTH
        self.barcolor = GREEN

        self.score = 0
            
    def update(self, platform_list):
        
        self.gravity()

        # INTERACTION OF THE CHARACTER WITH THE COLLIDED BLOCKS

        self.rect.left += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)

        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.top += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)

        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
         
    def gravity(self):
        if self.change_y == 0:
            self.change_y = 4
        else:
            self.change_y += 1

    def animation(self):
        self.index += 1
        if self.index > 9:
            self.index = 0
        
    def jump(self, platform_list):
        self.rect.top += 2
        platform_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        self.rect.top -= 2
        if len(platform_hit_list) > 0:
            self.change_y = -20.5
        
    def runLeft(self):
        self.change_x = -RUNSPEED
        self.image = pygame.transform.flip(self.actions[1][self.index], True, False)
        self.animation()

    def runRight(self):
        self.change_x = RUNSPEED
        self.image = self.actions[1][self.index]
        self.animation()

    def throw_kunai(self):
        if self.idleR:
            self.image = self.actions[2][self.index]    
        else:
            self.image = pygame.transform.flip(self.actions[2][self.index], True, False)
        self.animation()

    def dead(self):
        if self.idleR:
            self.image = self.actions[3][self.index]    
        else:
            self.image = pygame.transform.flip(self.actions[3][self.index], True, False)
        self.animation()
        
    def idle(self, right):
        self.change_x = 0
        if right == True:
            self.image = self.actions[0][self.index]
        elif right == False:
            self.image = pygame.transform.flip(self.actions[0][self.index], True, False)
        self.animation()

class Platform(pygame.sprite.Sprite):
    """Define the motion of blocks"""
    def __init__(self, image, top, left, distance, forth, up):  
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.top = top
        self.rect.left = left

        self.distance = distance
        self.forth = forth
        self.back = False
        self.up = up
        self.down = False
        self.gone = 0
        
    def update(self, player):
        # MOVING BACK AND FORTH
        if self.forth:
            self.rect.left += MOVINGSPEED
            self.gone += MOVINGSPEED
            if self.gone >= self.distance:
                self.forth = False
                self.back = True
                self.gone = 0
            if player.rect.bottom == self.rect.top and self.rect.left - 15 <= player.rect.left < self.rect.right:
                player.rect.left += MOVINGSPEED

        elif self.back:
            self.rect.left -= MOVINGSPEED          
            self.gone += MOVINGSPEED
            if self.gone >= self.distance:
                self.forth = True
                self.back = False
                self.gone = 0

            if player.rect.bottom == self.rect.top and self.rect.left - 15 <= player.rect.left < self.rect.right:
                player.rect.left -= MOVINGSPEED
                
        #MOVING UP AND DOWN     
        elif self.up:
            self.rect.top -= MOVINGSPEED
            self.gone += MOVINGSPEED
            if self.gone >= self.distance:
                self.up = False
                self.down = True
                self.gone = 0

            if player.rect.bottom == self.rect.top and self.rect.left - 15 <= player.rect.left < self.rect.right:
                player.rect.top -= MOVINGSPEED
                
        elif self.down:
            self.rect.top += MOVINGSPEED
            self.gone += MOVINGSPEED
            if self.gone >= self.distance:
                self.up = True
                self.down = False
                self.gone = 0
        
            if player.rect.bottom == self.rect.top and self.rect.left - 15 <= player.rect.left < self.rect.right:
                player.rect.top += MOVINGSPEED
                
class Kunai(pygame.sprite.Sprite):
    """Defining the motion of the kunai"""
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.flyingRight = False
        self.flyingLeft = False
        
    def update(self):
        if self.flyingRight:
            self.rect.left += 20
        elif self.flyingLeft:
            self.rect.left -= 20

class Bullets(pygame.sprite.Sprite):
    """Defining the motion of the bullets/fires"""
    def __init__(self, name, speed):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.motion = []
        for x in range(BUL_IMG_NUM):
            if name == "Z":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (45,45)))
            if name == "X":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (55,55)))
                
        self.image = self.motion[self.index]
        self.rect = self.image.get_rect()
        self.speed = speed
        self.goingR = False
        
    def animation(self):
        self.index += 1
        if self.index > 3:
            self.index = 0
    
    def update(self):
        self.animation()
        if self.goingR:
            self.rect.left += self.speed
        elif not self.goingR:
            self.rect.left -= self.speed
            self.image = pygame.transform.flip(self.motion[self.index], True, False)
    
class Enemies(pygame.sprite.Sprite):
    """Defining the motion of the enemy"""
    def __init__(self, name, bottom, left, distance, forth, speed):
        pygame.sprite.Sprite.__init__(self)
        self.next_frame = time.time()
        self.motion = []
        for x in range(MON_IMG_NUM):
            if name == "A":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (401//4,249//4)))
            if name == "B":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (817//12,884//12)))
            if name == "C":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (505//7,610//7)))
            if name == "D":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (553//10,411//10)))
            if name == "E":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (459//7,507//7)))
            if name == "F":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (496//5,390//5)))
            if name == "G":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (376//6,500//6)))
            if name == "H":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (427//5,496//5)))
            if name == "I":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (827//11,905//11)))
            if name == "J":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (683//8,611//8)))
            if name == "K":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (540//7,459//7)))
            if name == "L":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (369//5,369//5)))
            if name == "M":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (654//7,534//7)))
            if name == "N":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (1214//10,787//10)))
            if name == "O":
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (451//6,508//6)))
            
        self.index = 0
        self.image = self.motion[self.index]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.left = left

        self.distance = distance
        self.forth = forth
        self.speed = speed
        self.gone = 0
        
    def animation(self):
        ready = time.time()
        if ready - self.next_frame >= 0.25:
            self.next_frame = time.time()
            self.index += 1
            if self.index > 1:
                self.index = 0
            
    def update(self):
        if self.forth:
            self.image = pygame.transform.flip(self.motion[self.index], True, False)
            if self.distance != 0:
                self.rect.left += self.speed
                self.gone += self.speed
                if self.gone >= self.distance:
                    self.gone = 0
                    self.forth = False
                
        elif not self.forth:
            self.image = self.motion[self.index]
            if self.distance != 0:
                self.rect.left -= self.speed
                self.gone += self.speed
                if self.gone >= self.distance:
                    self.gone = 0
                    self.forth = True        
        self.animation()   
                
class Boss(pygame.sprite.Sprite):
    """Defining the motion of the boss"""
    def __init__(self, name, top, left, distance, up, speed):
        pygame.sprite.Sprite.__init__(self)
        self.next_frame = time.time()
        self.motion = []
        for x in range(BOSS_IMG_NUM):
            self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + name + str(x+1) + '.png'), (473//2,468//2)))
        
        self.index = 0
        self.image = self.motion[self.index]
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left

        self.distance = distance
        self.gone = 0
        self.up = up
        self.speed = speed
        
        self.attacked = False
        self.destroyed  = False
        
        self.bar = BARLENGTH
        self.barcolor = GREEN

        self.showtime = False
        
    def animation(self):
        if self.attacked:
            self.index = 2
        else:
            ready = time.time()
            if ready - self.next_frame >= 0.25:
                self.next_frame = time.time()
                self.index += 1
                if self.index > 1:
                    self.index = 0
                    
    def update(self):
        # BEING DISPLAYED WHEN THE PLAYER REACHED 4/5 OF THE MAP
        if self.showtime:
            if not self.destroyed:
                self.animation()
                self.image = self.motion[self.index]
                if self.attacked == True:
                    self.attacked = False
                if not self.up:
                    self.rect.top += self.speed
                    self.gone +=  self.speed
                    if self.gone >= self.distance:
                        self.gone = 0
                        self.up = True  
                if self.up:
                    self.rect.top -= self.speed
                    self.gone +=  self.speed
                    if self.gone >= self.distance:
                        self.gone = 0
                        self.up = False

class Coin(pygame.sprite.Sprite):
    """Defining the motion of the COIN"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rotate_time = time.time()
        self.index = 0
        self.motion= []
        for x in range(COIN_IMG_NUM):
            if x != 4:
                self.motion.append(pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + "coin_0" + str(x+1) + '.png'), (25,25)))
        self.image = self.motion[self.index]
        self.rect = self.image.get_rect()

    def animation(self):
        ready = time.time()
        if ready - self.rotate_time >= 0.1:
            self.rotate_time = time.time()
            self.index += 1
            if self.index > 6:
                self.index = 0

    def update(self):
        self.animation()
        self.image = self.motion[self.index]

class Tool(pygame.sprite.Sprite):
    """Defining the motion of the TOOL/DECORATION"""
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.gained = False

class Game():
    def __init__(self, windowSurface, music_off):
        self.game_over = False

        self.firetime = time.time()
        self.firetime1 = time.time()

        self.player = Player()

        #Groups of Sprites
        self.platform_list = pygame.sprite.Group()
        self.kunai_list = pygame.sprite.Group()
        self.moving_blocks = pygame.sprite.Group()
        self.enemies_list = pygame.sprite.Group()
        self.shooters_list = pygame.sprite.Group()
        self.bullets_list = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()
        self.coins_list = pygame.sprite.Group()
        self.tools_list = pygame.sprite.Group()
        self.decoration_list = pygame.sprite.Group()
        
        self.surface_list = []
        self.shooting_land_list = []
        
        #Images of the tile set
        self.background = load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/BG.png')
        self.decoration = [pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/1.png'), (133//2,65//2)),
                           pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/2.png'), (133//2,65//2)),
                           pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/3.png'), (73//1,46//1)),
                           pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/4.png'), (73//1,47//1)),
                           pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/5.png'), (49//1,41//1)),
                           pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/6.png'), (50//1,41//1)),
                           pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/7.png'), (90//2,54//2)),
                           pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/8.png'), (282//2,301//2)),
                           pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/9.png'), (282//2,275//2))]

        # LOADING A COMPLETE MAP FROM 5 SMALL PIECES
        for num in range(MAP_NUM):
            a_map = create_list("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + 'map' + str(num+1) + '.txt')
            for x in range(len(a_map)):
                for y in range(len(a_map[x])):
                    if a_map[x][y] >= "A" and a_map[x][y] <= "Z":
                        block = a_map[x][y].lower()
                        blockimage =  pygame.transform.scale(load_image("/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/" + block + '.png'), (64,64))
                        a_block = Platform(blockimage, 64*x, 64*y + WINDOWWIDTH*num, 0, False, False)
                        self.platform_list.add(a_block)

                        if num == 0 and y == 0:
                            self.left_boundary = a_block.rect.left
                        elif num == 4 and y == 13:
                            self.right_boundary = a_block.rect.right

                        if a_map[x][y] in ["A","B","M","N"]: # SETTING DECORATION FOR THESE KINDS OF BLOCKS
                            rannum = random.randrange(0,5)
                            if rannum == 1:
                                index = random.randrange(0,len(self.decoration))
                                decor = Tool(self.decoration[index])
                                decor.rect.bottom = 64*x
                                decor.rect.left = 64*y + WINDOWWIDTH*num
                                self.decoration_list.add(decor)
                            if rannum == 3:
                                index = random.randrange(3,9)
                                decor = Tool(self.decoration[index])
                                decor.rect.bottom = 64*x
                                decor.rect.left = 64*y + WINDOWWIDTH*num + 10
                                self.decoration_list.add(decor)

                    # DETERMINE THE SURFACE WHERE ENEMIES CAN STAND ON
                    # MAPS ARE BASED ON 64X64 BLOCKS
                    if a_map[x][y] == "A":
                        surface_prop = ()
                        surface_prop += (64*x,)
                        surface_prop += (64*y + WINDOWWIDTH*num,)
                        width = 0
                        done = False
                        for block in range(y+1, len(a_map[x])):
                            if not done:
                                if a_map[x][block] != "0":
                                    width += 64
                                elif a_map[x][block] == "0":
                                    done = True
                        if width > 64:
                            surface_prop += (width,)
                            self.surface_list.append(surface_prop)

                    # THE BLOCKS WHERE THE SHOOTERS STAND ON
                    elif a_map[x][y] == "N" and a_map[x][y+1] == "O":
                        land_prop = ()
                        land_prop += (64*x,)
                        land_prop += (64*y + WINDOWWIDTH*num,)
                        self.shooting_land_list.append(land_prop)

                    # THE MOVING B&F, U&D BLOCKS
                    elif a_map[x][y] == "*":
                        blockimage =  pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/b.png'), (int(64*1.75),int(64*1.75)))
                        moving_block = Platform(blockimage, 64*x, 64*y + WINDOWWIDTH*num - 25, 300, False, True)
                        self.platform_list.add(moving_block)
                        self.moving_blocks.add(moving_block)
                        
                    elif a_map[x][y] == "#":
                        blockimage =  pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/b.png'), (int(64*1.5),int(64*1.5)))
                        moving_block = Platform(blockimage, 64*x, 64*y + WINDOWWIDTH*num, 200, True, False)
                        self.platform_list.add(moving_block)
                        self.moving_blocks.add(moving_block)
                        
        self.down_boundary = WINDOWHEIGHT # => TO TRACK IF THE PLAYER FALLS OUT FROM THE MAP
        
        #Kunai image
        self.kunai_image = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/Kunai.png'), (65, 15))
        
        #Enemies
        self.enemies_name = ["B", "C", "D", "E", "H", "I", "J", "K", "L"]
        for x in range(2, len(self.surface_list)):
            bottom = self.surface_list[x][0] + 5
            distance = self.surface_list[x][2]
            speed = random.randrange(2,6)
            rannum = random.randrange(0,2)
            if rannum == 0:
                forth = True
                left = self.surface_list[x][1]
            else:
                forth = False
                left = self.surface_list[x][1] + distance
            ranname = random.randrange(len(self.enemies_name))
            name = self.enemies_name[ranname]  
            enemy = Enemies(name, bottom, left, distance, forth, speed)
            self.enemies_list.add(enemy)

        for x in range(len(self.shooting_land_list)):
            bottom = self.shooting_land_list[x][0]
            left = self.shooting_land_list[x][1]
            name = "G"  
            enemy = Enemies(name, bottom, left, 0, False, 0)
            self.enemies_list.add(enemy)
            self.shooters_list.add(enemy)

        for x in range(BAT_NUM):
            top = random.randrange(-200, 200)
            left = random.randrange(0, WINDOWWIDTH*5)
            distance = random.randrange(100, 200)
            speed = random.randrange(2, 5)
            name = "A"
            forth = True
            enemy = Enemies(name, top, left, distance, forth, speed)
            self.enemies_list.add(enemy)

        # THE BOSS  
        self.boss = Boss("Y", -64*3 , WINDOWWIDTH*5 + 100, 500, False, 5)

        # AVATARS, LIFE BARS FOR THE PLAYER AND BOSS ON THE SCREEN
        self.player_avt = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/Avatar1.png'), (45, 40))
        self.player_avt_rect = self.player_avt.get_rect()
        self.player_avt_rect.top = 10
        self.player_avt_rect.left = 10

        self.boss_avt = pygame.transform.flip(pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/Avatar2.png'), (60, 60)), True, False)
        self.boss_avt_rect = self.boss_avt.get_rect()
        self.boss_avt_rect.top = 50
        self.boss_avt_rect.left = 0

        # TOOLS THAT AID THE PLAYER
        self.kunaitool = Tool(pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/Tool1.png'), (50, 50)))
        self.tools_list.add(self.kunaitool)
        rannum = random.randrange(0, len(self.surface_list)//1.5)
        self.kunaitool.rect.bottom = self.surface_list[rannum][0] - 50
        self.kunaitool.rect.left = self.surface_list[rannum][1]

        self.healthtool = Tool(pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/Tool2.png'), (100, 100)))
        self.tools_list.add(self.healthtool)
        rannum = random.randrange(len(self.surface_list)//1.5, len(self.surface_list))
        self.healthtool.rect.bottom = self.surface_list[rannum][0] - 50
        self.healthtool.rect.left = self.surface_list[rannum][1]

        # A LIST OF HIGH SCORES 
        self.scores_list = create_list('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/HighScore.txt')
        for x in range(len(self.scores_list)):
            self.scores_list[x] = int(self.scores_list[x])

        # MUSIC AND SOUNDS
        self.soundnames = ['/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_Coin.wav', 
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_Damage.wav', 
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_GO1.wav',
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_GO2.wav', 
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_Heal.wav', 
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_Hurt1.wav',
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_Hurt2.wav', 
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_Jump.wav',
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_LevelUp.wav',
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_MouseClick.wav',
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_PickUp.wav',
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_Shot.wav',
                           '/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_Sound_Victory.wav',]

        for x in range(len(self.soundnames)):
            self.soundnames[x] = pygame.mixer.Sound(self.soundnames[x])

        pygame.mixer.music.load('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/_GameMusic.wav')
        self.PlayMusic = not music_off
        
        if self.PlayMusic:
            pygame.mixer.music.play(-1 , 0.0)

        self.x = 0
    def process_events(self, windowSurface):
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if not self.game_over or self.player.killed or self.boss.destroyed: 
                if event.type == KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.runL = True
                        self.player.runR = False

                    elif event.key == pygame.K_RIGHT:
                        self.player.runR = True
                        self.player.runL = False

                    elif event.key == pygame.K_UP:
                        self.player.jumpup = True

                    elif event.key == K_SPACE:
                        if self.kunaitool.gained:
                            self.player.throw = True
                
                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        terminate()
                    if event.key == pygame.K_LEFT and self.player.change_x < 0:
                        self.player.runL = False
                        self.player.idleR = False
                        self.player.idleL = True
                        
                    elif event.key == pygame.K_RIGHT and self.player.change_x > 0:
                        self.player.runR = False
                        self.player.idleL = False
                        self.player.idleR = True

                    elif event.key == K_SPACE:
                        if self.kunaitool.gained:
                            if self.player.idleR:
                                right_kunai = Kunai(self.kunai_image)
                                right_kunai.flyingRight = True
                                right_kunai.rect.centerx = self.player.rect.centerx + 75
                                right_kunai.rect.centery = self.player.rect.centery - 25
                                self.kunai_list.add(right_kunai)
                                
                            if self.player.idleL:
                                left_kunai = Kunai(pygame.transform.flip(self.kunai_image, True, False))
                                left_kunai.flyingLeft = True
                                left_kunai.rect.centerx = self.player.rect.centerx - 50
                                left_kunai.rect.centery = self.player.rect.centery - 25
                                self.kunai_list.add(left_kunai)
                
    def run_logic(self):
        scroll = [0, 0] # => NEEDED TO MOVE EVERYTHING ON THE SCREEN RELATIVELY TO THE PLAYER
        
        if not self.game_over or self.boss.destroyed or self.player.killed:

            # BOUNDARIES FOR THE PLAYER
            if self.player.rect.left < self.left_boundary:
                self.player.rect.left = self.left_boundary

            elif self.player.rect.right > self.right_boundary:
                self.player.rect.right = self.right_boundary

            # THE GAME ENDS WHEN:
            # 1. THE PLAYER IS FALLING OUT FROM THE MAP
            # 2. THE PLAYER'S OR THE BOSS'S BARLENGTH IS 0
            if self.player.bar <= 0 or self.boss.bar <= 0 or self.player.rect.bottom >= self.down_boundary:
                if self.boss.bar <= 0:
                    self.boss.destroyed = True
                elif self.player.bar <= 0 or self.player.rect.bottom >= self.down_boundary:
                    self.player.killed = True
                self.game_over = True
                record(self.player.score, self.scores_list, "/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/HighScore.txt")

            # COLORS FOR STAGES OF BARLENGTH
            elif self.player.bar >= BARLENGTH:
                self.player.bar = BARLENGTH
            elif self.player.bar > 70:
                self.player.barcolor = GREEN
            elif 35 < self.player.bar <= 70:
                self.player.barcolor = YELLOW
            elif self.player.bar <= 35:
                self.player.barcolor = RED
            if 35 < self.boss.bar <= 70:
                self.boss.barcolor = YELLOW
            elif self.boss.bar <= 35:
                self.boss.barcolor = RED

            # WHEN THE PLAYER IS NEAR TO THE END OF THE MAP
            if self.player.rect.left - self.left_boundary >= 3600:
                self.boss.showtime = True

            # RELATIVE DISTANCE THAT THE PLAYER MOVES
            scroll[0] += (self.player.rect.x - scroll[0] - WINDOWWIDTH//5)
            scroll[1] += (self.player.rect.y - scroll[1] - WINDOWHEIGHT//2)

            # AND EVERYTHING HAS TO FOLLOW THAT
            for block in self.platform_list:
                block.rect.left -= scroll[0]
                block.rect.top -= scroll[1]
            for enemy in self.enemies_list:
                enemy.rect.left -= scroll[0]
                enemy.rect.top -= scroll[1]
            for bullet in self.bullets_list:
                bullet.rect.left -= scroll[0]
                bullet.rect.top -= scroll[1]
            for bullet in self.boss_bullets:
                bullet.rect.left -= scroll[0]
                bullet.rect.top -= scroll[1]
            for kunai in self.kunai_list:
                kunai.rect.left -= scroll[0]
                kunai.rect.top -= scroll[1]
            for coin in self.coins_list:
                coin.rect.left -= scroll[0]
                coin.rect.top -= scroll[1]
            for tool in self.tools_list:
                if not tool.gained:
                    tool.rect.left -= scroll[0]
                    tool.rect.top -= scroll[1]
            for decor in self.decoration_list:
                decor.rect.left -= scroll[0]
                decor.rect.top -= scroll[1]
                
            self.left_boundary -= scroll[0]
            self.right_boundary -= scroll[0]
            self.down_boundary -= scroll[1]

            self.player.rect.left -= scroll[0]
            self.player.rect.top -= scroll[1]

            self.boss.rect.left -= scroll[0]
            self.boss.rect.top -= scroll[1]

            # CHECK IF THE PLAYER EARNS THE THROWING SKILL
            did_touch1 = pygame.sprite.collide_rect(self.player, self.kunaitool)
            if did_touch1:
                if self.PlayMusic:
                    self.soundnames[4].play()
                self.kunaitool.gained = True
                self.kunaitool.image = pygame.transform.scale(load_image('/Users/hienle/Downloads/OLD_MAC/ICS4U1/Mei/Tool11.png'), (75, 75))
                self.kunaitool.rect.top = 10
                self.kunaitool.rect.left = 64*12.65

            # CHECK IF THE PLAYER GETS THE MEDKIT OR NOT
            if not self.healthtool.gained:
                did_touch2 = pygame.sprite.collide_rect(self.player, self.healthtool)
                if did_touch2:
                    if self.PlayMusic:
                        self.soundnames[4].play()
                    self.healthtool.gained = True
                    self.tools_list.remove(self.healthtool)
                    self.player.bar += 100
                    if self.player.bar > 70:
                        self.player.barcolor = GREEN

            # CHECK IF IT'S TIME FOR SHOOTERS SHOOTING
            readyshoot = time.time()             
            if readyshoot - self.firetime >= 1.5:
                 self.firetime = time.time()
                 for shooter in self.shooters_list:
                    if shooter.index == 1:
                        bullet = Bullets("Z", 15)
                        self.bullets_list.add(bullet)
                        bullet.rect.centerx = shooter.rect.centerx
                        bullet.rect.centery = shooter.rect.centery

            # CHECK IF THE PLAYER IS SHOT BY FIRES
            for fire in self.bullets_list:
                hurt = pygame.sprite.collide_rect(self.player, fire)
                if hurt:
                    if self.PlayMusic:
                        self.soundnames[5].play()
                    self.player.bar -= 5
                    self.bullets_list.remove(fire)

            # SAME CHECKING TIME PROCESS FOR THE BOSS'S SHOOTING 
            if self.boss.showtime:
                boss_shoot = time.time()   
                if boss_shoot - self.firetime1 >= 1:
                    if self.PlayMusic:
                        self.soundnames[11].play()
                    self.firetime1 = time.time()
                    bullet1 = Bullets("X", 15)
                    self.boss_bullets.add(bullet1)
                    bullet1.rect.top = self.boss.rect.top - 10
                    bullet1.rect.left = self.boss.rect.left

                    bullet2 = Bullets("X", 15)
                    self.boss_bullets.add(bullet2)
                    bullet2.rect.top = self.boss.rect.bottom + 10
                    bullet2.rect.left = self.boss.rect.left

            for fire in self.boss_bullets:
                hurt = pygame.sprite.collide_rect(self.player, fire)
                if hurt:
                    if self.PlayMusic:
                        self.soundnames[5].play()
                    self.player.bar -= 20
                    self.boss_bullets.remove(fire)

            # CHECK FOR THE COLLISION BETWEEN THE PLAYER AND ENEMIES
            for enemy in self.enemies_list:
                did_collide = pygame.sprite.collide_rect(self.player, enemy)

                # IF THE PLAYER IS NOT JUMPING ON THE ENEMIES, HIS BARLENGTH GOES DOWN
                if did_collide and self.player.change_y <= 0:
                    if self.PlayMusic:
                        self.soundnames[5].play()
                    self.player.bar -= 0.5


                # IF HE IS JUMPING ON THEIR HEADS, HE CAN ELIMINATE THEM
                elif did_collide and self.player.change_y > 0:
                    if self.PlayMusic:
                        self.soundnames[5].play()
                    acoin = Coin()
                    self.coins_list.add(acoin)
                    acoin.rect.x = enemy.rect.x - 25
                    acoin.rect.y = enemy.rect.y
                    self.enemies_list.remove(enemy)
                    if enemy in self.shooters_list:
                        self.shooters_list.remove(enemy)

                # CHECK THE COLLISION BETWEEN KUNAI AND ENEMY, IF YES, ELIMINATE BOTH OF THEM
                for kunai in self.kunai_list:
                    gothit = pygame.sprite.collide_rect(kunai, enemy)
                    if gothit:
                        if self.PlayMusic:
                            self.soundnames[5].play()
                        acoin = Coin()
                        self.coins_list.add(acoin)
                        acoin.rect.x = enemy.rect.x - 25
                        acoin.rect.y = enemy.rect.y
                        self.enemies_list.remove(enemy)
                        if enemy in self.shooters_list:
                            self.shooters_list.remove(enemy)
                        self.kunai_list.remove(kunai)

            # CHECK THE COLLISION BETWEEN KUNAIS AND THE BOSS, IF YES, ELIMINATE THE KUNAI
            for kunai in self.kunai_list:
                attacked = pygame.sprite.collide_rect(kunai, self.boss)
                if attacked:
                    if self.PlayMusic:
                        self.soundnames[1].play()
                    self.boss.attacked = True
                    self.player.score += 20
                    self.boss.bar -= 1
                    self.kunai_list.remove(kunai)

            # CHECK THE COLLISION BETWEEN THE PLAYER AND THE COIN, IF YES, SCORE IS GAINED, COIN DISAPPEARS
            for coin in self.coins_list:
                gained = pygame.sprite.collide_rect(coin, self.player)
                if gained:
                    if self.PlayMusic:
                        self.soundnames[0].play()
                    self.coins_list.remove(coin)
                    self.player.score += 10
                
    def display_frame(self, windowSurface):
        if not self.game_over:
            # self.x and rela_x are about to get the background moving infinitely
            rela_x = self.x % self.background.get_rect().width
            if not self.player.killed or not self.boss.destroyed:
                # DISPLAYING THE BACKGROUND
                windowSurface.blit(self.background, (rela_x - self.background.get_rect().width,0))
                if rela_x < WINDOWWIDTH:
                    windowSurface.blit(self.background, (rela_x,0))
                self.x -= 1

                # UPDATE EVERTHING
                for block in self.moving_blocks:
                    block.update(self.player)  
                for akunai in self.kunai_list:
                    akunai.update()
                for enemy in self.enemies_list:
                    enemy.update()
                for bullet in self.bullets_list:
                    bullet.update()
                for bullet in self.boss_bullets:
                    bullet.update()
                for coin in self.coins_list:
                    coin.update()
                    
                self.player.update(self.platform_list)
                self.boss.update()

                # DISPLAYING MOTION FOR EACH ACTION OF THE PLAYER
                if self.player.runL:
                    self.player.runLeft()
                elif self.player.runR:
                    self.player.runRight()
                    
                elif self.player.jumpup:
                    if self.PlayMusic:
                        self.soundnames[7].play()
                    self.player.jump(self.platform_list)
                    self.player.jumpup = False

                elif self.player.throw:
                    self.player.throw_kunai()
                    if self.player.index == 9:
                        self.player.throw = False

                elif self.player.idleR:
                    self.player.idle(True)
                elif self.player.idleL:
                    self.player.idle(False)

                # DISPLAYING EVERYTHING ON THE SCREEN
                self.platform_list.draw(windowSurface)
                self.decoration_list.draw(windowSurface)
                self.kunai_list.draw(windowSurface)
                self.enemies_list.draw(windowSurface)
                self.bullets_list.draw(windowSurface)
                self.coins_list.draw(windowSurface)
                self.tools_list.draw(windowSurface)
                
                # DISPLAYING THE AVATAR OF THE PLAYER
                windowSurface.blit(self.player.image, self.player.rect)
                windowSurface.blit(self.player_avt, self.player_avt_rect)
                pygame.draw.rect(windowSurface, WHITE, [65, 25, 150, 20])
                pygame.draw.rect(windowSurface, self.player.barcolor, [70, 30, self.player.bar, 10])


                # DISPLAYING THE BOSS AND ITS AVATAR WHEN IT'S THE RIGHT TIME
                if self.boss.showtime:
                    self.boss_bullets.draw(windowSurface)
                    windowSurface.blit(self.boss.image, self.boss.rect)
                    windowSurface.blit(self.boss_avt, self.boss_avt_rect)
                    pygame.draw.rect(windowSurface, WHITE, [65, 75, 150, 20])
                    pygame.draw.rect(windowSurface, self.boss.barcolor, [70, 80, self.boss.bar, 10])


                # DISPLAYING THE SCORES GAINED
                basicFont = pygame.font.SysFont('arial', 30)
                displayscores = "Scores: " + str(self.player.score)
                text1 = basicFont.render(displayscores, True, BLACK, None)
                textRect1 = text1.get_rect()
                textRect1.topleft = (670, 35)
                windowSurface.blit(text1, textRect1)

        pygame.display.update()

    def display_ending(self, windowSurface):        
        if self.player.killed: # WHEN LOSING
            self.player.index = 8
            pygame.mixer.music.stop()
            windowSurface.fill(BLACK)
            self.player.dead()
            windowSurface.blit(self.player.image, self.player.rect)
            display_restart(windowSurface, False, self.player.score)
            if self.PlayMusic:
                self.soundnames[2].play()
            
        elif self.boss.destroyed: # WHEN WINNING
            pygame.mixer.music.stop()
            windowSurface.fill(WHITE)
            self.player.idle(True)
            windowSurface.blit(self.player.image, self.player.rect)
            display_restart(windowSurface, True, self.player.score)
            if self.PlayMusic:
                self.soundnames[12].play()
   
        pygame.display.update()
        pygame.event.pump()
        pygame.time.wait(5000)
        
def main():
    """Mainline of the program"""
    pygame.init()
    mainClock = pygame.time.Clock()

    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('Shinobi Adventure')

    while True:
        interact = Interact(windowSurface)
        # WAITING UNTIL THE USER PRESSES THE PLAY BUTTON
        while not interact.newgame:
            interact.process_events(windowSurface)
            interact.update()
            interact.run_logic()
            interact.display(windowSurface)

        # INSTANTIATE A OBJECT OF THE GAME CLASS (A NEW GAME)
        game = Game(windowSurface, interact.mute)
        while not game.game_over:
            game.process_events(windowSurface)
            game.run_logic()
            game.display_frame(windowSurface)
            mainClock.tick(FRAMERATE)
        game.display_ending(windowSurface)

main()
