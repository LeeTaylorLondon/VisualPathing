import colors
import pygame
from visualnode import message_display, text_objects

class VisualVertex:
    def __init__(self, nodeS, nodeE, cost):
        self.nodeS = nodeS  # nodeS -> Starting Node
        self.nodeE = nodeE  # nodeE -> Ending Node
        self.start_point = self.init_start_point()  # [x, y]
        self.end_point = self.init_end_point()      # [x, y]
        self.line_width = 3

        self.vertex_color = colors.blue
        self.vertex_width = self.end_point[0] - self.start_point[0]
        self.vertex_height = self.end_point[1] - self.start_point[1]

        self.cost = cost
        self.cost_font_size = 18
        self.cost_color = colors.pycharm_white
        self.cost_point = self.init_cost_point()
        self.cost_text_x = self.init_cost_text_x()
        self.cost_text_y = self.init_cost_text_y()

    def __repr__(self):
        return '{} -> {}'.format(self.nodeS, self.nodeE)

    def init_cost_point(self):
        return (self.start_point[0] + ((self.end_point[0] - self.start_point[0]) / 2)), \
               self.start_point[1] + ((self.end_point[1] - self.start_point[1]) / 2)

    def init_cost_text_x(self):
        large_text = pygame.font.Font('freesansbold.ttf', self.cost_font_size)
        text_width = text_objects(str(self.cost), large_text, self.cost_color)[0].get_width()
        return self.start_point[0] + (self.vertex_width - text_width) / 2

    def init_cost_text_y(self):
        large_text = pygame.font.Font('freesansbold.ttf', self.cost_font_size)
        text_height = text_objects(str(self.cost), large_text, self.cost_color)[0].get_height()
        return self.start_point[1] + (self.vertex_height - text_height) / 2

    def init_start_point(self):
        """ Returns ([x, y] --> start_point) """
        return [self.nodeS.get_x() + (self.nodeS.get_width() / 2), self.nodeS.get_y() + (self.nodeS.get_width() / 2)]

    def init_end_point(self):
        """ Returns ([x, y] --> end_point) """
        return [self.nodeE.get_x() + (self.nodeS.get_width() / 2), self.nodeE.get_y() + (self.nodeS.get_width() / 2)]

    def to_string(self):
        return '{} {}'.format(self.nodeS.name, self.nodeE.name)

    def to_string_reverse(self):
        return '{} {}'.format(self.nodeE.name, self.nodeS.name)

    # Surface, color, start_pos, end_pos, width=1):
    def display_vertex(self, screen, debug):
        pygame.draw.line(screen, self.vertex_color, self.start_point, self.end_point, self.line_width)
        message_display(str(self.cost), self.cost_text_x, self.cost_text_y, self.cost_color, self.cost_font_size,
                        screen)
        if debug:  # Draws purple hitbox around vertex line
            pygame.draw.rect(screen, colors.purple, [self.start_point[0], self.start_point[1], self.vertex_width,
                                                    self.vertex_height], 1)