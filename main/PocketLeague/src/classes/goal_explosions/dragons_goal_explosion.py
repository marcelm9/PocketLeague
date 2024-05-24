import math
import pygame

from ..particle_manager import ParticleManager


class DragonGoalExplosion:
    def __init__(self, position, direction_factor):
        self.__position = position
        self.__direction_factor = direction_factor
        self.__duration = 2
        self.__distance = 700

        self.__time_passed = 0

        self.__func = lambda x: math.sin(20 * x) * x * 0.1
        self.__pos_x_difference = 0
        self.__pos_y_difference = 0
        self.__radius = 10

    def update(self, dt_s):
        self.__time_passed = min(self.__duration, self.__time_passed + dt_s)
        self.__pos_x_difference = (
            (self.__time_passed / self.__duration)
            * self.__direction_factor
            * self.__distance
        )
        self.__pos_y_difference = 1900 * self.__func(
            (self.__time_passed / self.__duration) * 0.4
        )
        self.__radius = max(10, 35 * (self.__time_passed / self.__duration))
        ParticleManager.create_particle(
            (
                self.__position[0] + self.__pos_x_difference,
                self.__position[1] + self.__pos_y_difference,
            ),
            (0, 0),
            (255, 105, 180),
            0.7,
            self.__radius,
            0,
        )
        ParticleManager.create_particle(
            (
                self.__position[0] + self.__pos_x_difference,
                self.__position[1] - self.__pos_y_difference,
            ),
            (0, 0),
            (0, 0, 139),
            0.7,
            self.__radius,
            0,
        )

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface,
            (255, 105, 180),
            (
                self.__position[0] + self.__pos_x_difference,
                self.__position[1] + self.__pos_y_difference,
            ),
            self.__radius,
        )
        pygame.draw.circle(
            surface,
            (0, 0, 139),
            (
                self.__position[0] + self.__pos_x_difference,
                self.__position[1] - self.__pos_y_difference,
            ),
            self.__radius,
        )

    def is_over(self):
        return self.__time_passed == self.__duration
