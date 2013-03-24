"""
Keybindings:
v = add 1 (V)ertex
t = add (T)en vertices
e = add an (E)dge
click to pan
grab a node and hold left ctrl to move it faster!!
"""
import pygame
from pygame.locals import *
import random
import math
# import os.path

background_colour = (50, 50, 50)
(width, height) = (1920, 1000)

"""prints interesting info"""
debug = False

"""this is how smushy the animations happen"""
dampen = 0.01

"""the rate at which the dampening increases after
    adding an edge or a node, or calling shake
    0 means none"""
dampen_decrease = .1

"""pad_scaler: 4 is big, 2.5 is cozy"""
pad_scaler = 2.5

"""can increase the visual size of nodes and edges"""
view_size_scaler = 1

"""can fill in the number of v,e to begin with"""
number_of_vertices = 0
number_of_edges = 0
edge_rate = .01

"""reduce if there's lots of vibrations"""
force_max = 30

"""controls panning speed"""
mouse_sens = .4

"""dont change these:"""
name_list = ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "Integer", "nec", "odio", "Praesent"]

monokai_bg = pygame.Color(34, 34, 34)
monokai_orange = pygame.Color(255, 151, 60)
monokai_purple = pygame.Color(145, 84, 188)
monokai_white = pygame.Color(235, 249, 243)
monokai_green = pygame.Color(152, 224, 35)
monokai_blue = pygame.Color(71, 192, 230)
# monokai_green = pygame.Color()
red_color = pygame.Color(255, 0, 0)
green_color = pygame.Color(0, 255, 0)
blue_color = pygame.Color(0, 0, 255)
white_color = pygame.Color(255, 255, 255)
black_color = pygame.Color(0, 0, 0)

background_color = monokai_bg
vertex_color = monokai_purple
vertex_boarder_color = monokai_blue
word_color = monokai_white
edge_color = monokai_blue
selected_color = monokai_orange
debug_color = monokai_green

# h5file = tb.openFile('overflow.h5', 'r')

#input: time
#output: 

# events = []
# event_table = h5file.getNode("/", "events")




