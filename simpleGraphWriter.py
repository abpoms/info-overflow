import cairo
from igraph import Graph, UniqueIdGenerator
from xml.dom import minidom

#combines graph_tutorial and readInFromPostXMLs to output a svg graph

########################
#note:  hardcoded to this particular xml
#               sample file. will want to loop over
#               all xml files in a folder.


#TODO: discuss language-tags vs areas_of_interest-tags

#TODO: make it work with cairo?

#TODO: (at asdf): we dont gain relationship data from 1 tag
#are we using it to map users to tags
#this implimentation asusmes that we dont care about the users...

g = Graph()


# XMLpath = "./miniposts.xml"
XMLpath = "/Users/bryanmaass/Dropbox/!Winter13/163/final/so-export-2009-08 \
           /100000posts.xml"
XMLdoc = minidom.parse(XMLpath)
rowlist = XMLdoc.getElementsByTagName('row')
print len(rowlist), "rows parsed"

gen = UniqueIdGenerator()  # check doc on this guy
#smart add edge, lazy instantiates both vertexes....
#cant add an edge if one of the verices are not made


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

for row in rowlist:
    tags = row.getAttribute("Tags")
    taglist = tags.encode('utf-8').strip("><").split("><")
    # print taglist
    del tags
    for i, source in enumerate(taglist):
        for target in taglist[i+1:]:
            smart_add_edge(source, target)
            # print source,target


#crudely resize svg canvas by # of nodes:
# sideLength = len(g.vs)*10


############################
# write_svg(self, fname, layout='auto', width=None, height=None,
# labels = 'label', colors = 'color', shapes = 'shape', vertex_size = 10,
# edge_colors = 'color', font_size = 16, *args, **kwds)
# g.write_svg("helloGraph.svg", "auto", sideLength, sideLength, "label",
#            "color", "rect", 10)

<<<<<<< HEAD
# layout = g.layout('kk')
# width,height = 900,600
# surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
# ctx = cairo.Context(surface)
# ctx.scale(width,height)
# ctx.rectangle(0, 0, 1, 1)
# ctx.set_source_rgba(0,0,0,0)
# ctx.fill()
# plot = plot(g, surface, bbox=(width, height), layout=layout)
# plot.background = None
# plot.redraw()
# surface.write_to_png('example.png')
=======
 
layout = g.layout('sphere')
width,height = 9000,6000
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)
ctx.scale(width,height)
ctx.rectangle(0, 0, 1, 1)
ctx.set_source_rgba(0,0,0,0)
ctx.fill()
plot = plot(g, surface, bbox=(width, height), layout=layout)
plot.background = None
plot.redraw()
surface.write_to_png('examplesphere.png')
>>>>>>> drawing png availiabile

# for i,v in enumerate(g.vs):
    # print i,": ",v['name']
# print g
