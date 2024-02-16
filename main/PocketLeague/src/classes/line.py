import pygame

class Line:
    def __init__(self, pos1: tuple, pos2: tuple, bounce_direction: tuple, collisions: bool):
        self.pos1 = pos1
        self.pos2 = pos2
        self.bounce_direction = bounce_direction
        self.collisions = collisions

        assert len(self.pos1) == 2
        assert len(self.pos2) == 2

    def draw(self, surface):
        pygame.draw.line(surface, (255, 255, 255) if self.collisions else (0,0,255), self.pos1, self.pos2, 1)