class GraphPlotPanel():
    def __init__(self):
        self.selected_bg = False
        self.selected_vertex = None
        self.hovered_vertex = None
        self.running = True
        self.frame_count = 0
        self.dampen = dampen
        self.dampen_decrease = 1 - dampen_decrease
        self.E = []
        self.V = []
        self.view_size_scaler = view_size_scaler
        self.mouse_sens = mouse_sens
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        self.info_font = pygame.font.SysFont("monospace", 20)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Graph Visualizer')

    def shake(self):
        self.dampen = dampen
        # for v in self.V:
        #     touching = self.findvertex(v.x, v.y)
        #     if touching is not None:
        #         e = Edge(v, touching, 20)
        #         self.E.append(e)
        # for v in self.V:
        #     m = random.choice([1, -1])
        #     v.dx = m * len(self.V) * 500
        #     m = random.choice([1, -1])
        #     v.dy = m * len(self.V) * 500

    def findvertex(self, x, y):
        for v in self.V:
            if math.hypot(v.x - x, v.y - y) <= v.size * self.view_size_scaler:
                return v
        return None

    def spring(self, edge):
        self._spring(edge.s, edge.t, edge.weight, edge=True)

    def _spring(self, v1, v2, weight, edge):
        pad = 4 * ((v1.size + v2.size) + len(self.V))
        x_diff = v1.x - v2.x
        y_diff = v1.y - v2.y
        angle = math.atan2(y_diff, x_diff)
        dist = math.hypot(x_diff, y_diff)
        # if dist < width/3 or edge:
        force = 10 * (dist - pad)
        if force > force_max:
            force = force_max
        if edge:
            force = 20 * (dist - pad / 2)
        x_force = math.cos(angle) * force
        y_force = math.sin(angle) * force
        v1.dx += x_force
        v2.dx -= x_force
        v1.dy += y_force
        v2.dy -= y_force

    def repel(self, v1):
        for v2 in self.V:
            if v2 == v1:
                return
            self._spring(v1, v2, 30, edge=False)

    def pan(self, x, y):
        for v in self.V:
            v.x += x * self.mouse_sens
            v.y += y * self.mouse_sens

    # def buildRandomGraph(self, number_of_vertices, edge_rate):
    #     for n in range(self.):
    #         size = random.choice([k for k in range(5, 25, 5)])
    #         v = Vertex(size)
    #         self.V.append(v)

    def add_node(self):
        self.dampen = dampen
        size = random.choice([k for k in range(10, 50, 5)])
        v = Vertex(size, str(size))
        self.V.append(v)

    def add_edge(self):
        self.dampen = dampen
        if len(self.V) > 1:
            edges = random.sample(self.V, 2)
            e = Edge(edges[1], edges[0], 20)
            self.E.append(e)

    def calculate_positions(self):
        for e in self.E:
            self.spring(e)
        for v in self.V:
            if debug:
                pygame.draw.line(self.screen, monokai_green,
                                (v.x, v.y), (v.x + v.dx * 3, v.y + v.dy * 3), 3)
            # if self.dampen > 1e-05:
            self.repel(v)
            if math.fabs(v.dx) > 1000:
                v.dx *= .7
            if math.fabs(v.dy) > 1000:
                v.dy *= .7
            v.dx = v.dx * self.dampen
            v.dy = v.dy * self.dampen
            v.move()

    def run(self):
        while(self.running):
            
            self.frame_count += 1
            self.dampen *= self.dampen_decrease
            for event in pygame.event.get():
                #checking pressed keys
                keys = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_s]:
                        self.shake()
                    if keys[pygame.K_v]:
                        self.add_node()
                    if keys[pygame.K_t]:
                        for x in range(10):
                            self.add_node()
                    if keys[pygame.K_e]:
                        if event.mod & KMOD_SHIFT:
                            for x in range(10):
                                self.add_edge()
                        else:
                            self.add_edge()
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    self.selected_vertex = self.findvertex(mouseX, mouseY)
                    if self.selected_vertex:
                        self.selected_vertex.border_color = selected_color
                    else:
                        self.selected_bg = True
                # elif event.type == pygame.MOUSEBUTTONUP:
                #     # if self.selected_vertex:
                #     #     self.selected_vertex.border_color = vertex_boarder_color
                #     self.selected_vertex = None
                #     self.selected_bg = False
                # elif event.type == pygame.MOUSEMOTION:
                #     (mouseX, mouseY) = pygame.mouse.get_pos()
                #     found = self.findvertex(mouseX, mouseY)
                #     if found:
                #         self.hovered_vertex = found
                #         self.hovered_vertex.border_color = selected_color
                #         self.hovered_vertex.color = selected_color
                #     elif self.hovered_vertex:
                #         self.hovered_vertex.border_color = vertex_boarder_color
                #         self.hovered_vertex.color = vertex_color
                #         self.hovered_vertex = None
            self.screen.fill(background_color)
            if self.selected_vertex:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                self.selected_vertex.x = mouseX
                self.selected_vertex.y = mouseY
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL]:
                    self.pan(int(mouseX - width / 2) * -.2,
                            (int(mouseY - height / 2) * -.2))
            if self.selected_bg:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                # if math.fabs(mouseX) + math.fabs(mouseY) < 500:
                self.pan(int(mouseX - width / 2) * -.2,
                        (int(mouseY - height / 2) * -.2))
            self.calculate_positions()

            for e in self.E:
                # if e.s == self.selected_vertex or\
                #    e.t == self.selected_vertex or\
                #    e.s == self.hovered_vertex or\
                #    e.t == self.hovered_vertex:
                #     e.color = selected_color
                # else:
                #     e.color = edge_color
                e.display(self.screen)
            for v in self.V:
                v.display(self.screen)
            vertex_number_info = self.info_font.render(
                "Vertices: " + str(len(self.V)),
                1,
                debug_color)
            edge_number_info = self.info_font.render(
                "    Edges: " + str(len(self.E)),
                1,
                debug_color)
            fps_number_info = self.info_font.render(
                "      FPS: " + str(self.fpsClock.get_fps())[:5],
                1,
                debug_color)
            self.screen.blit(vertex_number_info, (10, 10))
            self.screen.blit(edge_number_info, (10, 30))
            self.screen.blit(fps_number_info, (10, 50))
            pygame.display.flip()
            self.fpsClock.tick(120)


def launch_graph_plot():
    graph_plot = GraphPlotPanel()
    # graph_plot.buildRandomGraph(number_of_vertices, edge_rate)
    for x in range(number_of_vertices):
        graph_plot.add_node()
    for y in range(number_of_edges):
        graph_plot.add_edge()
    graph_plot.run()


class Edge():
    def __init__(self, s, t, weight):
        self.s = s
        self.t = t
        s.degree += 1
        t.degree += 1
        self.weight = min(random.choice([x for x in range(5, 15)]), s.size, t.size)
        self.color = edge_color

    def __str__(self):
        return "(" + str(self.s) + ", " + str(self.t) + ")"

    def display(self, screen):
        pygame.draw.line(screen, background_color,
                        (self.s.x, self.s.y), (self.t.x, self.t.y),
                         int(self.weight/2)+3)
        pygame.draw.line(screen, self.color,
                        (self.s.x, self.s.y), (self.t.x, self.t.y),
                         int(self.weight/2))


