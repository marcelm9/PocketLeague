import pygame
from ..files.config import FIELD_LINE_SIZE

class Line:
    def __init__(self, pos1: tuple, pos2: tuple, bounce_direction: tuple, color):
        self.pos1 = pos1
        self.pos2 = pos2
        self.__bounce_direction = bounce_direction
        self.__color = color

    def get_bounce_direction(self):
        return self.__bounce_direction

    def draw(self, surface, size_factor=1):
        pygame.draw.line(surface, self.__color, self.pos1, self.pos2, FIELD_LINE_SIZE * 2 * size_factor)
