import pygame
from .ball import Ball

class BallManager:
    
    balls: list[Ball] = []

    def add_ball(pos, vector, radius, speed):
        assert isinstance(pos, (tuple, list))
        assert len(pos) == 2
        assert isinstance(vector, (tuple, list, pygame.Vector2))
        assert len(pos) == 2
        BallManager.balls.append(
            Ball(pos, vector, radius, speed)
        )

    def get_balls():
        return BallManager.balls
