class Node:
    def __init__(self, name, node_names, node_weights):
        self.name = str(name).lower()            # String
        self.node_names = node_names             # Array
        self.node_weights = node_weights         # Array
        self.visited = False                     # Boolean
        self.previous_node = None                # node

        # Ensures equal no. of nodes & weights
        if len(self.node_names) != len(self.node_weights):
            raise TypeError("shape error node '{}' {} node name(s) != {} weight(s)"
                            .format(self.name, len(self.node_names), len(self.node_weights)))

        # Ensures neighbouring node 'names' are a list
        if type(self.node_names) is not list:
            raise TypeError("Linking node names must be a 1-dimensional list")

        # Ensures neighbouring node 'weights' are a list
        if type(self.node_weights) is not list:
            raise TypeError("Linking node weights must be a 1-dimensional list")

        for i in range(len(self.node_names)):
            self.node_names[i] = str(self.node_names[i])

    def __repr__(self):
        """ Overrides string method displaying node name and link data """
        return 'node.{}'.format(self.name.lower())

    def __str__(self):
        return '{}'.format(self.name.lower())

    def get_neighbours_dict(self):
        """ Returns a dictionary of node names and weights {<node_name>:<node_weight>} """
        rv = {}
        for index in range(len(self.node_names)):
            rv.update({self.node_names[index]: self.node_weights[index]})
        return rv

    def backtrack(self):
        rv = []
        previous_node = self.previous_node
        while previous_node is not None:
            rv.append(previous_node)
            previous_node = previous_node.previous_node
        rv.reverse()
        rv.append(self)
        return rv
