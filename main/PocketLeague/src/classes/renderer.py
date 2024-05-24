import pygame

from .particle_manager import ParticleManager

from .ball_manager import BallManager
from .boost_pads_manager import BoostPadsManager
from .field import Field
from .goal_explosions.goal_explosion_manager import GoalExplosionManager
from .HUD import HUD
from .match_stats import MatchStats
from .player_manager import PlayerManager


class Renderer:

    screen: pygame.Surface

    def init(screen: pygame.Surface):
        Renderer.screen = screen

    def reset():
        Renderer.screen = None

    def render():
        Renderer.screen.fill((0, 0, 0))
        for line in Field.get_lines():
            line.draw(Renderer.screen)

        if MatchStats.get_state() != "aftergoal":
            BallManager.get_ball().draw(Renderer.screen)
        PlayerManager.draw(Renderer.screen)
        BoostPadsManager.draw(Renderer.screen)
        GoalExplosionManager.draw(Renderer.screen)
        ParticleManager.draw(Renderer.screen)
        HUD.draw()
