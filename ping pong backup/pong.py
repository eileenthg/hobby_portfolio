import os, sys
import pygame
import random

#this version uses switch statements instead of if-else.

#==protocols
def load_image(name, colorkey = None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,)
    return image, image.get_rect()

#==Static vars
SCRWIDTH = 1024
SCRHALFW = int(SCRWIDTH/2)

SCRHEIGHT = 576
SCRHALFH = int(SCRHEIGHT/2)

Ballspeed = 5


#==Classes
#note* self.start is reserved for when object is initialised.
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("ball.bmp", -1)
        self.rect.move_ip(SCRHALFW, SCRHALFH)
        self.x = SCRHALFW
        self.y = SCRHALFH
        self.movex = (random.choice([-2, -1, 1, 2])) * Ballspeed
        self.movey = (random.randrange(-10,10))
        self.run = 0
    
    def update(self):
        if self.run:
            self.move()
    
    def start(self):
        self.run = 1
        return "start"
    
    def move(self):
        self.x = self.x + self.movex
        if self.rect.colliderect(paddle1.rect):
            if self.movex < 0: self.movex = -self.movex
            if paddle1.godown:
                self.movey += int(Ballspeed / 2)
            if paddle1.goup:
                self.movey -= int(Ballspeed / 2)
        if self.rect.colliderect(paddle2.rect):
            if self.movex > 0: self.movex = -self.movex
            if paddle2.godown:
                self.movey += int(Ballspeed / 2)
            if paddle2.goup:
                self.movey -= int(Ballspeed / 2)
        self.y = self.y + self.movey
        if self.y < 36 or self.y > SCRHEIGHT - 45:
            self.movey = -self.movey
        self.rect = self.rect.move(self.movex, self.movey)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([9, 90])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.y = SCRHALFH
        self.godown = 0
        self.goup = 0
        if color == (255,0,0): self.rect.move_ip(32, SCRHALFH - 36) #player 1
        elif color == (0,128,255): self.rect.move_ip(968, SCRHALFH - 36) #player 2
        
    def update(self):
        if self.godown:
            self.y = self.y + 10
            if self.y < SCRHEIGHT - 100: self.rect.move_ip(0, 10)
            elif self.y > SCRHEIGHT - 100: self.y = self.y - 10
        if self.goup:
            self.y = self.y - 10
            if self.y > 80: self.rect.move_ip(0, -10)
            elif self.y < 80: self.y = self.y + 10
    
    def down(self):
        self.godown = 1
    
    def nodown(self):
        self.godown = 0

    def up(self):
        self.goup = 1
    
    def noup(self):
        self.goup = 0

class Score:
    def __init__(self, no):
        self.counter = 0
        self.font = pygame.font.Font(None, 100)
        self.text = self.font.render(str(self.counter), 1, (70,70, 70))
        if no == 1: self.textpos = self.text.get_rect(center = (int(SCRWIDTH * 3/4), int(SCRHALFH)))
        if no == 2: self.textpos = self.text.get_rect(center = (int(SCRWIDTH * 1/4), int(SCRHALFH)))
        background.blit(self.text, self.textpos)
        self.light = 0
        self.no = no

        
        if no == 1: self.rect = pygame.Rect(0, 0, 25, SCRHEIGHT)
        if no == 2: self.rect = pygame.Rect(SCRWIDTH - 25, 0, 25, SCRHEIGHT)
    
    def update(self):
        if self.rect.colliderect(ball.rect) and self.light == 0:
            self.counter = self.counter + 1
            self.text = self.font.render(str(self.counter), 1, (0, 255, 0))
            if self.no == 1: self.textpos = self.text.get_rect(center = (int(SCRWIDTH * 3/4), int(SCRHALFH)))
            if self.no == 2: self.textpos = self.text.get_rect(center = (int(SCRWIDTH * 1/4), int(SCRHALFH)))
            pygame.draw.rect(background,(0,0,0), self.textpos)
            background.blit(self.text, self.textpos)
            self.light = 1
            return True
        
        if self.light == 1:
            self.text = self.font.render(str(self.counter),1,(70,70,70))
            if self.no == 1: self.textpos = self.text.get_rect(center =  (int(SCRWIDTH * 3/4), int(SCRHALFH)))
            if self.no == 2: self.textpos = self.text.get_rect(center = (int(SCRWIDTH * 1/4), int(SCRHALFH)))
            pygame.draw.rect(background,(0,0,0), self.textpos)
            background.blit(self.text, self.textpos)
            self.light = 0

