from graph import Graph
from node import Node

# Todo: The constructor should be passed an int, s, in which a grid (graph) of 's by s' nodes is created automatically
class Grid(Graph):
    def __init__(self, rows, elements):
        self.elements = elements
        self.rows = rows
        self.nodes = self.wip_init_nodes()
        super().__init__(self.nodes)

    def wip_init_nodes(self):
        dictionary = {}
        matrix = []
        node_name = 1

        # Linearly populate matrix and dictionary with newly created node objects based on self.rows and self.elements
        for row in range(self.rows):
            vector = []
            if row != self.rows-1:  # Last row only has rightward links
                for element in range(self.elements):
                    if element != self.elements-1:  # Ending node only contains downward links
                        vector.append(Node(node_name, [node_name+1, node_name+self.elements], [1, 1]))
                    else:
                        vector.append(Node(node_name, [node_name+self.elements], [1]))
                    node_name += 1
                matrix.append(vector)
            else:  # Rightward links for last row
                for element in range(self.elements):
                    vector.append(Node(node_name, [node_name+1], [1]))
                    node_name += 1
                matrix.append(vector)
                matrix[self.rows-1][self.elements-1] = Node(self.rows * self.elements, [], [])

        for vector in matrix:
            for node in vector:
                dictionary.update({node.name: node})

        for node in dictionary.values():
            self.node_bidirectional_linker(node, dictionary)

        return list(dictionary.values())

        # ----[DEBUG]----
        # for array in matrix:
        #     print(array)
        # for vector in matrix:
        #     for node in vector:
        #         print(node.name, node.get_neighbours_dict())
        # print(dictionary.get('25').get_neighbours_dict())
        # print(dictionary.get('19').get_neighbours_dict())
        # print(dictionary.get('28').get_neighbours_dict())

    def node_bidirectional_linker(self, created_node, dictionary):
        """ Given a node with neighbours those referenced
            neighbouring nodes will be linked to the given node
        """
        for node_name in list(created_node.get_neighbours_dict().keys()):
            if node_name not in dictionary.get(node_name).get_neighbours_dict():
                unlinked_node = dictionary.get(node_name)
                unlinked_node.node_names.append(created_node.name.upper())
                unlinked_node.node_weights.append(1)
