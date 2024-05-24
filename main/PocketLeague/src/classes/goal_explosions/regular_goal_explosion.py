import pygame
from PygameXtras import Function


class RegularGoalExplosion:
    def __init__(self, position, color):
        self.__position = position
        self.__color = color
        self.__thickness = 10
        self.__max_radius = 700
        self.__duration = 1.2

        self.__func = Function()
        self.__func.set_outer_values(0, 1)
        self.__func.add_func("- x ** 10", -0.88, -0.6, self.__duration)

        self.__time_passed = 0

    def update(self, dt_s):
        self.__time_passed = min(self.__duration, self.__time_passed + dt_s)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface,
            self.__color,
            self.__position,
            self.__max_radius * self.__func.get(self.__time_passed),
            self.__thickness,
        )

    def is_over(self):
        return self.__time_passed == self.__duration
