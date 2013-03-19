import pygame
import sys
import random
import time
import math
from pprint import pprint
from pygame.locals import *

debug = True


# make dummy list:
def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.
    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.localtime(ptime)


def random_date(prop, start="1/1/2008 1:30 PM", end="1/1/2013 4:50 AM"):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)

# print randomDate("1/1/2008 1:30 PM", "1/1/2013 4:50 AM", random.random())


def random_time_value_pair_maker(size=800, max_value=3000):
    scratch = []
    for x in range(size):
        t = random_date(random.random())
        num = random.randint(0, max_value)
        scratch.append((t, num))
    return sorted(scratch)

if debug:
    print "randomizing values"
qq = random_time_value_pair_maker(max_value=3)


######################
# graphics starts here

scale = 4
padding = 200 / scale
current_x_selection = 2 * padding
W = 3840 / scale
H = 2160 / scale
mouse_down = False
pygame.init()
fpsClock = pygame.time.Clock()
windowSurfaceObj = pygame.display.set_mode((W, H))
return_time = 0

pygame.display.set_caption('LineGraph')

red_color = pygame.Color(255, 0, 0)
lightRed_color = pygame.Color(200, 50, 50)
green_color = pygame.Color(0, 255, 0)
blue_color = pygame.Color(0, 0, 255)
white_color = pygame.Color(255, 255, 255)
black_color = pygame.Color(0, 0, 0)
background_color = pygame.Color(50, 50, 50)
mousex, mousey = 0, 0
msg = "0, 0"
fontObj = pygame.font.Font('freesansbold.ttf', 48)


def drawCoords(ctx):
    msgSurfaceObj = fontObj.render(msg, False, white_color)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (mousex, mousey)
    ctx.blit(msgSurfaceObj, msgRectobj)


def make_scale((d_min, d_max), (r_min, r_max)):
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


def drawPlot(ctx, data, (x, y), (width, height)):
    y_axis_place = y + height - padding
    if debug:
        pygame.draw.rect(ctx, red_color, (x, y, width, height), 1)
    pygame.draw.line(
        ctx, black_color, (x + padding, y), (x + padding, y_axis_place), 5)
    pygame.draw.line(ctx, black_color, (
        x + padding, y_axis_place), (x + width, y_axis_place), 5)

    pygame.draw.polygon(ctx, (200, 50, 50), data)


def graph_data_formatter(data, (x, y), (width, height)):
    y_axis_place = y + height - padding
    pixelsWide = width - padding
    breaks = [0 for not_used in range(pixelsWide)]

    # start_time / end_time in seconds since epoch
    start_time = time.mktime(data[0][0])
    end_time = time.mktime(data[-1][0])

    xScale = make_scale((start_time, end_time), (0, pixelsWide - 1))

    if debug:
        print "filling bins"
    # fill bins
    for i, q in enumerate(data):
        bin = int(xScale(time.mktime(qq[i][0])))
        breaks[bin] = breaks[bin] + 1

    del data

    if debug:
        print "constructing breaks"
    # transform to cumulative seen
    total = 0
    prev = breaks[0]
    graph_data = [(0, breaks[0])]
    for i in range(len(breaks) - 1):
        total = breaks[i]
        breaks[i + 1] = breaks[i + 1] + total

    yScale = make_scale((0, max(breaks)), (y_axis_place, y))

    graph_data = [(100, yScale(breaks[0]))]
    for i in range(1, len(breaks)):
        if breaks[i - 1] != breaks[i]:
            graph_data.append((100 + i, yScale(breaks[i])))

    graph_data.append((x + width, y_axis_place))
    graph_data.append((x + padding, y_axis_place))

    return graph_data

graph_upper = graph_data_formatter(qq, (padding, padding),
                                   (W - 2 * padding, H / 2 - padding))
graph_lower = graph_data_formatter(qq,
                                   (padding, H / 2),
                                   (W - 2 * padding, H / 2 - padding))

time_fn = make_scale( (2 * padding - 1, W - padding +1 ), 
                      (time.mktime(qq[0][0]), time.mktime(qq[-1][0])) )
del qq

while True:
    windowSurfaceObj.fill(background_color)

    drawPlot(windowSurfaceObj, graph_upper, (padding, padding), (W - 2 *
             padding, H / 2 - padding))

    drawPlot(windowSurfaceObj, graph_lower,
             (padding, H / 2),
             (W - 2 * padding,  H / 2 - padding))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            if mouse_down:
                if mousex > 2 * padding and mousex < W - padding:
                    current_x_selection = mousex
                    return_time = time_fn(current_x_selection)
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if mousex > 2 * padding and mousex < W - padding:
                current_x_selection = mousex
                return_time = time_fn(current_x_selection)
            mouse_down = True

    if debug:
        msg = str(return_time)
    pygame.draw.line(
        windowSurfaceObj,
        red_color,
        (current_x_selection, padding),
        (current_x_selection, H - padding),
        2)

    if debug:
        drawCoords(windowSurfaceObj)

    pygame.display.update()
    fpsClock.tick(30)
