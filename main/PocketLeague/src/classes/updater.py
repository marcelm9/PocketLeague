import random
import pygame

from .particle_manager import ParticleManager

from ..files.config import (FIELD_LEFT_EDGE, FIELD_RIGHT_EDGE, FPS,
                            TEAM_COLOR_MAP)
from ..ui.after_match_screen import AfterMatchScreen
from .ball_manager import BallManager
from .boost_pads_manager import BoostPadsManager
from .field import Field
from .goal_explosions.goal_explosion_manager import GoalExplosionManager
from .HUD import HUD
from .match_stats import MatchStats
from .player_manager import PlayerManager
from .space import Space


class Updater:

    __fpsclock: pygame.time.Clock

    def init(fpsclock: pygame.time.Clock):
        # needs to be passed in from Game, otherwise the first iteration of .tick is very large
        Updater.__fpsclock = fpsclock

    def reset():
        Updater.__fpsclock = None

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
                elif event.key == pygame.K_SPACE:
                    MatchStats._finish_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    ParticleManager.create_explosion(
                        pygame.mouse.get_pos(),
                        300,
                        3,
                        (255, 0, 0),
                        2,
                        5
                    )

        
        if pygame.mouse.get_pressed()[0]:
            ParticleManager.create_particle(
                pygame.mouse.get_pos(),
                (random.random() * 3 - 1.5, random.random() * -3),
                (255, 204, 0),
                2,
                4,
                0
            )

        HUD.update()

        if MatchStats.get_countdown() > 0:
            return

        state = MatchStats.get_state()

        if state == "game":
            MatchStats.reduce_match_time(dt_s)

        PlayerManager.update(dt_s)
        BallManager.get_ball().update()
        Space.space.step(dt)
        PlayerManager.keep_in_bounds()
        BoostPadsManager.update()
        GoalExplosionManager.update(dt_s)
        ParticleManager.update(dt_s)

        if MatchStats.get_match_seconds_left() == 0:
            if BallManager.get_ball().get_speed() < 0.05:
                return AfterMatchScreen.show()

        if state == "game":
            # check for goals
            ball_pos_x = BallManager.get_ball().get_pos()[0]
            if ball_pos_x < FIELD_LEFT_EDGE or ball_pos_x > FIELD_RIGHT_EDGE:
                if ball_pos_x < FIELD_LEFT_EDGE:
                    # goal right team
                    MatchStats.register_goal("Team Orange")
                    GoalExplosionManager.summon_goal_explosion(
                        MatchStats.get_last_player_touch_by_team("Team Orange"), BallManager.get_ball().get_pos()
                    )
                elif ball_pos_x > FIELD_RIGHT_EDGE:
                    # goal left team
                    MatchStats.register_goal("Team Blue")
                    GoalExplosionManager.summon_goal_explosion(
                        MatchStats.get_last_player_touch_by_team("Team Blue"), BallManager.get_ball().get_pos()
                    )
                HUD.update_score()
                MatchStats.reset_aftergoal_time()
                MatchStats.set_state("aftergoal")

        elif state == "aftergoal":
            MatchStats.reduce_aftergoal_time(dt_s)
            if MatchStats.get_aftergoal_time() == 0:
                BallManager.reset_ball()
                PlayerManager.respawn_players()
                BoostPadsManager.reset_pads()
                MatchStats.set_state("game")
                MatchStats.start_countdown()
                ParticleManager.clear()
