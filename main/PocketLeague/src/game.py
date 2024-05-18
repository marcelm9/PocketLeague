import pygame

from .ui.after_match_screen import AfterMatchScreen

from .classes.player_manager import PlayerManager

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
        PlayerConfigManager._use_debug_configs()
        Game.start()

    def __configure():
        if len(PlayerConfigManager.get_player_configs()) < 2:
            print(f"At least two players have to be registered (currently {len(PlayerConfigManager.get_player_configs())})")
            return False

        for cfg in PlayerConfigManager.get_player_configs():
            PlayerManager.summon_player(
                cfg.name,
                cfg.team,
                cfg.color,
                cfg.boost_type,
                cfg.goal_explosion,
                cfg.controller_id,
                cfg.controller_side
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

        Updater.init(Game.fpsclock)
        AfterMatchScreen.init(Game.fpsclock, Game.screen)
        Renderer.init(Game.screen)
        PlayerManager.respawn_players()
        HUD.init(Game.screen)
        MatchStats.start_match()
        HUD.update_time_display()
        BoostPadsManager.init()

        while True:
            
            Updater.update()
            Renderer.render()
            
            pygame.display.flip()
            # pygame.display.set_caption(f"fps: {Game.fpsclock.get_fps()}")
