import random
import time

import pygame

from ..files.config import FIELD_LEFT_EDGE, FIELD_RIGHT_EDGE
from ..ui.after_match_screen import AfterMatchScreen
from ..ui.confirm_screen import ConfirmScreen
from .ball_manager import BallManager
from .boost_pads_manager import BoostPadsManager
from .controller_manager import ControllerManager
from .field import Field
from .goal_explosions.goal_explosion_manager import GoalExplosionManager
from .HUD import HUD
from .match_stats import MatchStats
from .particle_manager import ParticleManager
from .player_manager import PlayerManager
from .sounds import Sounds
from .space import Space


class Updater:

    __fpsclock: pygame.time.Clock
    __simulation_precision: int = 10

    __last_frame_time: float = None

    def init(fpsclock: pygame.time.Clock, simulation_precision: int):
        # needs to be passed in from Game, otherwise the first iteration of .tick is very large
        Updater.__fpsclock = fpsclock
        Updater.__simulation_precision = simulation_precision

    def reset():
        Updater.__fpsclock = None

    def update():

        if Updater.__last_frame_time == None:
            Updater.__last_frame_time = time.time()

        # framerate independence
        now = time.time()
        dt = now - Updater.__last_frame_time
        dt_s = dt  # save for timers and such
        dt *= 120
        Updater.__last_frame_time = now

        if MatchStats.get_countdown() > 0:
            MatchStats.reduce_countdown(dt_s)

        if ControllerManager.has_anyone_pressed_ps_button():
            if ConfirmScreen.ask("Are you sure you want to quit?"):
                return False
            Updater.__last_frame_time = time.time()

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
                    PlayerManager.respawn_players()
                    BoostPadsManager.reset_pads()
                    MatchStats.set_state("game")
                    MatchStats.start_countdown()
                    ParticleManager.clear()
                    MatchStats.reset_tracking_stats()
                    Sounds.stop_all_boost_sounds()
                elif event.key == pygame.K_SPACE:
                    MatchStats._finish_game()
                elif event.key == pygame.K_RETURN:
                    print(f"{Updater.__fpsclock.get_fps() = }")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    ParticleManager.create_explosion(
                        pygame.mouse.get_pos(), 300, 3, (255, 0, 0), 2, 5
                    )

        if pygame.mouse.get_pressed()[0]:
            ParticleManager.create_particle(
                pygame.mouse.get_pos(),
                (random.random() * 3 - 1.5, random.random() * -3),
                (255, 204, 0),
                2,
                4,
                0,
            )

        HUD.update()
        BoostPadsManager.update(dt_s)
        ParticleManager.update(dt, dt_s)

        if MatchStats.get_countdown() > 0:
            return

        state = MatchStats.get_state()

        if state == "game":
            MatchStats.reduce_match_time(dt_s)
        elif state == "overtime":
            MatchStats.increase_overtime(dt_s)

        PlayerManager.update(dt, dt_s)
        BallManager.get_ball().update(dt, dt_s)
        small_step = dt_s / Updater.__simulation_precision
        for _ in range(Updater.__simulation_precision):
            Space.space.step(small_step)
        PlayerManager.keep_in_bounds()
        GoalExplosionManager.update(dt_s)

        if (
            MatchStats.get_state() == "game"
            and MatchStats.get_match_seconds_left() == 0
        ):
            if BallManager.get_ball().get_speed() < 15:
                if (
                    MatchStats.get_goals_team_blue()
                    != MatchStats.get_goals_team_orange()
                ):
                    return AfterMatchScreen.show()
                else:
                    MatchStats.set_state("overtime")
                    BallManager.reset_ball()
                    PlayerManager.respawn_players()
                    BoostPadsManager.reset_pads()
                    MatchStats.start_countdown()
                    ParticleManager.clear()
                    Sounds.stop_all_boost_sounds()
                    return

        if state == "game" or state == "overtime":
            # check for goals
            ball_pos_x, ball_pos_y = BallManager.get_ball().get_pos()
            if ball_pos_x < FIELD_LEFT_EDGE or ball_pos_x > FIELD_RIGHT_EDGE:
                if ball_pos_x < FIELD_LEFT_EDGE and Field.rect_left.collidepoint(
                    ball_pos_x, ball_pos_y
                ):
                    # goal right team
                    MatchStats.register_goal("Team Orange")
                    GoalExplosionManager.summon_goal_explosion(
                        MatchStats.get_last_player_touch_by_team("Team Orange"),
                        BallManager.get_ball().get_pos(),
                    )
                    MatchStats.update_goal_label(
                        "Team Orange",
                        MatchStats.get_last_player_touch_by_team("Team Orange"),
                    )
                elif ball_pos_x > FIELD_RIGHT_EDGE and Field.rect_right.collidepoint(
                    ball_pos_x, ball_pos_y
                ):
                    # goal left team
                    MatchStats.register_goal("Team Blue")
                    GoalExplosionManager.summon_goal_explosion(
                        MatchStats.get_last_player_touch_by_team("Team Blue"),
                        BallManager.get_ball().get_pos(),
                    )
                    MatchStats.update_goal_label(
                        "Team Blue",
                        MatchStats.get_last_player_touch_by_team("Team Blue"),
                    )
                HUD.update_score()
                MatchStats.reset_aftergoal_time()
                if MatchStats.get_state() == "game":
                    MatchStats.set_state("aftergoal")
                elif MatchStats.get_state() == "overtime":
                    MatchStats.set_state("aftergoal_ot")

        elif state == "aftergoal" or state == "aftergoal_ot":
            MatchStats.reduce_aftergoal_time(dt_s)
            if MatchStats.get_aftergoal_time() == 0:
                if MatchStats.get_state() == "aftergoal":
                    BallManager.reset_ball()
                    PlayerManager.respawn_players()
                    BoostPadsManager.reset_pads()
                    MatchStats.set_state("game")
                    MatchStats.start_countdown()
                    ParticleManager.clear()
                    MatchStats.reset_tracking_stats()
                    Sounds.stop_all_boost_sounds()
                elif MatchStats.get_state() == "aftergoal_ot":
                    Sounds.stop_all_boost_sounds()
                    return AfterMatchScreen.show()
