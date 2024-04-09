import pygame
import time

from ..files.config import FPS, FIELD_LEFT_EDGE, FIELD_RIGHT_EDGE, MATCH_DURATION_IN_SECONDS
from .ball_manager import BallManager
from .player import Player
from .space import Space
from .match_stats import MatchStats
from .HUD import HUD

class Updater:

    __fpsclock = pygame.time.Clock()

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
        
        if MatchStats.get_countdown() > 0:
            return
        
        MatchStats.reduce_match_time(dt_s)

        for player in Player.players:
            player.update()

        BallManager.get_ball().update()

        Space.space.step(dt)

        for player in Player.players:
            player.keep_in_bounds()

        # goals
        ball_pos_x = BallManager.get_ball().get_pos()[0]
        if ball_pos_x < FIELD_LEFT_EDGE:
            # goal right team
            MatchStats.goal_team1()
            HUD.update_score()
            BallManager.reset_ball()
            Player.reset_all_player_positions()
            MatchStats.start_countdown()
        elif ball_pos_x > FIELD_RIGHT_EDGE:
            # goal left team
            MatchStats.goal_team0()
            HUD.update_score()
            BallManager.reset_ball()
            Player.reset_all_player_positions()
            MatchStats.start_countdown()

        HUD.update_time_display()
