import pygame


class Text:

    def __init__(self, text, x_pos, y_pos, font_size, font_color, bg_color=(0, 0, 0), padding=3, isSelected=False, font_file='coolfont.ttf', underline=False):

        self.font = pygame.font.Font(font_file, font_size)
        self.font.set_underline(underline)
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font_color = font_color
        self.padding = padding
        self.isSelected = isSelected

        self.name = self.font.render(
            self.text, True, self.font_color, bg_color)
        self.rect = self.name.get_rect(center=(self.x_pos, self.y_pos))
        self.rectangle_rect = self.rect.inflate(self.padding, self.padding)

    def setBackgroundColor(self, bg_color: tuple):
        self.name = self.font.render(
            self.text, True, self.font_color, bg_color)

    def setSelected(self, isSelected: bool):
        self.isSelected = isSelected

    def get_hitbox(self, x_pos, y_pos, x_offset = 0):
        hitbox = self.rect.inflate(x_pos,y_pos)
        hitbox.x += x_offset
        return hitbox

    def update_text(self, new_text):
        self.text = new_text
        self.name = self.font.render(self.text, True, self.font_color)
        self.rect = self.name.get_rect(center=(self.x_pos, self.y_pos))