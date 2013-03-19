from pprint import pprint
import pygame
from pygame.locals import *
import random
import math
import os.path
import tables as tb
import cPickle


background_colour = (50, 50, 50)
(width, height) = (1920/2, 1080/2)
dampen = .01

frame_count = 0
current_time = None
sorted_event_index = None
edge_rate = .05
number_of_vertices = 30
force_max = 30

red_color = pygame.Color(255, 0, 0)
lightRed_color = pygame.Color(200, 50, 50)
green_color = pygame.Color(0, 255, 0)
blue_color = pygame.Color(0, 0, 255)
white_color = pygame.Color(255, 255, 255)
black_color = pygame.Color(0, 0, 0)
background_color = pygame.Color(50, 50, 50)

mouse_sens = 3
fpsClock = pygame.time.Clock()
# h5file = tb.openFile('overflow.h5', 'r')

#input: time
#output: 

# events = []
# event_table = h5file.getNode("/", "events")

# print "loading... (should take about a minute)"
# def createSortedIndexFile():
#     sorted_index = events.argsort(order=('timestamp'))
#     cPickle.dump(sorted_index, open("index_sorted.p", "wb"))
# if not os.path.isfile("index_sorted.p"):
#     print "recreating Pickle"
#     createSortedIndexFile()
# sorted_event_index = cPickle.load(open('index_sorted.p', 'rb'))

class TagGroup():
    def __init__(self):
        self.tags = {}

    def add_tags(self, taglist):
        for i, source in enumerate(taglist):
            for target in taglist[i + 1:]:
                e = (source, target)
                if e[0] > e[1]:
                    e = (target, source)
                w = 1.0 / len(taglist)
                if e in self.tags:
                    self.tags[e] += w
                else:
                    self.tags[e] = w

    def remove_tags(self, taglist):
        for i, source in enumerate(taglist):
            for target in taglist[i + 1:]:
                e = (source, target)
                if e[0] > e[1]:
                    e = (target, source)
                w = 1.0 / len(taglist)
                if self.tags[e] == w:
                    del self.tags[e]
                else:
                    self.tags[e] -= w

class TimeFilter():
    def __init__(self, event_table, sorted_event_index):
        self.event_table = event_table
        self.sorted_event_index = sorted_event_index
        self.oldindex = 0
        self.newindex = 0
        self.isReverse = None

    def setTime(self, time):
        #binary search to find the latest index
        #that is lte this time
        self.oldindex = self.newindex
        self.newindex = self._bisect_left(time)
        if self.newindex > self.oldindex:
            self.isReverse = False
        else:
            self.isReverse = True


    def eventSequenceGenerator(self, time):
        i = self.oldindex
        if not self.isReverse:
            while i < self.newindex:
                yield self.event_table[self.sorted_event_index[i]]
                i += 1
        elif self.isReverse:
            while i > self.newindex:
                yield self.event_table[self.sorted_event_index[i]]
                i -= 1

    def _bisect_left(self, x, lo=0, hi=None):
        if hi is None:
            hi = len(self.sorted_event_index)
        while lo < hi:
            mid = (lo+hi)/2
            midval = self.event_table[self.sorted_event_index[mid]][3]
            if midval+1 <= x:
                lo = mid+1
            elif midval-1 > x: 
                hi = mid
            else:
                return mid
        return -1


# Process new events into a tag table

# tf = TimeFilter(event_table, sorted_event_index)

# for i in eventSequenceGenerator(3):
#     print i

# Vert(name, total_rep, ...)
# Edge(w,(v1,v2))


class Edge():
    def __init__(self, s, t, weight):
        self.s = s
        self.t = t
        self.weight = weight
        c = weight + 50
        self.color = (c, c, c)


    def __str__(self):
        return "("+ str(self.s) +", "+ str(self.t) +")"

    def display(self):
        pygame.draw.line(screen, self.color,
                        (self.s.x, self.s.y), (self.t.x, self.t.y),
                        int(self.weight / 15))


class Vertex():
    def __init__(self, (x, y), size, name=None):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.size = size
        self.mass = size
        self.color = lightRed_color
        self.border = (10,10,10)
        self.thickness = 0
        self.name = name
        if self.name == None:
            self.name = str(random.choice([x for x in range(100)]))

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def display(self):
        pygame.draw.circle(screen, self.color, (
            int(self.x), int(self.y)), self.size, self.thickness)
        pygame.draw.circle(screen, self.border, (
            int(self.x), int(self.y)), self.size, 1)
        fontObj = pygame.font.Font(None, max(self.size,12))
        label = fontObj.render(self.name, False, white_color)
        screen.blit(label, (self.x-label.get_width()/2, self.y-label.get_height()/2))

    def move(self):
        self.x += self.dx
        self.y += self.dy


def findvertex(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None


def spring(edge):
    pass
    _spring(edge.s,edge.t, edge.weight, pull=True)

def _spring(v1, v2, weight, pull):
    pad = v1.size + v2.size
    x_diff = v1.x - v2.x
    y_diff = v1.y - v2.y

    angle = math.atan2(y_diff, x_diff)

    dist = math.hypot(x_diff, y_diff)

    
    force = ((dist-(weight + pad*2)))**3 * .0001

    if force > force_max:
        force = force_max
    if pull:
        force =  200 + 100 * number_of_vertices

    x_force = math.cos(angle) * force
    y_force = math.sin(angle) * force

    v1.dx -= x_force
    v2.dx += x_force

    v1.dy -= y_force
    v2.dy += y_force

def repel(v1):
    for v2 in V:
        if v2 == v1:
            return
        _spring(v1,v2,350,pull=False)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('')

V = []
#presumably add the SIZE/NAME here,

#randomize position:
for n in range(number_of_vertices):
    size = random.randint(10, 50)
    name = None
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)
    vertex = Vertex((x, y), size, name)
    V.append(vertex)

# E = []
E = [Edge(V[0],V[1],50)]
for i, s in enumerate(V):
    for t in V[i+1:]:
        if random.random() > 1-edge_rate:
            E.append (Edge(s, t, s.size+t.size))

def pan(x ,y):
    for v in V:
        v.x+=x * mouse_sens
        v.y+=y * mouse_sens

selected_vertex = None
selected_bg = False
running = True
while running:
    # print fpsClock.get_fps()
    frame_count += 1
    dampen = dampen * .99
    # V.append(Vertex((width/2,height/2), 5,"w0t"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            found = findvertex(V, mouseX, mouseY)
            if found:
                selected_vertex = found
            else:
                selected_bg = True
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_vertex = None
            selected_bg = False

    screen.fill(background_color)

    if selected_vertex:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        selected_vertex.x = mouseX
        selected_vertex.y = mouseY

    if selected_bg:
        (mouseX, mouseY) = pygame.mouse.get_rel()
        if math.fabs(mouseX) + math.fabs(mouseY) < 100:
            print mouseX, mouseY
            pan(mouseX, mouseY)

    if dampen > 6.31157979432e-05:
        print dampen
        for e in E:
            spring(e)
        for v in V:
            # pygame.draw.line(screen, (0, 0, 0),
            #      (v.x, v.y), (v.x+v.dx*10, v.y+v.dy*10), 2)
            repel(v)
            if math.fabs(v.dx) > 1000:
                v.dx *= .8
            if math.fabs(v.dy) > 1000:
                v.dy *= .8
            v.dx = v.dx * dampen
            v.dy = v.dy * dampen
            v.move()

    for e in E:
        e.display()
    for v in V:
        v.display()

    

    pygame.display.flip()
    fpsClock.tick(60)
