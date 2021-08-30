import pygame
from visualnode import message_display

class Button:
    def __init__(self, screen, btn_color, x, y, width, height, text, txt_color, font_size, on_click_function):
        self.screen = screen
        self.btn_color = btn_color
        self.rect = [x, y, width, height]
        self.text = text
        self.text_color = txt_color
        self.font_size = font_size
        self.clicked = False
        self.on_click_function = on_click_function

    def get_x(self):
        return self.rect[0]

    def get_y(self):
        return self.rect[1]

    def get_width(self):
        return self.rect[2]

    def get_height(self):
        return self.rect[3]

    def action(self, *args, **kwargs):
        self.on_click_function(*args, **kwargs)

    def render(self, mouse_pos, mouse_clicked):
        pygame.draw.rect(self.screen, self.btn_color, self.rect)
        message_display(self.text, self.get_x(), self.get_y(), self.text_color, self.font_size, self.screen)
        # Check bounds for clicking
        while self.get_x() + self.get_width() > mouse_pos[0] > self.get_x() and \
            self.get_y() + self.get_height() > mouse_pos[1] > self.get_y() and mouse_clicked[0] and not(self.clicked):
            self.clicked = True