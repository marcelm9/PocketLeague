import pygame

from .classes.player_config_manager import PlayerConfigManager

from .classes.ball_manager import BallManager
from .classes.boost_pads_manager import BoostPadsManager
from .classes.field import Field
from .classes.HUD import HUD
from .classes.match_stats import MatchStats
from .classes.player import Player
from .classes.renderer import Renderer
from .classes.updater import Updater
from .files.config import *


class Game:

    screen: pygame.Surface = None
    fpsclock: pygame.time.Clock = None

    def init(screen: pygame.Surface):
        Game.screen = screen
        Game.fpsclock = pygame.time.Clock()

    def debug():
        Game.init(
            pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), display=0, flags = pygame.FULLSCREEN | pygame.SCALED)
        )
        Game.start()

    def __configure():
        if len(PlayerConfigManager.get_player_configs()) < 2:
            print(f"At least two players have to be registered (currently {len(PlayerConfigManager.get_player_configs())})")
            return False

        for cfg in PlayerConfigManager.get_player_configs():
            p = Player()
            p.set_name(cfg.name)
            p.set_team({"Team Blue": 0, "Team Orange": 1}[cfg.team])
            p.set_color(COLOR_MAP[cfg.color])
            p.set_boost_type(cfg.boost)
            p.set_goal_explosion(cfg.goal_explosion)
            p.set_controller_input(
                cfg.controller_id,
                *({"left": (0, 9), "right": (1, 10)}[cfg.controller_side])
            )

        Field.init()

    def start():
        if Game.__configure() == False:
            # TODO: improve handling
            return
        
        if Game.screen is None:
            Game.init(
                pygame.display.get_surface()
            )

        Player.reset_all_player_positions()
        HUD.init(Game.screen)
        Renderer.init(Game.screen)
        BallManager.create_ball()
        MatchStats.start_match()
        HUD.update_time_display()
        BoostPadsManager.init()

        while True:
            
            Updater.update()
            Renderer.render()
            
            pygame.display.flip()
            pygame.display.set_caption(f"fps: {Game.fpsclock.get_fps()}")
