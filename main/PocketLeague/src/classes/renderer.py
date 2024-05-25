import pygame

from .background import Background
from .ball_manager import BallManager
from .boost_pads_manager import BoostPadsManager
from .field import Field
from .goal_explosions.goal_explosion_manager import GoalExplosionManager
from .HUD import HUD
from .match_stats import MatchStats
from .particle_manager import ParticleManager
from .player_manager import PlayerManager


class Renderer:

    screen: pygame.Surface

    def init(screen: pygame.Surface):
        Renderer.screen = screen

    def reset():
        Renderer.screen = None

    def render():
        Renderer.screen.fill((0, 0, 0))
        Background.draw(Renderer.screen)

        for line in Field.get_lines():
            line.draw(Renderer.screen)
        for line in Field.get_goal_lines():
            line.draw(Renderer.screen)

        BoostPadsManager.draw(Renderer.screen)
        ParticleManager.draw(Renderer.screen)

        if MatchStats.get_state() == "game" or MatchStats.get_state() == "overtime":
            BallManager.get_ball().draw(Renderer.screen)
        else:
            MatchStats.get_goal_label().draw_to(Renderer.screen)

        GoalExplosionManager.draw(Renderer.screen)
        PlayerManager.draw(Renderer.screen)
        HUD.draw()
