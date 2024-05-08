import time

import pygame

from .player_manager import PlayerManager

from ..files.colors import BOOST_PAD_COLOR_ACTIVE, BOOST_PAD_COLOR_INACTIVE
from ..files.config import BOOST_PAD_RADIUS, BOOST_PAD_RECHARGE_TIME


class BoostPad:
    def __init__(self, center):
        self.__center = center
        self.reset()

    def update(self):
        if not self.__collectable and (
            time.time() - self.__last_time_collected >= BOOST_PAD_RECHARGE_TIME
        ):
            self.__collectable = True
        
        if self.__collectable:
            for player in PlayerManager.get_players():
                if player.collides_with(self.__center, BOOST_PAD_RADIUS):
                    player.recharge_boost()
                    self.__last_time_collected = time.time()
                    self.__collectable = False

    def draw(self, surface):
        if self.__collectable:
            pygame.draw.circle(surface, BOOST_PAD_COLOR_ACTIVE, self.__center, BOOST_PAD_RADIUS)
        else:
            pygame.draw.circle(surface, BOOST_PAD_COLOR_INACTIVE, self.__center, BOOST_PAD_RADIUS)

    def reset(self):
        self.__last_time_collected = 0
        self.__collectable = True
