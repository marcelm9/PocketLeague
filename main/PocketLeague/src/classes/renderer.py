import pygame

from .ball_manager import BallManager
from .boost_pads_manager import BoostPadsManager
from .field import Field
from .HUD import HUD
from .player_manager import PlayerManager


class Renderer:

    screen: pygame.Surface

    def init(screen: pygame.Surface):
        Renderer.screen = screen

    def reset():
        Renderer.screen = None

    def render():
        Renderer.screen.fill((0,0,0))
        for line in Field.get_lines():
            line.draw(Renderer.screen)


        PlayerManager.draw(Renderer.screen)
        BoostPadsManager.draw(Renderer.screen)
        BallManager.get_ball().draw(Renderer.screen)

        HUD.draw()
