import pygame

from .player_manager import PlayerManager

from .boost_pads_manager import BoostPadsManager

from ..files.config import FPS, FIELD_LEFT_EDGE, FIELD_RIGHT_EDGE
from .ball_manager import BallManager
from .player import Player
from .space import Space
from .match_stats import MatchStats
from .HUD import HUD

class Updater:

    __fpsclock: pygame.time.Clock

    def init(fpsclock: pygame.time.Clock):
        # needs to be passed in from Game, otherwise the first iteration of .tick is very large
        Updater.__fpsclock = fpsclock

    def update():
        dt = Updater.__fpsclock.tick(FPS)
        dt_s = dt / 1000

        if MatchStats.get_countdown() > 0:
            MatchStats.reduce_countdown(dt_s)

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_r:
                    BallManager.reset_ball()
        
        if MatchStats.get_countdown() > 0:
            return
        
        MatchStats.reduce_match_time(dt_s)

        PlayerManager.update(dt_s)

        BallManager.get_ball().update()

        Space.space.step(dt)

        PlayerManager.keep_in_bounds()

        # goals
        ball_pos_x = BallManager.get_ball().get_pos()[0]
        if ball_pos_x < FIELD_LEFT_EDGE or ball_pos_x > FIELD_RIGHT_EDGE:
            if ball_pos_x < FIELD_LEFT_EDGE:
                # goal right team
                MatchStats.goal_team1()
            elif ball_pos_x > FIELD_RIGHT_EDGE:
                # goal left team
                MatchStats.goal_team0()
            HUD.update_score()
            BallManager.reset_ball()
            PlayerManager.respawn_players()
            MatchStats.start_countdown()
            BoostPadsManager.reset_pads()

        BoostPadsManager.update()

        HUD.update()
