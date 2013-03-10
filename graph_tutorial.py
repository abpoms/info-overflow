from igraph import Graph
# help("modules")



#full graph:
# g = Graph.Full(3)

#GenerateRandomGraph:
g = Graph.GRG(50,.3)


# surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, 300, 300)
# ctx = cairo.Context(surface)




#writes a svg file:
g.write_svg("helloGraph.svg","auto",300,300)


# write_svg(self, fname, layout='auto', width=None, height=None,
# labels = 'label', colors = 'color', shapes = 'shape', vertex_size = 10,
# edge_colors = 'color', font_size = 16, *args, **kwds)
