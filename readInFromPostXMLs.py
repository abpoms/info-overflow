import os
from xml.dom import minidom
###########
# for dir in os.walk('./'):
# 	if dir[0] != "./":
		XMLpath = dir[0]+"/miniposts.xml"
		# print XMLpath
		XMLdoc = minidom.parse(XMLpath)
		# print XMLdoc
		rowlist = XMLdoc.getElementsByTagName('row')
		print len(rowlist)
		for row in rowlist:
			tags = row.getAttribute("Tags")
			if tags != "":

				# print type(tags)
				print
				taglist = tags.strip("><").split("><")
				for t in taglist:
					print t
				