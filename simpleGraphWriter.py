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


# XMLpath = "./miniposts.xml"
XMLpath = "/Users/bryanmaass/Dropbox/!Winter13/163/final/so-export-2009-08/100posts.xml"
XMLdoc = minidom.parse(XMLpath)
rowlist = XMLdoc.getElementsByTagName('row')
print len(rowlist), "rows parsed"

gen = UniqueIdGenerator()
def smart_add_edge(sourceName,targetName):
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
	g.add_edge(gen[sourceName],gen[targetName])

for row in rowlist:
	tags = row.getAttribute("Tags")
	taglist = tags.encode('utf-8').strip("><").split("><")
	print taglist
	del tags
	for i,source in enumerate(taglist):
		for target in taglist[i+1:]:
			smart_add_edge(source,target)
			# print source,target


#crudely resize svg canvas by # of nodes:
sideLength = len(g.vs)*10


############################
# write_svg(self, fname, layout='auto', width=None, height=None,
# labels = 'label', colors = 'color', shapes = 'shape', vertex_size = 10,
# edge_colors = 'color', font_size = 16, *args, **kwds)
g.write_svg("helloGraph.svg","auto",sideLength,sideLength,"label","color","rect",10)

# for i,v in enumerate(g.vs):
# 	print i,": ",v['name']
print g









