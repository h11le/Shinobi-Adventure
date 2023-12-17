import pygame, os, random, time
from pygame.locals import *

# set up the window
WINDOWWIDTH = 64*14
WINDOWHEIGHT = 64*10 

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

FRAMERATE = 30
MAP = 'map1.txt'

def terminate():
    """Shortcut to exit the game"""
    pygame.quit()
    os._exit(1)

def load_image(filename):
    image = pygame.image.load(filename)
    image = image.convert_alpha()  
    return image

def create_list(filename):
    in_file = open(filename, "r")
    entire_list = in_file.readlines()
    for x in range(len(entire_list)):
        entire_list[x] = entire_list[x].strip()
    in_file.close()
    return entire_list
    
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, top, left):  
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        
        self.rect.top = top
        self.rect.left = left

class Moving(pygame.sprite.Sprite):
    def __init__(self, image, top, left, distance, forth, up, speed):  
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

        self.change_x = speed
        self.change_y = speed

    def update(self):
        if self.forth:
            self.rect.left += self.change_x
            self.gone += self.change_x
            if self.gone >= self.distance:
                self.forth = False
                self.back = True
                self.gone = 0
        elif self.back:
            self.rect.left -= self.change_x
            self.gone += self.change_x
            if self.gone >= self.distance:
                self.forth = True
                self.back = False
                self.gone = 0
        elif self.up:
            self.rect.top -= self.change_y
            self.gone += self.change_y
            if self.gone >= self.distance:
                self.up = False
                self.down = True
                self.gone = 0
        elif self.down:
            self.rect.top += self.change_y
            self.gone += self.change_y
            if self.gone >= self.distance:
                self.up = True
                self.down = False
                self.gone = 0

class Game():
    def __init__(self):
        self.game_over = False

        self.background = load_image('BG.png')
        self.waves = load_image('waves.png')
        self.water = load_image('water.png')
        waves_image = pygame.transform.scale(self.waves, (64,64))
        water_image = pygame.transform.scale(self.water, (64,64))

        maplist = create_list(MAP)

        self.platform_list = pygame.sprite.Group()
        self.water_list = pygame.sprite.Group()

        for x in range(WINDOWWIDTH//64):
            
            waves = Platform(waves_image, 64*8, 64*x)
            self.water_list.add(waves)
            water = Platform(water_image, 64*9, 64*x)
            self.water_list.add(water)

        for x in range(len(maplist)):
            for y in range(len(maplist[x])):
                if maplist[x][y] >= "A" and maplist[x][y] <= "Z":
                    tile = maplist[x][y].lower()
                    self.blockimage =  pygame.transform.scale(load_image(tile + '.png'), (64,64))
                    ablock = Platform(self.blockimage, 64*x, 64*y)
                    self.platform_list.add(ablock)

        #self.ablock = Moving(self.blockimage, 150, 400, 200, True, False, 4)
        #self.platform_list.add(self.ablock)

    def process_events(self, windowSurface):
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                
    def display_frame(self, windowSurface):
        
        windowSurface.fill(WHITE)
        windowSurface.blit(self.background, (0,0))
        
        if not self.game_over:
            
            #self.ablock.update()
            self.water_list.draw(windowSurface)
            self.platform_list.draw(windowSurface)
             
            pygame.display.update()
        
def main():
    """Mainline of the program"""

    pygame.init()
    mainClock = pygame.time.Clock()

    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('MAP')

    game = Game()

    while True:
        game.process_events(windowSurface)
        game.display_frame(windowSurface)
        mainClock.tick(FRAMERATE)

main()
                
