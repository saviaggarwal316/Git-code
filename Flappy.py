import random
import sys        #use to exit programme
import pygame
from pygame.locals import *     #basic pygame imports

#global variable for game
FPS = 32    #frames per seconds
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = "FlappyBird/gallery/sprite/bird.png"
BACKGROUND = "FlappyBird/gallery/sprite/background.png"
PIPE = "FlappyBird/gallery/sprite/pipe.png"

def welcomeScreen():
    """
    show welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #if user clicks cross button, quit game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if user press space or up key, start the game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return 
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey ))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    # create 2 random pipe for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #my list of upper pipes
    upperPipes = [{'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']}, {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[0]['y']}]
    #my list of lower pipes
    lowerPipes = [{'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']}, {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[1]['y']}]

    pipeVelx = -4          #vel = velocity
    playerVely = -9
    playerMaxVely = 10
    PlayerMinVely = -8
    PlayerAccy = 1
    playerFlapAccV = -8       #velocity while flapping
    playerFlapped = False     #its true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()      
            if event.type == KEYDOWN and (event.key==K_SPACE and event.key==K_UP):
                if playery > 0:
                    playerVely = playerFlapAccV
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        crashtest = isCollide(playerx, playery, upperPipes, lowerPipes) #this function will return true when player is crashed
        if crashtest:
            return
        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score +=1
                print(f'Your score is {score}')
                GAME_SOUNDS['points'].play()

        if playerVely < playerMaxVely and not playerFlapped:
            playerVely += PlayerAccy

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx
        # add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


        #if pipe is out of the screen , remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)  

        #lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))  

        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True
    

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False

def getRandomPipe():
    """
    generate positions of two pipe for blitting on the screen (one bottom straight, one top rotated)
    """
    pipeHieght = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHieght - y2 + offset
    pipe = [{'x': pipex, 'y': -y1}, {'x': pipex, 'y': y2}]     #uper pipe and lower pipe
    return pipe




if __name__ == "__main__":
    pygame.init()              #initialize pygame's module
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy game by Savi')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('FlappyBird/gallery/sprite/zero.png').convert_alpha(),
        pygame.image.load('FlappyBird/gallery/sprite/one.png').convert_alpha(),
        pygame.image.load('FlappyBird/gallery/sprite/two.png').convert_alpha(),
        pygame.image.load('FlappyBird/gallery/sprite/three.png').convert_alpha(),
        pygame.image.load('FlappyBird/gallery/sprite/four.png').convert_alpha(),
        pygame.image.load('FlappyBird/gallery/sprite/five.png').convert_alpha(),
        pygame.image.load('FlappyBird/gallery/sprite/six.png').convert_alpha(),
        pygame.image.load('FlappyBird/gallery/sprite/seven.png').convert_alpha(),
        pygame.image.load('FlappyBird/gallery/sprite/eight.png').convert_alpha(),
        pygame.image.load('FlappyBird/gallery/sprite/nine.png').convert_alpha()
        )

    GAME_SPRITES['message'] = pygame.image.load('FlappyBird/gallery/sprite/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('FlappyBird/gallery/sprite/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), pygame.image.load(PIPE).convert_alpha())

    GAME_SOUNDS['die'] = pygame.mixer.music.load('FlappyBird/gallery/sounds/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.music.load('FlappyBird/gallery/sounds/hit.mp3')
    GAME_SOUNDS['points'] = pygame.mixer.music.load('FlappyBird/gallery/sounds/points.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.music.load('FlappyBird/gallery/sounds/swoosh.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.music.load('FlappyBird/gallery/sounds/wing.mp3')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

while True:
    welcomeScreen()  #shoe welcome to user until he/she presses a button
    mainGame()      #this is the main game function







        







