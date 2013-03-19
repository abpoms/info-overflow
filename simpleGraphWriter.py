import cairo
from igraph import Graph, UniqueIdGenerator
import igraph
from xml.dom import minidom

# combines graph_tutorial and readInFromPostXMLs to output a svg graph

########################
# note:  hardcoded to this particular xml
#               sample file. will want to loop over
#               all xml files in a folder.

# TODO: discuss language-tags vs areas_of_interest-tags

# TODO: (at asdf): we dont gain relationship data from 1 tag
# are we using it to map users to tags
# this implimentation asusmes that we dont care about the users...

drawPNG = True

print "entering XML"
# XMLpath = "./miniposts .xml"
XMLpath = "./10000posts.xml"
XMLdoc = minidom.parse(XMLpath)
rowlist = XMLdoc.getElementsByTagName('row')
print len(rowlist), "rows parsed"






adjList = {}
for row in rowlist:
    tags = row.getAttribute("Tags")
    taglist = tags.encode('utf-8').strip("><").split("><")
    del tags
    for i, source in enumerate(taglist):
        for target in taglist[i + 1:]:
            e = (source, target)
            if e[0] > e[1]:
                e = (target, source)
             

# cant add an edge if one of the verices are not made
g = Graph()
# print g
g.es["weight"] = 1.0

gen = UniqueIdGenerator()

for e in adjList:
    # print e[0], e[1]
    if e[0] not in gen:
        sourceVertex = {}
        # sourceVertex["uid"] = gen[e[0]]
        sourceVertex = e[0]
        g.add_vertex(sourceVertex)
        # print g
    if e[1] not in gen:
        targetVertex = {}
        # targetVertex["uid"] = gen[e[1]]
        targetVertex = e[1]
        g.add_vertex(targetVertex)
    # print adjList[e]
    g[gen[e[0]], gen[e[1]]] = adjList[e] * 5

print "graph contains ", len(g.es), "edges"
print "graph contains ", len(g.vs), "vertices"


# filterOutNoise(edge)

minDegree = 5
for e in g.es:
    if e["weight"] < 10000.0:
        g.delete_edges(e)
for x in range(8):
    print "removing:"
    for v in g.vs:
        if v.degree() < minDegree:
            g.delete_vertices(v)
    print "graph contains ", len(g.es), "edges"
    print "graph contains ", len(g.vs), "vertices"

drawPNG = True
if drawPNG:
    print "drawing begins:"
    layout = g.layout('kk')
    width, height = 5000, 5000
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.scale(width, height)
    ctx.rectangle(0, 0, 1, 1)
    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.fill()

    plot = igraph.plot(g, surface,
                       vertex_shape="rect", vertex_label=g.vs["name"],
                       edge_width=g.es["weight"],
                       bbox=(width, height), layout=layout)
    # plot = igraph.plot(g, surface, bbox=(width, height), layout=layout)
    plot.background = None
    plot.redraw()
    surface.write_to_png('example.png')

    # for i,v in enumerate(g.vs):
    # print i,": ",v['name']
    # print g