class Vertex():
    def __init__(self, size, name=None):
        self.x = random.choice(range(size, width-size))
        self.y = random.choice(range(size, height-size))
        self.dx = int(random.random() * 100)
        self.dy = int(random.random() * 100)
        self.mass = size
        self.color = vertex_color
        self.border_color = vertex_boarder_color
        self.thickness = 0
        self.degree = 0
        self.size = size * 4
        self.name = name
        if self.name is None:
            self.name = str(random.choice([v for v in range(100)]))

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def display(self, screen):
        pygame.draw.circle(screen, self.border_color, (
            int(self.x), int(self.y)), self.size * view_size_scaler + 3)
        pygame.draw.circle(screen, self.color, (
            int(self.x), int(self.y)), self.size * view_size_scaler, self.thickness)
        fontObj = pygame.font.Font(None, max(self.size, 12))
        label = fontObj.render(self.name, False, word_color)
        screen.blit(label, (self.x-label.get_width()/2,
                            self.y-label.get_height() / 2))

    def move(self):
        self.x -= self.dx
        self.y -= self.dy

if __name__ == "__main__":
    launch_graph_plot()

class TagGraph():
    def __init__(self):
        self.tags = {}
        self.edges = {}
        self.vertices = {}
        self.posts = set()


    def _add_post_tag(self, tag, post):
        if not tag in self.vertices:
            tg = TagInfo()
            tg.post_count = 1
            tg.score = 0
            self.vertices[tag] = tg
        else:
            self.vertices[tag].post_count += 1

    def _remove_post_tag(self, tag, post):
        self.vertices[tag].post_count -= 1
        if self.vertices[tag].post_count == 0:
            del self.vertices[tag]

    def _add_answer_tag(self, tag, answer):
        if not tag in self.vertices:
            return
        self.vertices[tag].answer_count += 1

    def _remove_answer_tag(self, tag, answer):
        if not tag in self.vertices:
            return
        self.vertices[tag].answer_count -= 1

    def add_answer(self, answer, post):
        for tag in post['tags']:
            self._add_answer_tag(tag, answer)

    def remove_answer(self, answer, post):
        for tag in post['tags']:
            self._remove_answer_tag(tag, answer)

    def add_question(self, post):
        if post['id'] in self.posts:
            return
        self.posts.add(post['id'])
        taglist = []
        for tag in post['tags']:
            taglist.append(tag)
            self._add_post_tag(tag, post)
        for i, source in enumerate(taglist):
            for target in taglist[i + 1:]:
                e = (source, target)
                if e[0] > e[1]:
                    e = (target, source)
                w = 1.0 / len(taglist)
                if e in self.edges:
                    self.edges[e] += w
                # Add new vertex
                else:
                    self.edges[e] = w

    def remove_question(self, post):
        if not post['id'] in self.posts:
            return
        self.posts.remove(post['id'])
        taglist = []
        for tag in post['tags']:
            taglist.append(tag)
            self._remove_post_tag(tag, post)
        for i, source in enumerate(taglist):
            for target in taglist[i + 1:]:
                e = (source, target)
                if e[0] > e[1]:
                    e = (target, source)
                w = 1.0 / len(taglist)
                # Remove vertex
                if self.edges[e] == w:
                    del self.edges[e]
                else:
                    self.edges[e] -= w

    def add_vote(self, vote, post):
        vote_type = vote['vote_type_id']
        # Up Mod
        if vote_type == 2:
            for tag in post['tags']:
                self.vertices[tag].score += 1
        elif vote_type == 3:
            for tag in post['tags']:
                self.vertices[tag].score -= 1
        elif vote_type == 5:
            for tag in post['tags']:
                self.vertices[tag].favorite_count += 1

    def remove_vote(self, vote, post):
        vote_type = vote['vote_type_id']
        # Up Mod
        if vote_type == 2:
            for tag in post['tags']:
                if not tag in self.vertices:
                    continue
                self.vertices[tag].score -= 1
        # Down mod
        elif vote_type == 3:
            for tag in post['tags']:
                if not tag in self.vertices:
                    continue
                self.vertices[tag].score += 1
        # Favorite
        elif vote_type == 5:
            for tag in post['tags']:
                if not tag in self.vertices:
                    continue
                self.vertices[tag].favorite_count -= 1


class TimeFilter():
    def __init__(self, event_array, sorted_event_index):
        self.event_array = event_array
        self.sorted_event_index = sorted_event_index
        self.oldindex = 0
        self.newindex = 0
        self.isReverse = None

    def setTime(self, time):
        #binary search to find the latest index
        #that is lte this time
        self.oldindex = 0
        self.newindex = self._bisect_left(time)
        if self.newindex > self.oldindex:
            self.isReverse = False
        else:
            self.isReverse = True

    def event_seq_gen(self):
        i = self.oldindex
        if not self.isReverse:
            while i < self.newindex:
                yield self.event_array[self.sorted_event_index[i]]
                i += 1
        elif self.isReverse:
            while i > self.newindex:
                yield self.event_array[self.sorted_event_index[i]]
                i -= 1

    def _bisect_left(self, x, lo=0, hi=None):
        max = self.event_array[0]['timestamp']
        i = 1
        while x > max and i < len(self.event_array):
            max = self.event_array[i]['timestamp']
            i += 1
        return i

