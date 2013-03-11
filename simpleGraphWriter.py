import cairo
from igraph import Graph, UniqueIdGenerator
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

g = Graph()

# XMLpath = "./miniposts.xml"
XMLpath = "/Users/bryanmaass/Dropbox/!Winter13/163/"\
          "final/so-export-2009-08/100posts.xml"
XMLdoc = minidom.parse(XMLpath)
rowlist = XMLdoc.getElementsByTagName('row')
print len(rowlist), "rows parsed"

gen = UniqueIdGenerator()  # check doc on this guy
# smart add edge, lazy instantiates both vertexes....
# cant add an edge if one of the verices are not made
adjList = {}


def smart_add_edge(sourceName, targetName):
    if sourceName not in gen:
        sourceVertex = {}
        sourceVertex["uid"] = gen[sourceName]
        sourceVertex["name"] = sourceName
        g.add_vertex(sourceVertex)
        if targetName not in gen:
            targetVertex = {}
            targetVertex["uid"] = gen[targetName]
            targetVertex["name"] = targetName
            g.add_vertex(targetVertex)
            g.add_edge(gen[sourceName], gen[targetName])

adjList = {}
for row in rowlist:
    tags = row.getAttribute("Tags")
    taglist = tags.encode('utf-8').strip("><").split("><")
    print taglist
    del tags
    for i, source in enumerate(taglist):
        for target in taglist[i + 1:]:
            print source, target
            smart_add_edge(source, target)
            s = set(target).add(source)
            w = 1/len(taglist)
            if s in adjList:
                adjList[s] += w
            else:
                adjList[s] = w
            print

print adjList            
layout = g.layout('kk')
width, height = 9000, 6000
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)
ctx.scale(width, height)
ctx.rectangle(0, 0, 1, 1)
ctx.set_source_rgba(0, 0, 0, 0)
ctx.fill()
plot = Graph.plot(g, surface, bbox=(width, height), layout=layout)
plot.background = None
plot.redraw()
surface.write_to_png('example.png')

# for i,v in enumerate(g.vs):
# print i,": ",v['name']
# print g
