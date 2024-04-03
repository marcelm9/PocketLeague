import pygame
import pymunk

from ..files.config import BALL_COLOR
from .space import Space


class Ball:
    def __init__(self, pos, radius, vector=(0, 0)):
        self.vector = pygame.Vector2(vector)
        self.radius = radius

        self.__body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.__body.position = pos
        self.__body.mass = 1
        self.__shape = pymunk.Circle(self.__body, radius=self.radius)
        self.__shape.density = 1
        self.__shape.elasticity = 1
        self.__shape.friction = 1
        Space.space.add(self.__body, self.__shape)

    def update(self):
        self.__body.velocity *= 0.99

    def draw(self, surface):
        pygame.draw.circle(surface, BALL_COLOR, self.__body.position, self.radius)

    def get_pos(self):
        return self.__body.position
