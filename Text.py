import pygame


class Text:

    def __init__(self, text, x_pos, y_pos, font_size, font_color, bg_color=(0, 0, 0), padding=3, isSelected=False, font_file='coolfont.ttf'):

        self.font = pygame.font.Font(font_file, font_size)

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
