import pygame
import PygameXtras as px

class Point:
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.position = position

        self.label = px.Label(None, self.name, 32, px.C(self.position) + px.C(0, -10), "midbottom", tc=(0,0,255))
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.position, 5)
        self.label.draw_to(surface)
