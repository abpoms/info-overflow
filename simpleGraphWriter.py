import os
from igraph import *
from xml.dom import minidom

#combines graph_tutorial and readInFromPostXMLs to output a svg graph


########################
#note:  hardcoded to this particular xml
#		sample file. will want to loop over
#		all xml files in a folder.


#TODO: convert from unicode to ascii
	#		 2bytes---^  1byte--^

#TODO: discuss language-tags vs areas_of_interest-tags

#TODO: make it work with cairo?

#TODO: (at asdf): we dont gain relationship data from 1 tag
	#are we using it to map users to tags
	#this implimentation asusmes that we dont care about the users...


g = Graph()

ar = []


XMLpath = "./miniposts.xml"
XMLdoc = minidom.parse(XMLpath)
rowlist = XMLdoc.getElementsByTagName('row')
print len(rowlist), "rows parsed"
for row in rowlist:
	tags = row.getAttribute("Tags")
	taglist = tags.strip("><").split("><")
	for i,source in enumerate(taglist):
		for dest in taglist[i+1:]:
			g.add_vertices([source,dest])
			g.add_edge(source,dest)
			# print source,dest
sideLength = len(g.vs)*20

g.write_svg("helloGraph.svg","auto",sideLength,sideLength,"label","color","rect",10)

# write_svg(self, fname, layout='auto', width=None, height=None,
# labels = 'label', colors = 'color', shapes = 'shape', vertex_size = 10,
# edge_colors = 'color', font_size = 16, *args, **kwds)

# print g









