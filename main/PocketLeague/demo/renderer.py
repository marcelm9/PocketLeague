import PygameXtras as px
import pygame
from .point_manager import PointManager

class Renderer:

    screen: pygame.Surface

    def init(screen: pygame.Surface):
        Renderer.screen = screen
        Renderer.label = px.Label(
            Renderer.screen,
            "Marcel",
            40,
            (250,250),
            textcolor = (178,17,200),
            f = "helvetica",
            bgc = (70,70,80),
            anchor = "center",
            bc = (250,250,250),
            bw = 5,
            xad = 20,
            yad = 20,
            br = 20
        )
        Renderer.label.update_text("Pauli")
        Renderer.label2 = px.Label(
            Renderer.screen,
            "PauliGOAT",
            40,
            Renderer.label.midleft,
            "midright",
        )

    def render():
        Renderer.screen.fill(
            (100,100,100)
        )
        for point in PointManager.get_points():
            point.draw(Renderer.screen)
        Renderer.label.draw()
        Renderer.label2.draw()