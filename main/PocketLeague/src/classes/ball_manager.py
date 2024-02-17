import pygame
from .ball import Ball

class BallManager:
    
    balls: list[Ball] = []

    @staticmethod
    def add_ball(pos, radius, vector = (0,0)):
        assert isinstance(pos, (tuple, list))
        assert len(pos) == 2
        assert isinstance(vector, (tuple, list, pygame.Vector2))
        assert len(pos) == 2
        BallManager.balls.append(
            Ball(pos, radius, vector)
        )

    @staticmethod
    def get_balls():
        return BallManager.balls
