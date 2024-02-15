import pygame
from .point_manager import PointManager

class Renderer:

    screen: pygame.Surface

    def init(screen: pygame.Surface):
        Renderer.screen = screen

    def render():
        Renderer.screen.fill(
            (0,0,0)
        )
        for point in PointManager.get_points():
            point.draw(Renderer.screen)
