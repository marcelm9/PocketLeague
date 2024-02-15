import pygame
from ..files.config import CENTER


class Field:

    def init(width, height):
        Field.__rect = pygame.Rect(0, 0, width, height)
        Field.__rect.center = CENTER

        Field.left = Field.__rect.left
        Field.right = Field.__rect.right
        Field.top = Field.__rect.top
        Field.bottom = Field.__rect.bottom

    def get_rect():
        return Field.__rect
