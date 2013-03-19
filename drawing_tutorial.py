# http://inventwithpython.com/pygamecheatsheet.png
import pygame
import sys
import time

from pygame.locals import *
pygame.init()

fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((640, 480))

pygame.display.set_caption('Pygame Cheat Sheet')
current_x_selection = 0
# catSurfaceObj = pygame.image.load('cat.png')
redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 255, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)



mousex, mousey = 0, 0
fontObj = pygame.font.Font('freesansbold.ttf', 32)
msg = 'Hello world!'


while True:
    windowSurfaceObj.fill(whiteColor)

    pygame.draw.polygon(
        windowSurfaceObj, greenColor, ((146, 0), (291, 106,), (236, 277)))
    pygame.draw.circle(windowSurfaceObj, blueColor, (300, 50), 20, 0)

    # pygame.draw.line(windowSurfaceObj, redColor, (mousex, 0), (mousey, 100),
    # 2)

    pixArr = pygame.PixelArray(windowSurfaceObj)
    for x in range(100, 200, 4):
        for y in range(100, 200, 4):
            pixArr[x + y][y] = redColor
    del pixArr

    msgSurfaceObj = fontObj.render(msg, False, blueColor)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (mousex, mousey)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            pass
        elif event.type == MOUSEBUTTONUP:
            if event.button in (1, 2, 3):
                msg = "mouse button clicked"
            elif event.button == 4:
                msg = "mouse scrolled up"
            elif event.button == 5:
                msg = "mouse scrolled down"

        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            current_x_selection = mousex
            pygame.draw.line(
                windowSurfaceObj, redColor, (mousex, 0), (mousex, 100), 2)

    print current_x_selection

    pygame.display.update()
    fpsClock.tick(30)
