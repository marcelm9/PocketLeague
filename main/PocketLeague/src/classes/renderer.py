import pygame
from .field import Field
from .ball_manager import BallManager

class Renderer:

    screen: pygame.Surface

    def init(screen: pygame.Surface):
        Renderer.screen = screen

    def render():
        Renderer.screen.fill((0,0,0))
        for line in Field.get_lines():
            line.draw(Renderer.screen)
        
        for ball in BallManager.get_balls():
            ball.draw(Renderer.screen)
