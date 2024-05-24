import pygame


class DragonGoalExplosion:
    def __init__(self, position, direction_factor, duration, distance):
        self.__position = position
        self.__direction_factor = direction_factor
        self.__duration = duration
        self.__distance = distance

        self.__time_passed = 0

    def update(self, dt_s):
        self.__time_passed = min(self.__duration, self.__time_passed + dt_s)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface,
            (255, 0, 0),
            (self.__position[0] + (self.__time_passed / self.__duration) * self.__direction_factor * self.__distance, self.__position[1]),
            20
        )

    def is_over(self):
        return self.__time_passed == self.__duration
