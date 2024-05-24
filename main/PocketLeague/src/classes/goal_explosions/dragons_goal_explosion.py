import math
import pygame


class DragonGoalExplosion:
    def __init__(self, position, direction_factor, duration, distance):
        self.__position = position
        self.__direction_factor = direction_factor
        self.__duration = duration
        self.__distance = distance

        self.__time_passed = 0

        self.__func = lambda x: math.sin(20 * x) * x * 0.1

    def update(self, dt_s):
        self.__time_passed = min(self.__duration, self.__time_passed + dt_s)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface,
            (255, 105, 180),
            (
                self.__position[0] + (self.__time_passed / self.__duration) * self.__direction_factor * self.__distance,
                self.__position[1] + 1900 * self.__func((self.__time_passed / self.__duration) * 0.4),
            ),
            max(10, 35 * (self.__time_passed / self.__duration)),
        )
        pygame.draw.circle(
            surface,
            (0, 0, 139),
            (
                self.__position[0] + (self.__time_passed / self.__duration) * self.__direction_factor * self.__distance,
                self.__position[1] - 1900 * self.__func((self.__time_passed / self.__duration) * 0.4),
            ),
            max(10, 35 * (self.__time_passed / self.__duration)),
        )

    def is_over(self):
        return self.__time_passed == self.__duration
