import pygame
from .field import Field
from .module_collisions import Collisions
from ..files.config import BALL_MAX_SPEED, BALL_COLOR

class Ball:
    def __init__(self, pos, vector, radius):
        self.pos = list(pos)
        self.vector = pygame.Vector2(vector)
        self.radius = radius

    def update(self):
        self.pos[0] += self.vector[0]
        self.pos[1] += self.vector[1]

        for line in Field.get_lines():
            if dist := Collisions.lineCircle(line.pos1, line.pos2, self.pos, self.radius):
                self.mirror_around_vector(line.bounce_direction)
                v = pygame.Vector2(line.bounce_direction)
                v.scale_to_length(dist * 2)
                self.pos[0] += v[0]
                self.pos[1] += v[1]

    def draw(self, surface):
        pygame.draw.circle(surface, BALL_COLOR, self.pos, self.radius)

    def mirror_around_vector(self, vector):
        dot_product = 2 * self.vector.dot(vector)
        self.vector -= dot_product * vector
