import os
from xml.dom import minidom

#combines graph_tutorial and readInFromPostXMLs to output a svg graph

#TODO: make it work with cairo



########################
#note:  hardcoded to this particular xml
#		sample file. will want to loop over
#		all xml files in a folder.
XMLpath = "./miniposts.xml"
XMLdoc = minidom.parse(XMLpath)
rowlist = XMLdoc.getElementsByTagName('row')
print len(rowlist), "rows parsed"
for row in rowlist:
	tags = row.getAttribute("Tags")
	if tags != "":#there are many empty tags
		taglist = tags.strip("><").split("><")
		