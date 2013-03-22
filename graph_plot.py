from pprint import pprint
import pygame
from pygame.locals import *
import random
import math
import tables as tb
import cPickle



background_colour = (50, 50, 50)
(width, height) = (1920/2, 1080/2)
dampen = 0.01

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


class TagInfo():
    def __init__(self):
        self.post_count = 0
        self.score = 0
        self.answer_count = 0
        self.favorite_count = 0
        
mouse_sens = 3
fpsClock = pygame.time.Clock()

# h5file = tb.openFile('overflow.h5', 'r')

#input: time
#output: 

# events = []
# event_table = h5file.getNode("/", "events")


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



USER_TYPE = 0
VOTE_TYPE = 1
POST_TYPE = 2

# Vert(name, total_rep, ...)
# Edge(w,(v1,v2))


class GraphPlotPanel():
    def __init__(self):
        self.selected_bg = False
        self.selected_vertex = None
        self.running = True
        self.frame_count = 0
        self.dampen = 0.2
        self.prune = 0.95
        self.E = []
        self.V = []
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('')


def findvertex(x, y):
    for v in self.V:
        if math.hypot(v.x - x, v.y - y) <= v.size:
            return v
    return None


def spring(edge):
    _spring(edge.s, edge.t, edge.weight, edge=True)

    
def _spring(v1, v2, weight, edge):
    pad = 3*(v1.size + v2.size)
    x_diff = v1.x - v2.x
    y_diff = v1.y - v2.y

    angle = math.atan2(y_diff, x_diff)

    dist = math.hypot(x_diff, y_diff)

    force = 30 * (dist - pad)

    if force > force_max:
        force = force_max
    if edge:
        force = 200 + 50 * number_of_vertices
        
    x_force = math.cos(angle) * force
    y_force = math.sin(angle) * force

    v1.dx += x_force
    v2.dx -= x_force

    v1.dy += y_force
    v2.dy -= y_force


def repel(self, v1):
    for v2 in V:
        if v2 == v1:
            return
        _spring(v1,v2,300,pull=False)



    def pan(self, x ,y):
        for v in V:
            v.x+=x * mouse_sens
            v.y+=y * mouse_sens


    def run(self):
        while(self.running):   
            self.frame_count += 1   
            self.dampen = self.dampen * .97
            # V.append(Vertex((width/2,height/2), 5,"w0t"))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    found = findvertex(self.V, mouseX, mouseY)
                    if found:
                        self.selected_vertex = found
                    else:
                        self.selected_bg = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.selected_vertex = None
                    self.selected_bg = False
            self.screen.fill(background_color)
            if self.selected_vertex:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                self.selected_vertex.x = mouseX
                self.selected_vertex.y = mouseY
            if self.selected_bg:
                (mouseX, mouseY) = pygame.mouse.get_rel()
                if math.fabs(mouseX) + math.fabs(mouseY) < 100:
                    print mouseX, mouseY
                    pan(mouseX, mouseY, self.V)
            for e in self.E:
                spring(e)
            for v in self.V:
                # pygame.draw.line(screen, (0, 0, 0),
                #      (v.x, v.y), (v.x+v.dx*10, v.y+v.dy*10), 2)
                # print self.dampen
                # if self.dampen > 1e-05:
                repel(v, self.V)
                if math.fabs(v.dx) > 1000:
                    v.dx *= .7
                if math.fabs(v.dy) > 1000:
                    v.dy *= .7
                v.dx = v.dx * dampen
                v.dy = v.dy * dampen
                v.move()

            for e in self.E:
                e.display(self.screen)
            for v in self.V:
                v.display(self.screen)
            pygame.display.flip()
            fpsClock.tick(60)

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
        vote_func(vote, post)

    def _post(self, e_id, post_func, answer_func):
        if not e_id in self.post_dict:
            return None
        post = self.post_dict[e_id]
        if post['post_type_id'] == 1:
            post_func(post)
            return post
        else:
            if not post['parent_id'] in self.post_dict:
                return None
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
        count = 0
        for event in new_events:
            count += 1
            print "count:", count
            t = event['event_type']
            e_id = event['event_id']
            if t == USER_TYPE:
                user = self.user_dict[e_id]
            elif t == VOTE_TYPE:
                self._vote(e_id, vote_func, post_func, answer_func)
            elif t == POST_TYPE:
                self._post(e_id, post_func, answer_func)
        self.dampen = dampen
        self._create_visible()

    def _create_visible(self):
        v_dict = {}
        max_size = 0
        item_list = self.tag_group.vertices.items()
        pruned_list = []
        for tag, taginfo in item_list:
            if tag == '':
                continue
            if taginfo.post_count > max_size:
                max_size = taginfo.post_count
        print "max:", max_size
        for tag, taginfo in item_list:
            print "size:", taginfo.post_count
            if (0.2 * max_size) > taginfo.post_count or tag == '':
                continue
            pruned_list.append((tag, taginfo))
            if len(pruned_list) > number_of_vertices:
                break
        for tag, taginfo in pruned_list:
            if taginfo.post_count > max_size:
                max_size = taginfo.post_count
        for tag, taginfo in pruned_list:
            size = int(taginfo.post_count*1.0/max_size * 256)
            size /= 4
            print size
            v_dict[tag] = Vertex((random.randint(size, width-size),
                                  random.randint(size, height-size)),
                                 size,
                                 tag)
        e_dict = {}
        max_weight = 0
        e_pruned = []
        for e, weight in self.tag_group.edges.items():
            if not e[0] in v_dict or not e[1]in v_dict:
                continue
            if weight > max_weight:
                max_weight = weight
            e_pruned.append((e, weight))
        for e, weight in e_pruned:
            print "weight", weight
            weight = (weight*1.0/max_weight)*100
            print "new weight", weight
            s = v_dict[e[0]]
            t = v_dict[e[1]]
            e_dict[(s, t)] = Edge(s, t, weight)
        self.V = v_dict.values()
        self.E = e_dict.values()
        print "done calculating"
        print len(self.V)
        print len(self.E)


