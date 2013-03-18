import pygame
import random
import math
import os.path
import tables as tb
import cPickle


background_colour = (255, 255, 255)
(width, height) = (400, 400)
dampen = .01
elasticity = 0.75
fpsClock = pygame.time.Clock()
spread = 3
vertex_padding = 0
frame_count = 0
current_time = None
sorted_event_index = None

h5file = tb.openFile('overflow.h5', 'r')

#input: time
#output: 

events = []
event_table = h5file.getNode("/", "events")

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



# class Edge():
#     def __init__(self, (s, t), weight):
#         self.s = s
#         self.t = t
#         self.weight = weight
#         self.color = (0, 0, 255)

# class Vertex():
#     def __init__(self, (x, y), size):
#         self.x = x
#         self.y = y
#         self.dx = 0
#         self.dy = 0
#         self.size = size
#         self.mass = size
#         self.color = (0, 0, 255)
#         self.thickness = 2

#     def __str__(self):
#         return "(" + str(self.x) + ", " + str(self.y) + ")"

#     def display(self):
#         pygame.draw.circle(screen, self.color, (
#             int(self.x), int(self.y)), self.size, self.thickness)

#     def move(self):
#         self.x += self.dx
#         self.y += self.dy

# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption('')

# number_of_vertices = 50
# V = []
# # V = [vertex((50, height / 2), 30),
# #                 vertex((300, height / 2), 30)]
# for n in range(number_of_vertices):
#     size = random.randint(10, 20)
#     x = random.randint(size, width - size)
#     y = random.randint(size, height - size)
#     vertex = Vertex((x, y), size)
#     V.append(vertex)


# selected_vertex = None
# running = True
# while running:
#     # print fpsClock.get_fps()
#     frame_count += 1
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             (mouseX, mouseY) = pygame.mouse.get_pos()
#             selected_vertex = findvertex(V, mouseX, mouseY)
#         elif event.type == pygame.MOUSEBUTTONUP:
#             selected_vertex = None

#     # if selected_vertex:
#     #     (mouseX, mouseY) = pygame.mouse.get_pos()
#     #     dx = mouseX - selected_vertex.x
#     #     dy = mouseY - selected_vertex.y
#     #     selected_vertex.angle = 0.5 * math.pi + math.atan2(dy, dx)
#     #     selected_vertex.speed = math.hypot(dx, dy) * 0.1

#     screen.fill(background_colour)

#     for i, vertex in enumerate(V):
#         # for vertex2 in V[i + 1:]:
#             # attract(vertex, vertex2)
#         vertex.dx = (vertex.dx / number_of_vertices) * dampen
#         vertex.dy = (vertex.dy / number_of_vertices) * dampen

#     for vertex in V:
#         vertex.dx
#         vertex.dy
#         vertex.move()
#         vertex.display()

#     # for vertex in V:
#     #     vertex.move()
#     #     vertex.bounce()
#     #     vertex.display()

#     pygame.display.flip()
#     fpsClock.tick(60)
