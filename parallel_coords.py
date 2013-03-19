# http://inventwithpython.com/pygamecheatsheet.png
import pygame
import sys
import time
import math

from pygame.locals import *
pygame.init()
fpsClock = pygame.time.Clock()
s = 1 #scaler
(width, height) = (int(960 * s), int(540 * s))
padding = 50/s
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Paralell Coordinates')
debug = True

red_color = pygame.Color(255, 0, 0)
lightRed_color = pygame.Color(200, 50, 50)
green_color = pygame.Color(0, 255, 0)
blue_color = pygame.Color(0, 0, 255)
white_color = pygame.Color(255, 255, 255)
black_color = pygame.Color(0, 0, 0)
background_color = pygame.Color(50, 50, 50)
msg = 'Hello world!'
mouse_down = False
mousex, mousey = 0, 0
fontObj = pygame.font.Font('freesansbold.ttf', 32*s)



def drawCoords(ctx):
    msgSurfaceObj = fontObj.render(msg, False, blue_color)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (mousex, mousey)
    ctx.blit(msgSurfaceObj, msgRectobj)


class Axis():
    def __init__(self, title, (lo_bound, hi_bound), x):
        self.title = title
        self.lo_bound = lo_bound
        self.hi_bound = hi_bound
        self.x = x
        self.min_value = None
        self.max_value = None

    #return y value, given dimension data
    def intersect_y(self, value):
        return height/2

    def display(self):
        if self.max_value is not None:
            maxValSurface = fontObj.render(str(self.max_value), False, white_color)
            msgRectobj = maxValSurface.get_rect()
            msgRectobj.center = (self.x+20, padding*2)
            screen.blit(maxValSurface, msgRectobj)

        if self.min_value is not None:
            minValSurface = fontObj.render(str(self.min_value), False, white_color)
            msgRectobj = minValSurface.get_rect()
            msgRectobj.center = (self.x+20, height - padding*2)
            screen.blit(minValSurface, msgRectobj)


        pygame.draw.line(screen, red_color, 
            (self.x, top+padding), (self.x, bottom-padding),  2)
        msgSurfaceObj = fontObj.render(self.title, False, red_color)
        msgRectobj = msgSurfaceObj.get_rect()
        msgRectobj.center = (self.x, padding)
        screen.blit(msgSurfaceObj, msgRectobj)

def make_scale(a):
    d_min = min(a)
    d_max = max(a)
    r_min = 2 * padding
    r_max = bottom - padding
    def scaleFunction(y):
        if y < (d_min + d_max) / 2:
            m = 1
        else:
            m = -1
        x = (y * 1.0) + .0001 * m
        if d_min <= x and x <= d_max + .0001:
            d_width = d_max - d_min
            r_width = r_max - r_min
            return round(((x - d_min) / d_width * r_width) + r_min)
        if x <= d_min:
            raise Exception(str(x) + " too small")
        if d_max <= x:
            raise Exception(str(x) + " too big")
    return scaleFunction

class Chart():
    def __init__(self, axes, vectors):
        self.axes = axes
        self.vectors = vectors
        self.num_lines = len(self.vectors)
        self.starting_x = 2 * padding
        self.increments = (bottom - top - 2 * padding) / self.num_lines
        self.starting_y = 2 * padding
        
        axisData = [[] for x in range(6)]

        for row in self.vectors:
            for i in range(5):
                axisData[i].append(row[i])

        for i in range(5):
            self.axes[i].intersect_y = make_scale(axisData[i])
            self.axes[i].max_value = max(axisData[i])
            self.axes[i].min_value = min(axisData[i])



    def display(self):
        for ax in self.axes:
            ax.display()

        for line in self.vectors:
            pygame.draw.line(screen, red_color, 
                (self.starting_x, int(self.starting_y)), #from
                (self.axes[0].x, self.axes[0].intersect_y(line[0])),  1) #to
            self.starting_y += self.increments

            for i in range(4):
                pygame.draw.line(screen, red_color, 
                    (self.axes[i].x, self.axes[i].intersect_y(line[i])), #from
                    (self.axes[i+1].x, self.axes[i+1].intersect_y(line[i+1])),  1) #to



class Vectors():
    def __init__(self, column_values):
        pass

top = padding
left = padding
bottom = height - padding
right = width - padding

screen.fill(background_color)
pygame.draw.rect(screen, red_color,
    (top, left, right - padding, bottom - padding), 1)

L = [[n,-n/20,3+n/2,4+n**2,500-n] for n in range(100)]
print L

A = []
#make axx
for x in xrange(left + 200 * s, right - left, int(150*s)):
    if debug:
        print x
    A.append(Axis(str(x), (1,11), x))

c = Chart(A,L)
c.display()


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            if mouse_down:
                mousex, mousey = event.pos
                msg = "( "+str(mousex)+", "+\
                           str(mousey)+" )"
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            msg = "( "+str(mousex)+", "+\
                           str(mousey)+" )"
            mouse_down = True
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
            pygame.quit()
            sys.exit()

    if mouse_down:
        if debug:
            drawCoords(screen)
            pygame.draw.line(screen, black_color, 
                (mousex, 0), (mousex, height), 1)
            pygame.draw.line(screen, black_color, 
                (0, mousey), (width, mousey),  1)
    pygame.display.update()
    fpsClock.tick(30)

