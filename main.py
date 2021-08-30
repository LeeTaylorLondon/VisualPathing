from node import Node
from graph import Graph
from scene import Scene
from wip_grid import Grid

""" Node initialisation 
# <node_name> = node(<node_name>, <link_node_names>, <link_node_weights>) """
a = Node("A", ["B"], [5])
b = Node("B", ["A", "F", "C"], [5, 8, 6])
c = Node("C", ["B", "D"], [6, 7])
d = Node("D", ["C", "E", "M"], [7, 13, 12])
e = Node("E", ["D"], [13])
f = Node("F", ["B", "I", "H", "G"], [8, 10, 3, 2])
g = Node("G", ["F"], [2])
h = Node("H", ["F", "J", "K"], [3, 8, 1])
i = Node("I", ["F", "J"], [10, 9])
j = Node("J", ["H", "I"], [8, 9])
k = Node("K", ["H", "L"], [1, 4])
l = Node("L", ["K", "M"], [4, 7])
m = Node("M", ["D", "L"], [12, 7])

a2 = Node("A", ["B", "C"], [4, 3])
b2 = Node("B", ["D", "A"], [9, 4])
c2 = Node("C", ["A", "D"], [3, 8])
d2 = Node("D", ["B", "C"], [9, 8])


""" Graph initialisation ([<node>, <node>, <node>, ...]) """
small_graph = Graph([a2, b2, c2, d2])
new_graph = Graph([a, b, c, d, e, f, g, h, i, j, k, l, m])

""" Testing djikstra method """
#print('Main', new_graph.djikstra(b, h))
#print(new_graph.djikstra(k, d))
#print(new_graph.djikstra(b, h))

""" WIP Grid """
#wip_grid = Grid(5, 5)
#wip_grid_2 = Grid(3, 3)
#wip_grid_bugged = Grid(4, 4)
grid_test = Grid(6, 6)
#wip_grid_big = Grid(8, 8)

#Scene(wip_grid_2)
#Scene(wip_grid_bugged)
#Scene(wip_grid_big)
Scene(grid_test)

""" Scene objects """
#Scene(small_graph)
#Scene(new_graph)