def launch_graph_plot():
    graph_plot = GraphPlotPanel()
    for n in range(16):
        size = random.choice([k for k in range(20, 50, 5)])
        x = random.choice([k for k in range(size, width + size, 5)])
        y = random.choice([k for k in range(size, height + size, 5)])
        v = Vertex((x, y), size)
        graph_plot.V.append(v)
    for i in range(10):
        weight = random.choice([k for k in range(20, 50, 5)])
        v1spot = random.choice([k for k in range(0, len(graph_plot.V))])
        v2spot = random.choice([k for k in range(0, len(graph_plot.V))])
        e = Edge(graph_plot.V[v1spot], graph_plot.V[v2spot], weight)
        graph_plot.E.append(e)

    graph_plot.run()


def _launch_daemon(daemon, q):
    graph_endpoint = GraphPlotEndpoint(q)
    graph_plot_uri = daemon.register(graph_endpoint)
    ns = Pyro4.locateNS()
    ns.register("info-overflow.graph_plot", graph_plot_uri)
    daemon.requestLoop()


class GraphPlotEndpoint():
    def __init__(self, q):
        self.q = q
        pass

    def set_time(self, time):
        print 'received time'
        self.q.put(('time', time))
        print 'returning'
        return None

# class Edge():
#     def __init__(self, (s, t), weight):
#         self.s = s
#         self.t = t
#         self.weight = weight
#         self.color = (0, 0, 255)
class Edge():
    def __init__(self, s, t, weight):
        self.s = s
        self.t = t
        self.weight = weight
        c = weight + 50
        self.color = (c, c, c)

    def __str__(self):
        return "("+ str(self.s) +", "+ str(self.t) +")"

    def display(self, screen):
        pygame.draw.line(screen, self.color,
                        (self.s.x, self.s.y), (self.t.x, self.t.y),
                        int(self.weight))


class Vertex():
    def __init__(self, (x, y), size, name=None):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.size = size
        self.mass = size
        self.color = lightRed_color
        self.border = (10, 10, 10)
        self.thickness = 0
        self.name = name
        if self.name is None:
            self.name = str(random.choice([v for v in range(100)]))

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def display(self, screen):
        pygame.draw.circle(screen, self.color, (
            int(self.x), int(self.y)), self.size, self.thickness)
        pygame.draw.circle(screen, self.border, (
            int(self.x), int(self.y)), self.size, 1)
        fontObj = pygame.font.Font(None, max(self.size,12))
        label = fontObj.render(self.name, False, white_color)
        screen.blit(label, (self.x-label.get_width()/2, self.y-label.get_height()/2))

    def move(self):
        self.x -= self.dx
        self.y -= self.dy




if __name__ == "__main__":
    launch_graph_plot()
