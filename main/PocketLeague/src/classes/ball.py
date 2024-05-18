import pygame
import pymunk

from ..files.config import BALL_COLOR, BALL_RADIUS, BALL_SPAWN
from .space import Space


class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS

        self.__body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.__body.position = BALL_SPAWN
        self.__body.mass = 1
        self.__shape = pymunk.Circle(self.__body, radius=self.radius)
        self.__shape.collision_type = 0
        print(f"Ball collision type =  {self.__shape.collision_type}")
        self.__shape.density = 1
        self.__shape.elasticity = 1
        self.__shape.friction = 1
        Space.space.add(self.__body, self.__shape)

    def get_shape(self):
        return self.__shape

    def update(self):
        self.__body.velocity *= 0.99

    def draw(self, surface):
        pygame.draw.circle(surface, BALL_COLOR, self.__body.position, self.radius)

    def get_pos(self):
        return self.__body.position

    def reset(self):
        self.__body.velocity = (0, 0)
        self.__body.position = BALL_SPAWN

    def get_speed(self):
        return self.__body.velocity.length
