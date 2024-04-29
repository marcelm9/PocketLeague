import pygame

from .boost_pads_manager import BoostPadsManager
from .HUD import HUD
from .field import Field
from .ball_manager import BallManager
from .player import Player

class Renderer:

    screen: pygame.Surface

    def init(screen: pygame.Surface):
        Renderer.screen = screen

    def render():
        Renderer.screen.fill((0,0,0))
        for line in Field.get_lines():
            line.draw(Renderer.screen)
        
        BallManager.get_ball().draw(Renderer.screen)
        
        for player in Player.players:
            player.draw(Renderer.screen)
        
        BoostPadsManager.draw(Renderer.screen)
        HUD.draw()
