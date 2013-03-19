import pygame
import random
import math
import os.path
import tables as tb
import cPickle
import Pyro4


background_colour = (255, 255, 255)
(width, height) = (400, 400)
dampen = .01
elasticity = 0.75
fpsClock = pygame.time.Clock()
spread = 3
vertex_padding = 0
frame_count = 0


class TagInfo():
    def __init__(self):
        self.post_count = 0
        self.score = 0
        self.answer_count = 0
        self.favorite_count = 0


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
                self.vertices[tag].score -= 1
        # Down mod
        elif vote_type == 3:
            for tag in post['tags']:
                self.vertices[tag].score += 1
        # Favorite
        elif vote_type == 5:
            for tag in post['tags']:
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
        self.oldindex = self.newindex
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
        if hi is None:
            hi = len(self.sorted_event_index)
        while lo < hi:
            mid = (lo+hi)/2
            midval = self.event_array[
                self.sorted_event_index[mid]]['timestamp']
            if midval+1 <= x:
                lo = mid+1
            elif midval-1 > x:
                hi = mid
            else:
                return mid
        return -1


def createSortedIndexFile(events):
    print "loading... (should take about a minute)"
    if not os.path.isfile("index_sorted.p"):
        print "recreating Pickle"
        sorted_event_index = events[0:].argsort(order=('timestamp'))
        cPickle.dump(sorted_event_index, open("index_sorted.p", "wb"))
    else:
        sorted_event_index = cPickle.load(open('index_sorted.p', 'rb'))
    return sorted_event_index


USER_TYPE = 0
VOTE_TYPE = 1
POST_TYPE = 2


class GraphPlotPanel():
    def __init__(self):
        self.h5file = tb.openFile('overflow.h5', 'r')
        self.event_table = self.h5file.getNode("/", "events")
        self.user_table = self.h5file.getNode("/", "users")
        self.post_table = self.h5file.getNode("/", "posts")
        self.vote_table = self.h5file.getNode("/", "votes")
        self.user_dict = self._load_table(self.user_table)
        self.post_dict = self._load_table(self.post_table)
        self.vote_dict = self._load_table(self.vote_table)
        self.event_array = self._load_array(self.event_table)
        self.sorted_event_index = createSortedIndexFile(self.event_table)
        self.timefilter = TimeFilter(self.event_array, self.sorted_event_index)
        self.tag_group = TagGraph()

    def run(self):
        self.set_time(self.event_table[100]['timestamp'])

    def _load_table(self, table):
        d = {}
        for row in table.iterrows():
            fields = row.fetch_all_fields()
            d[fields['id']] = fields
        return d

    def _load_array(self, table):
        d = []
        for row in table.iterrows():
            d.append(row.fetch_all_fields())
        return d

    def _vote(self, e_id, vote_func, post_func, answer_func):
        if not e_id in self.vote_dict:
            return
        vote = self.vote_dict[e_id]
        post = self._post(vote['post_id'], post_func, answer_func)
        if post is None:
            return
        print post
        vote_func(vote, post)

    def _post(self, e_id, post_func, answer_func):
        if not e_id in self.post_dict:
            return None
        post = self.post_dict[e_id]
        if post['post_type_id'] == 1:
            post_func(post)
            return post
        else:
            question = self.post_dict[post['parent_id']]
            answer_func(post, question)
            post_func(question)
            return question

    def set_time(self, time):
        self.timefilter.setTime(time)
        new_events = self.timefilter.event_seq_gen()
        if self.timefilter.isReverse:
            post_func = self.tag_group.remove_question
            answer_func = self.tag_group.remove_answer
            vote_func = self.tag_group.remove_vote
        else:
            post_func = self.tag_group.add_question
            answer_func = self.tag_group.add_answer
            vote_func = self.tag_group.add_vote
        for event in new_events:
            t = event['event_type']
            e_id = event['event_id']
            if t == USER_TYPE:
                user = self.user_dict[e_id]
            elif t == VOTE_TYPE:
                self._vote(e_id, vote_func, post_func, answer_func)
            elif t == POST_TYPE:
                self._post(e_id, post_func, answer_func)


def launch_graph_plot():
    graph_plot = GraphPlotPanel()
    daemon = Pyro4.Daemon()
    graph_plot_uri = daemon.register(graph_plot)
    ns = Pyro4.locateNS()
    ns.register("info-overflow.graph_plot", graph_plot_uri)
    graph_plot.run()
    while True:
       # graph_plot.run()
        pass
    
    pass


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
