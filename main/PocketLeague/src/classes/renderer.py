import pygame
from .field import Field

class Renderer:

    screen: pygame.Surface

    def init(screen: pygame.Surface):
        Renderer.screen = screen

    def render():
        Renderer.screen.fill((0,0,0))
        for line in Field.get_lines():
            line.draw(Renderer.screen)
