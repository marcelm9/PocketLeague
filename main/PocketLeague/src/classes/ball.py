import pygame
import pymunk

from ..files.config import BALL_COLOR, BALL_RADIUS, BALL_SPAWN
from .particle_manager import Particle
from .space import Space


class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS

        self.__body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.__body.position = BALL_SPAWN
        self.__body.mass = 1
        self.__shape = pymunk.Circle(self.__body, radius=self.radius)
        self.__shape.collision_type = 0
        self.__shape.density = 1
        self.__shape.elasticity = 1
        self.__shape.friction = 1
        Space.space.add(self.__body, self.__shape)

        self.__particles: list[Particle] = []

    def get_shape(self):
        return self.__shape

    def update(self, dt_s):
        self.__body.velocity *= 0.99
        self.__particles = [p for p in self.__particles if p.time_passed < p.duration]
        self.__particles.append(
            Particle(list(self.get_pos()), (0, 0), BALL_COLOR, 0.1, BALL_RADIUS, 0)
        )
        for p in self.__particles:
            p.time_passed += dt_s

    def draw(self, surface):
        pygame.draw.circle(surface, BALL_COLOR, self.__body.position, self.radius)
        for p in self.__particles:
            pygame.draw.circle(
                surface,
                p.color,
                p.pos,
                min(1, p.time_passed / p.duration) * (p.radius_end - p.radius_start)
                + p.radius_start,
            )

    def get_pos(self):
        return self.__body.position

    def reset(self):
        self.__body.velocity = (0, 0)
        self.__body.position = BALL_SPAWN
        self.__particles.clear()

    def get_speed(self):
        return self.__body.velocity.length

    def get_direction(self):
        return tuple(self.__body.velocity)