#==game init modules

def nun():
    pass

def game_init():
    return "reset"

def match_init():
    return "next"


#==execution switch statements
def match_off(event_type, event_key):
    arg = (event_type, event_key)
    print(arg)
    print("match off trigger")
    trigger = {
        (2, 114): game_init, #press r, resets game.
        (2, 27): quit, #press esc, quits program.
        (12, "*"): quit, #close window, quits program.
        (2, 32): ball.start #press space, starts game (returns "start") 
        }
    func = trigger.get(arg, nun)
    return func()

def match_on(event_type, event_key):
    arg = (event_type, event_key)
    print(arg)
    print("match on trigger")
    trigger = {
        (2, 114): game_init, #press r, resets game.
        (2, 27): quit, #press esc, quits program.
        (12, "*"): quit, #close window, quits program.
        (2, 119): paddle1.up,
        (3, 119): paddle1.noup,
        (2, 273): paddle2.up,
        (3, 273): paddle2.noup,
        (2, 115): paddle1.down,
        (3, 115): paddle1.nodown,
        (2, 274): paddle2.down,
        (3, 274): paddle2.nodown 
        }
    func = trigger.get(arg, nun)
    return func()

def match_done(event_type, event_key):
    arg = (event_type, event_key)
    print(arg)
    print('match done trigger')
    trigger = {
        (2, 114): game_init, #press r, resets game. note: this doesn't work.
        (2, 27): quit, #press esc, quits program.
        (12, "*"): quit, #close window, quits program.
        (2, 32): match_init #press start, next match.
        }
    func = trigger.get(arg, nun)
    return func()

#==main code
pygame.init()
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode([SCRWIDTH, SCRHEIGHT])
#pygame.mouse.set_visible(0)
pygame.event.set_blocked(None)
pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])
background = pygame.Surface(screen.get_size())
background = background.convert()


clock = pygame.time.Clock()

while True:
    background.fill((0,0,0))
    pygame.draw.rect(background,(255,255,255),(0, 0, SCRWIDTH, 36))
    pygame.draw.rect(background,(255,255,255),(0, SCRHEIGHT - 36, SCRWIDTH, 36))
    pygame.draw.rect(background,(70,70,70),(SCRHALFW - 4, 40, 18, SCRHEIGHT - 80))
    score1 = Score(1)
    score2 = Score(2)
    ball = Ball()
    paddle1 = Paddle((255,0,0))
    paddle2 = Paddle((0,128,255))
    allsprites = pygame.sprite.Group((ball, paddle1, paddle2))
    screen.blit(background, (0,0))
    allsprites.draw(screen)
    pygame.display.flip()
    state = None
    while state != "reset":
        while state != "reset":
            #clock.tick(60)
            for event in pygame.event.get():
                print(event)
                if event.type == 12: state = match_off(event.type, '*') #this could also be moved to a separate func and be quit on it's own.
                else: state = match_off(event.type, event.key)
                print(state)
            ball.update()
            screen.blit(background, (0,0))
            allsprites.draw(screen)
            pygame.display.flip()
            if state == "start": break
        while state != "reset":
            clock.tick(60)
            #must be set in game loop or time will advance too fast.
            #only needed for when object movement is noticable
            for event in pygame.event.get():
                print(event)
                if event.type == 12: state = match_on(event.type, '*')
                else: state = match_on(event.type, event.key)
                print(state)
            allsprites.update()
            check1 = score1.update()
            check2 = score2.update()
            screen.blit(background, (0,0))
            allsprites.draw(screen)
            pygame.display.flip()
            if check1 or check2: break
        while state != "reset":
            clock.tick(60)
            #must be set in game loop or time will advance too fast.
            #only needed for when object movement is noticable
            for event in pygame.event.get():
                print(event)
                if event.type == 12: state = match_done(event.type, '*')
                else: state = match_done(event.type, event.key)
                print(state)
            if state == "next": 
                ball = Ball()
                paddle1 = Paddle((255,0,0))
                paddle2 = Paddle((0,128,255))
                allsprites = pygame.sprite.Group((ball, paddle1, paddle2))
                #note: must always pack the sprites back in group after reloading or the old sprites will stay drawn without updating.
                score1.update()
                score2.update()
                screen.blit(background, (0,0))
                allsprites.draw(screen)
                pygame.display.flip()
                break
            allsprites.update()
            screen.blit(background, (0,0))
            allsprites.draw(screen)
            pygame.display.flip()