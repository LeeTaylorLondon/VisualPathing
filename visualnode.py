from node import Node
import colors
import pygame

def text_objects(text, font, inp_color):
    text_surface = font.render(text, True, inp_color)
    return text_surface, text_surface.get_rect()

def message_display(text, x, y, inp_color, font_size, screen):
    large_text = pygame.font.Font('freesansbold.ttf', font_size)
    text_surf, text_rect = text_objects(text, large_text, inp_color)  # Text.width is calculated here
    text_rect = (x, y)
    screen.blit(text_surf, text_rect)
    return text_surf

class VisualNode(Node):
    def __init__(self, node, x, y, width):
        super().__init__(node.name, node.node_names, node.node_weights)
        self.color = colors.black
        self.text_color = colors.pycharm_white
        self.font_size = 20
        self.rect = [x, y, width, width]
        self.text_x = self.set_text_x()
        self.text_y = self.set_text_y()
        self.dragged = False

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return "nodeV.{}, {},{}".format(self.name, self.get_x(), self.get_y())

    def set_x(self, x):
        self.rect[0] = x
        self.text_x = self.set_text_x()

    def set_y(self, y):
        self.rect[1] = y
        self.text_y = self.set_text_y()

    def set_xy(self, x, y):
        self.set_x(x)
        self.set_y(y)
        self.text_x = self.set_text_x()
        self.text_y = self.set_text_y()

    def get_x(self):
        return self.rect[0]

    def get_y(self):
        return self.rect[1]

    def get_width(self):
        return self.rect[2]

    def set_text_x(self):
        large_text = pygame.font.Font('freesansbold.ttf', self.font_size)
        text_width = text_objects(self.name.upper(), large_text, self.color)[0].get_width()
        return self.get_x() + (self.get_width() - text_width) / 2

    def set_text_y(self):
        large_text = pygame.font.Font('freesansbold.ttf', self.font_size)
        text_height = text_objects(self.name.upper(), large_text, self.color)[0].get_height()
        return self.get_y() + (self.get_width() - text_height) / 2

    def calc_center(self, text):
        """ Returns (x, y) coordinates of text """
        large_text = pygame.font.Font('freesansbold.ttf', self.font_size)
        text_width = text_objects(text, large_text, self.color)[0].get_width()
        text_height = text_objects(text, large_text, self.color)[0].get_height()
        return self.get_x() + (self.get_width() - text_width) / 2, self.get_y() + (self.get_width() - text_height) / 2

    def display_node(self, screen, mouse_pos, mouse_clicked, debug):
        pygame.draw.ellipse(screen, self.color, self.rect)
        message_display(self.name.upper(), self.text_x, self.text_y, self.text_color, self.font_size, screen)
        while self.get_x() + self.get_width() > mouse_pos[0] > self.get_x() \
                and self.get_y() + self.get_width() > mouse_pos[1] > self.get_y() and mouse_clicked[0]:
            self.dragged = True
            self.set_x(mouse_pos[0] - (self.get_width() / 2))
            self.set_y(mouse_pos[1] - (self.get_width() / 2))
            break

        if debug:  # Draws red hitbox around node circle
            pygame.draw.rect(screen, colors.dark_red, self.rect, 1)
