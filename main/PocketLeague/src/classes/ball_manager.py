import pygame
from .ball import Ball

class BallManager:
    
    ball: Ball = Ball()

    @staticmethod
    def get_ball():
        return BallManager.ball
    
    def reset_ball():
        BallManager.ball.reset()
