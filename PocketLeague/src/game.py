import pygame

from .classes.ball_manager import BallManager
from .classes.boost_pads_manager import BoostPadsManager
from .classes.field import Field
from .classes.goal_explosions.goal_explosion_manager import GoalExplosionManager
from .classes.HUD import HUD
from .classes.match_stats import MatchStats
from .classes.player_config_manager import PlayerConfigManager
from .classes.player_manager import PlayerManager
from .classes.renderer import Renderer
from .classes.sounds import Sounds
from .classes.space import Space
from .classes.updater import Updater
from .files.config import *
from .ui.after_match_screen import AfterMatchScreen


class Game:

    screen: pygame.Surface = None
    fpsclock: pygame.time.Clock = None

    __map: str = "Regular map"
    __time: int = 120
    __ball_bounciness: float = 1
    __boost_capacity: float = 1

    def init(screen: pygame.Surface, fpsclock: pygame.time.Clock):
        Game.screen = screen
        Game.fpsclock = fpsclock

    def __configure_players():
        if len(PlayerConfigManager.get_player_configs()) < 2:
            raise Exception(
                f"At least two players have to be registered (currently {len(PlayerConfigManager.get_player_configs())})"
            )

        for cfg in PlayerConfigManager.get_player_configs():
            PlayerManager.summon_player(
                cfg.name,
                cfg.team,
                cfg.color,
                cfg.boost_type,
                cfg.controller_id,
                cfg.controller_side,
                Game.__boost_capacity,
            )

    def set_settings(map: str, time: int, ball_bounciness: float, boost_capacity):
        Game.__map = map
        Game.__time = time
        Game.__ball_bounciness = ball_bounciness
        Game.__boost_capacity = boost_capacity

    def start():

        Space.init(MatchStats.handle_player_ball_collision)
        Game.__configure_players()
        Field.init(Game.__map)
        BoostPadsManager.init()
        Updater.init(Game.fpsclock, SIMULATION_PRECISION_MAP[Game.__ball_bounciness])
        AfterMatchScreen.init(Game.fpsclock, Game.screen)
        Renderer.init(Game.screen)
        MatchStats.start_match(PlayerManager.get_players(), time=Game.__time)
        HUD.init(Game.screen)
        PlayerManager.respawn_players()
        HUD.update_time_display()
        BallManager.create_ball(BALL_BOUNCINESS_MAP[Game.__ball_bounciness])

        while True:

            if (return_value := Updater.update()) != None:
                break
            Renderer.render()

            pygame.display.flip()
            Game.fpsclock.tick(FPS)

        # reset everything
        Space.reset()
        PlayerManager.reset()
        Field.reset()
        Updater.reset()
        Renderer.reset()
        AfterMatchScreen.reset()
        HUD.reset()
        BoostPadsManager.reset()
        GoalExplosionManager.reset()
        BallManager.destroy_ball()
        MatchStats.reset()
        Sounds.reset()

        return return_value
