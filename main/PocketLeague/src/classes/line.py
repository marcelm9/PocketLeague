import pygame
from ..files.config import FIELD_LINE_SIZE

class Line:
    def __init__(self, pos1: tuple, pos2: tuple, bounce_direction: tuple, collisions: bool):
        self.pos1 = pos1
        self.pos2 = pos2
        self.bounce_direction = bounce_direction
        self.collisions = collisions

        # debug
        v1 = pygame.Vector2(bounce_direction)
        v1.scale_to_length(10)
        self.__bounce_vector = v1
        v2 = pygame.Vector2(
            self.pos2[0] - self.pos1[0],
            self.pos2[1] - self.pos1[1]
        )
        v2.scale_to_length(
            v2.length() / 2
        )
        self.__center = self.pos1[0] + v2[0], self.pos1[1] + v2[1]

        assert len(self.pos1) == 2
        assert len(self.pos2) == 2

    def draw(self, surface):
        pygame.draw.line(surface, (255, 255, 255) if self.collisions else (0,0,255), self.pos1, self.pos2, FIELD_LINE_SIZE)
        pygame.draw.line(surface, (0,255,0), self.__center, (self.__center[0] + self.__bounce_vector[0], self.__center[1] + self.__bounce_vector[1]), FIELD_LINE_SIZE)
