import pygame
from .field import Field

class Renderer:

    screen: pygame.Surface

    def init(screen: pygame.Surface):
        Renderer.screen = screen

    def render():
        pygame.draw.rect(Renderer.screen, (255, 255, 255), Field.get_rect(), 1)
