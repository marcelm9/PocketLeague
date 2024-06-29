import math
import random
import time

import pygame

from ..files.colors import BOOST_PAD_COLOR_ACTIVE, BOOST_PAD_COLOR_INACTIVE
from ..files.config import BOOST_PAD_RADIUS, BOOST_PAD_RECHARGE_TIME
from .particle_manager import Particle
from .player_manager import PlayerManager


class BoostPad:
    def __init__(self, center):
        self.__center = center
        self.__particles: list[Particle] = []
        self.reset()

    def update(self, dt_s):
        if not self.__collectable and (
            time.time() - self.__last_time_collected >= BOOST_PAD_RECHARGE_TIME
        ):
            self.__collectable = True

        if self.__collectable:
            # removing old particles
            self.__particles = [
                p for p in self.__particles if p.time_passed < p.duration
            ]

            # generating a new particle
            r = random.random() * math.pi * 2
            self.__particles.append(
                Particle(
                    list(self.__center),
                    (math.sin(r) * 0.2, math.cos(r) * 0.2),
                    BOOST_PAD_COLOR_ACTIVE,
                    0.8,
                    5,
                    2,
                )
            )

            # updating particles
            for p in self.__particles:
                p.time_passed += dt_s
                p.pos[0] += p.vec[0]
                p.pos[1] += p.vec[1]

            for player in PlayerManager.get_players():
                if player.collides_with(self.__center, BOOST_PAD_RADIUS):
                    player.recharge_boost()
                    self.__last_time_collected = time.time()
                    self.__collectable = False
                    self.__particles.clear()

    def draw(self, surface):
        if self.__collectable:
            pygame.draw.circle(
                surface, BOOST_PAD_COLOR_ACTIVE, self.__center, BOOST_PAD_RADIUS
            )
            for p in self.__particles:
                pygame.draw.circle(
                    surface,
                    p.color,
                    p.pos,
                    min(1, p.time_passed / p.duration) * (p.radius_end - p.radius_start)
                    + p.radius_start,
                )
        else:
            pygame.draw.circle(
                surface, BOOST_PAD_COLOR_INACTIVE, self.__center, BOOST_PAD_RADIUS
            )

    def reset(self):
        self.__last_time_collected = 0
        self.__collectable = True
        self.__particles.clear()
