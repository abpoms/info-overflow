from igraph import Graph

#full graph:
# g = Graph.Full(3)

#GenerateRandomGraph:
g = Graph.GRG(50,.3)


#writes a svg file:
<<<<<<< HEAD
g.write_svg("helloGraph.svg", "auto", 500, 500)
=======
g.write_svg("helloGraph.svg","auto",300,300)
>>>>>>> uncommented out some stuff

# write_svg(self, fname, layout='auto', width=None, height=None,
# labels = 'label', colors = 'color', shapes = 'shape', vertex_size = 10,
# edge_colors = 'color', font_size = 16, *args, **kwds)
