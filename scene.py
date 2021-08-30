from math import sqrt

import pygame
import colors
import random
import time
from button import Button
from visualnode import VisualNode
from visualnode import message_display
from visualvertex import VisualVertex

class Scene:
    def __init__(self, graph):
        pygame.init()
        pygame.display.set_caption('Searching.exe')

        self.display_width = 1075
        self.display_height = 600
        self.window_display = pygame.display.set_mode((self.display_width, self.display_height))
        self.clock = pygame.time.Clock()
        self.refresh_rate = 144
        self.tick = 0.1

        self.node_width = 40
        self.graph = graph
        self.nodes = self.init_nodes()
        self.vertices = self.init_vertices()

        self.start = None
        self.end = None
        self.algorithm = 'djikstra'
        self.djikstra = False

        # WIP
        self.buttons = self.init_buttons()

        self.window_loop(fps_debug=True)

    def init_buttons(self):
        rv = []
        rv.append(Button(self.window_display, colors.green, 800, 100, 150, 40, 'Run', colors.white, 40,
                                   self.run_animation))
        rv.append(Button(self.window_display, colors.blue, 800, 160, 150, 40, 'Load Preset', colors.white, 25,
                         self.load_graph_preset))
        rv.append(Button(self.window_display, colors.darker_red, 800, 220, 150, 40, 'Randomise', colors.white, 25,
                         self.randomise_graph))
        return rv

    def init_vertices(self):
        rv = {}
        for current_visual_node in list(self.nodes.values()):
            for node_name in current_visual_node.get_neighbours_dict().keys():
                connecting_node = self.nodes.get(node_name.lower())
                connecting_cost = current_visual_node.get_neighbours_dict().get(node_name)
                vertex = VisualVertex(current_visual_node, connecting_node, connecting_cost)
                if vertex.to_string() not in rv.keys() and vertex.to_string_reverse() not in rv.keys():
                    rv.update({vertex.to_string(): vertex})
        return rv

    def init_nodes(self):
        rv = {}
        for node in self.graph.nodes:
            rv.update({node.name: VisualNode(node, random.randint(self.node_width, self.display_width - self.node_width),
                                 random.randint(self.node_width, self.display_height - self.node_width), self.node_width)})
        return rv

    # Todo: display costs that are the sum of the route to that node (self.graph.vertices @ each iteration)
    # Todo: update self.graph.djikstra(...) to return each iteration of vertices
    def djikstra_animated(self, start, end):
        if type(start) is str and type(end) is str:
            start = self.graph.dictionary.get(start)
            end = self.graph.dictionary.get(end)
        else:
            raise TypeError('invalid object type passed to method djikstra_animated')
        shortest_cost, shortest_path, visited_path, iterations = self.graph.djikstra(start, end)

        def load_path(path):
            visual_nodes = []
            nodes = []
            for node in path:
                visual_nodes.append(self.nodes.get(node.name))
                nodes.append(self.graph.dictionary.get(node.name))
            return visual_nodes, nodes

        def load_vertices(path):
            nodes = load_path(path)[1]
            node_links = []
            vertex_names = []
            vertices = []
            for node in nodes:
                node_links.append(node.backtrack()[-2:])
            for vertex in node_links:
                if len(vertex) is 2:
                    # Todo: Update to account for names with len > 1 (name + ' ' + other_name)
                    vertex_names.append(vertex[0].name + ' ' + vertex[1].name)
            for vertex_name in vertex_names:
                if vertex_name in self.vertices:
                    vertices.append(self.vertices.get(vertex_name))
                else:
                    vertices.append(self.vertices.get(vertex_name[::-1]))
            return vertices

        def reset_colors():
            # Set node (default) colors
            for nodeV in visited_path:
                nodeV.color = node_default_color
                nodeV.text_color = text_default_color

            # Set vertex (default) colors
            for vertex in visited_vertices:
                vertex.vertex_color = vertex_default_color
                vertex.cost_color = vertex_default_text_color

        visited_path = load_path(visited_path)[0]         # type = visualnode(s)
        shortest_path = load_path(shortest_path)[0]       # type = visualnode(s)
        visited_vertices = load_vertices(visited_path)    # type = visualvertex(s)
        shortest_vertices = load_vertices(shortest_path)  # type = visualvertex(s)

        node_default_color = colors.black
        node_visit_color = colors.white
        node_shortest_path_color = colors.cyan_blue
        text_default_color = colors.pycharm_white
        text_visit_color = colors.black
        vertex_visit_color = colors.cyan_blue
        vertex_text_color = colors.white
        vertex_default_color = colors.blue
        vertex_default_text_color = colors.pycharm_white

        ''' Changes node then vertex colors (visited path) '''
        for i in range(len(visited_path)):
            """ Changes the node colors to visited color (node shape, node name) """
            visited_path[i].color = node_visit_color
            visited_path[i].text_color = text_visit_color
            yield

            """ Changes the corresponding vertex colors (vertex line, cost text) """
            try:
                visited_vertices[i].vertex_color = vertex_visit_color
                visited_vertices[i].cost_color = vertex_text_color
                yield
            except IndexError:
                yield
        reset_colors()

        ''' Changes node then vertex colors (shortest path) '''
        for i in range(len(shortest_path)):
            """ Changes the node colors to visited color (node shape, node name) """
            shortest_path[i].color = node_visit_color
            shortest_path[i].text_color = text_visit_color
            yield

            """ Changes the corresponding vertex colors (vertex line, cost text) """
            try:
                shortest_vertices[i].vertex_color = vertex_visit_color
                shortest_vertices[i].cost_color = vertex_text_color
                yield
            except IndexError:
                yield
        reset_colors()

    def randomise_graph(self):
        self.nodes.clear()
        self.nodes = self.init_nodes()
        self.vertices.clear()
        self.vertices = self.init_vertices()

    def graph_grid(self):
        x, y, counter = 50, 50, 0
        nodes = len(self.nodes.values())
        nodes_per_row = int(sqrt(nodes))
        node_names = list(self.nodes.keys())
        for i in range(len(node_names)):
            if counter == nodes_per_row:
                x = 50
                y += 90
                counter = 0
            self.nodes.get(node_names[i]).set_xy(x, y)
            x += 90
            counter += 1

        self.vertices.clear()
        self.vertices = self.init_vertices()

    def load_graph_preset(self):
        if len(self.nodes.values()) is 13:
            """ Predefined pairs of xy coordinates resembling original drawn graph """
            preset_coordinates = [[253.0,51.0], [467.0,9.0], [557.0,185.0], [496.0,317.0], [670.0,258.0], [338.0,142.0],
                                  [227.0,142.0], [183.0,280.0], [413.0,266.0], [264.0,345.0], [29.0,327.0], [206.0,438.0],
                                  [382.0,425.0]]
            for i in range(len(self.nodes.values())):
                list(self.nodes.values())[i].set_xy(preset_coordinates[i][0], preset_coordinates[i][1])
            self.vertices.clear()
            self.vertices = self.init_vertices()

    def render_dragging(self, node):
        """ Updates drawn vertices corresponding only to the neighbours of the affected node
            Without this algorithm scene fps w/ 13 nodes ~ 23.50, now w/ 13 nodes fps ~ 50.00+ """
        for node_name in node.get_neighbours_dict().keys():
            connecting_node = self.nodes.get(node_name.lower())
            connecting_cost = node.get_neighbours_dict().get(node_name)
            vertex = VisualVertex(node, connecting_node, connecting_cost)
            try:
                self.vertices.pop(vertex.to_string())
                self.vertices.pop(vertex.to_string_reverse())
            except KeyError:
                pass
            self.vertices.update({vertex.to_string(): vertex})

    def render_vertices(self, debug):
        try:  # Render VERTICES
            for vertex in self.vertices.values():
                vertex.display_vertex(self.window_display, debug)
        except (TypeError, AttributeError):
            pass

    def render_nodes(self, mouse_pos, mouse_button_clicked, debug):
        try:
            for node in list(self.nodes.values()):
                node.display_node(self.window_display, mouse_pos, mouse_button_clicked, debug)
                if node.dragged:
                    self.render_dragging(node)
                    node.dragged = False
        except AttributeError:
            pass

    def run_animation(self):
        if self.algorithm is 'djikstra':
            self.djikstra = True

    def render_buttons(self, mouse_pos, mouse_button_clicked, debug):
        try:
            for button in self.buttons:
                button.render(mouse_pos, mouse_button_clicked)
                if button.clicked:
                    button.action()
                    button.clicked = False
        except AttributeError:
            pass

    def window_loop(self, fps_debug):
        starting_interval = time.time()
        #color_node = self.djikstra_animated('k', 'd')
        color_node = self.djikstra_animated('1', '36')

        window_exit = False
        while not window_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # DEBUG
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Randomise Node Positions
                        self.randomise_graph()
                    if event.key == pygame.K_d:  # Animate Djikstra's Algorithm
                        self.djikstra = True
                    if event.key == pygame.K_q:  # Print Node Coordinates
                        print('\n')
                        for node in list(self.nodes.values()):
                            print(node)
                        self.djikstra = False
                    if event.key == pygame.K_1:  # Load Preset Node Configuration
                        self.load_graph_preset()
                    if event.key == pygame.K_e:
                        self.graph_grid()
                # DEBUG (End)

            self.window_display.fill(colors.grey)
            mouse_pos = pygame.mouse.get_pos()
            mouse_button_clicked = pygame.mouse.get_pressed()

            # Start of Rendering
            self.render_vertices(debug = False)
            self.render_nodes(mouse_pos, mouse_button_clicked, debug = False)
            self.render_buttons(mouse_pos, mouse_button_clicked, debug = False)

            if self.djikstra:
                if time.time() - starting_interval > self.tick:
                    try:
                        starting_interval = time.time()
                        next(color_node)
                    except StopIteration:
                        color_node = self.djikstra_animated('k', 'd')
                        self.djikstra = False
            # End of Rendering

            if fps_debug:
                message_display('FPS: ' + str(self.clock)[11:13], 10, 10, colors.green, 15, self.window_display)
            pygame.display.update()
            self.clock.tick(self.refresh_rate)
