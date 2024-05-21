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

    def draw(self, surface):
        pygame.draw.line(surface, self.__color, self.pos1, self.pos2, FIELD_LINE_SIZE)
        pygame.draw.circle(surface, self.__color, self.pos1, FIELD_LINE_SIZE // 2)
        pygame.draw.circle(surface, self.__color, self.pos2, FIELD_LINE_SIZE // 2)
