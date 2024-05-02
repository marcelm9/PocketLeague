import pygame
import math
from ..files.config import *

class BoostDisplay:
    def __init__(self, center):
        self.__rect = pygame.Rect(0,0,BOOST_DISPLAY_SIZE,BOOST_DISPLAY_SIZE)
        self.__rect.center = center
        self.__fill_factor = PLAYER_BOOST_SECONDS_ON_SPAWN / PLAYER_BOOST_SECONDS

    def update(self, value):
        self.__fill_factor = value / PLAYER_BOOST_SECONDS

    def draw(self, surface):
        pygame.draw.circle(surface, (60,60,60), self.__rect.center, BOOST_DISPLAY_SIZE / 2, BOOST_DISPLAY_LINE_SIZE)
        pygame.draw.arc(surface, (0,255,0), self.__rect, 0, math.radians(360 * self.__fill_factor), BOOST_DISPLAY_LINE_SIZE)