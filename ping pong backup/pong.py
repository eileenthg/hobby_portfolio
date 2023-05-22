import os, sys
import pygame
import random


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
        
        if playing == False and self.light == 1:
            self.text = self.font.render(str(self.counter),1,(70,70,70))
            if self.no == 1: self.textpos = self.text.get_rect(center =  (int(SCRWIDTH * 3/4), int(SCRHALFH)))
            if self.no == 2: self.textpos = self.text.get_rect(center = (int(SCRWIDTH * 1/4), int(SCRHALFH)))
            pygame.draw.rect(background,(0,0,0), self.textpos)
            background.blit(self.text, self.textpos)
            self.light = 0

#==main code
pygame.init()
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode([SCRWIDTH, SCRHEIGHT])
#pygame.mouse.set_visible(0)
background = pygame.Surface(screen.get_size())
background = background.convert()

clock = pygame.time.Clock()
run = True

while run:
    reset = False
    background.fill((0,0,0))
    pygame.draw.rect(background,(255,255,255),(0, 0, SCRWIDTH, 36))
    pygame.draw.rect(background,(255,255,255),(0, SCRHEIGHT - 36, SCRWIDTH, 36))
    pygame.draw.rect(background,(70,70,70),(SCRHALFW - 4, 40, 18, SCRHEIGHT - 80))
    score1 = Score(1)
    score2 = Score(2)
    while not reset:
        done = False
        ball = Ball()
        paddle1 = Paddle((255,0,0))
        paddle2 = Paddle((0,128,255))
        allsprites = pygame.sprite.Group((ball, paddle1, paddle2))
        match = True
        playing = False
        while match:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    reset = True
                    match = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                    reset = True
                    match = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    match = False
                    reset = True
                
                #= match    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and playing == False:
                    playing = True
                    ball.start()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and playing == True and done == True:
                    for sprite in allsprites:
                        sprite.kill()
                    playing = False
                    match = False
            
                #= player controls
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s and playing == True:
                    paddle1.down()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w and playing == True:
                    paddle1.up()
                if event.type == pygame.KEYUP and event.key == pygame.K_s and playing == True:
                    paddle1.nodown()
                if event.type == pygame.KEYUP and event.key == pygame.K_w and playing == True:
                    paddle1.noup()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and playing == True:
                    paddle2.down()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and playing == True:
                    paddle2.up()
                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN and playing == True:
                    paddle2.nodown()
                if event.type == pygame.KEYUP and event.key == pygame.K_UP and playing == True:
                    paddle2.noup()
                
            allsprites.update()
            check1 = score1.update()
            check2 = score2.update()
            if check1 or check2: done = True
            screen.blit(background, (0,0))
            allsprites.draw(screen)
            pygame.display.flip()

pygame.quit()
