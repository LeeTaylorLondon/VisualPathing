import node
max_value = 2147483647

class Graph:
    def __init__(self, nodes):
        # Ensures a list is passed to the constructor
        if type(nodes) is not list:
            raise TypeError("Nodes must be contained in a list")
        else:
            self.nodes = nodes
        # Ensures every element of the graph is of class 'node'
        for passed_node in self.nodes:
            if not isinstance(passed_node, node.Node):
                raise TypeError("Element '{}' at index '{}' is not of class node".
                                format(passed_node, self.nodes.index(passed_node)))
        # Init dictionary -> {<node.name>:<node>}
        self.dictionary = self.init_dictionary()

    def init_dictionary(self):
        #  Creates dictionary of IDs and 'node' objects
        dictionary = {}
        for n in self.nodes:
            dictionary.update({n.name: n})
        return dictionary

    def djikstra(self, start, end):
        # Init. vertices dictionary, current node, and unvisited dictionary
        vertices = self.dictionary.copy()  # Vertex dictionary -> {<node.name>:<node-obj>}
        current_node = start  # Current node is set to the starting node
        for n in self.nodes:  # Each <node-obj> in vertices is replaced with init. cost value (int)
            vertices.update({n.name.lower(): max_value})  # Populates vertex dict. with infinite costs
        vertices.update({start.name.lower(): 0})  # Starting node cost is set to 0
        unvisited = vertices.copy()  # Unvisited dictionary -> {<node.name>:<cost>} = vertices
        visited = []
        iterations = []
        current_cost = 0

        # While condition runs until end is found or all nodes have been explored hence no max_value(s)
        while current_node is not end and (max_value in vertices.values()):
            iterations.append(vertices)
            dict_prox_nodes = current_node.get_neighbours_dict()  # Dictionary of linked nodes to current node
            for key in dict_prox_nodes.keys():                    # Updates paths to nodes with shortest paths

                # If newly evaluated cost is less than the current cost,
                # update -> vertices, unvisited, and node.previous_node
                if dict_prox_nodes.get(key) + current_cost < vertices.get(key.lower()):
                    vertices.update({key.lower(): dict_prox_nodes.get(key) + current_cost})
                    unvisited.update({key.lower(): dict_prox_nodes.get(key) + current_cost})
                    self.dictionary.get(key.lower()).previous_node = current_node

            # Current node is marked as visited, removed from unvisited, and added to visited
            current_node.visited = True
            unvisited.pop(current_node.name.lower())
            visited.append(current_node)

            # (Reverse Dictionary Search) Index of the unvisited minimum cost corresponds to the name of the next node
            current_node = self.dictionary.get(list(unvisited.keys())[list(unvisited.
                                               values()).index(min(unvisited.values()))])
            current_cost = vertices.get(current_node.name)  # Current path cost is set to the cost of the current node

        visited.append(current_node)
        # print('Iterations', iterations)  # Debug
        return vertices.get(end.name.lower()), end.backtrack(), visited, iterations

    def a_star(self, start, end):
        pass

    def __repr__(self):
        return self.nodes
