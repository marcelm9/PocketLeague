import pygame
import PygameXtras as px
from .player_stats import PlayerStats
from ..files.config import (
    MATCH_COUNTDOWN,
    MATCH_DURATION_IN_SECONDS,
    WIN_WIDTH,
    DISTANCE_FROM_GOAL_FOR_SHOT_SQUARED,
)

from .field import Field

from .ball_manager import BallManager


class MatchStats:

    __match_time_left: float
    __countdown: float = 0
    __goals_team_blue: int = 0
    __goals_team_orange: int = 0
    __player_stats: dict[str, PlayerStats] = {}
    __last_touches: dict[str, str] = {}

    def _finish_game():
        MatchStats.__match_time_left = 1

    def start_match(players):
        MatchStats.__match_time_left = MATCH_DURATION_IN_SECONDS
        MatchStats.start_countdown()
        MatchStats.__last_touches["Team Blue"] = "Team Blue"
        MatchStats.__last_touches["Team Orange"] = "Team Orange"
        MatchStats.__player_stats.clear()
        for player in players:
            MatchStats.__player_stats[player.get_name()] = PlayerStats()

    def register_goal_for_team_blue():
        MatchStats.__goals_team_blue += 1

    def register_goal_for_team_orange():
        MatchStats.__goals_team_orange += 1

    def get_goals_team_blue():
        return MatchStats.__goals_team_blue

    def get_goals_team_orange():
        return MatchStats.__goals_team_orange

    def get_match_seconds_left():
        return MatchStats.__match_time_left

    def reduce_match_time(dt: float):
        MatchStats.__match_time_left = max(MatchStats.__match_time_left - dt, 0)

    def reduce_countdown(dt: float):
        MatchStats.__countdown = max(MatchStats.__countdown - dt, 0)

    def get_countdown():
        return MatchStats.__countdown

    def start_countdown():
        MatchStats.__countdown = MATCH_COUNTDOWN

    def reset():
        MatchStats.__goals_team_blue = 0
        MatchStats.__goals_team_orange = 0

    def get_player_stats() -> dict[str, PlayerStats]:
        return MatchStats.__player_stats

    def register_shot(player_name: str):
        MatchStats.__player_stats[player_name].shots += 1

    def register_save(player_name: str):
        MatchStats.__player_stats[player_name].saves += 1

    def register_layup(player_name: str):
        MatchStats.__player_stats[player_name].layups += 1

    def __lineLine(line1_start, line1_end, line2_start, line2_end):
        uA = (
            (line2_end[0] - line2_start[0]) * (line1_start[1] - line2_start[1])
            - (line2_end[1] - line2_start[1]) * (line1_start[0] - line2_start[0])
        ) / (
            (line2_end[1] - line2_start[1]) * (line1_end[0] - line1_start[0])
            - (line2_end[0] - line2_start[0]) * (line1_end[1] - line1_start[1])
        )
        uB = (
            (line1_end[0] - line1_start[0]) * (line1_start[1] - line2_start[1])
            - (line1_end[1] - line1_start[1]) * (line1_start[0] - line2_start[0])
        ) / (
            (line2_end[1] - line2_start[1]) * (line1_end[0] - line1_start[0])
            - (line2_end[0] - line2_start[0]) * (line1_end[1] - line1_start[1])
        )
        if (0 <= uA <= 1) and (0 <= uB <= 1):
            return True
        return False

    def handle_player_ball_collision(arbiter, space, data):
        player = data["player"]

        MatchStats.__player_stats[player.get_name()].touches += 1
        MatchStats.__last_touches[player.get_team()] = player.get_name()

        ball_v = pygame.Vector2(BallManager.get_ball().get_direction())
        # if ball_v.length() == 0:
        #     return
        ball_v.scale_to_length(WIN_WIDTH)
        ball_pos = pygame.Vector2(BallManager.get_ball().get_pos())

        if (
            player.get_team() == "Team Orange"
            and MatchStats.__lineLine(
                ball_pos, ball_pos + ball_v, *Field.get_blue_goal_line()
            )
            and (
                (ball_pos[0] - Field.get_blue_goal_center()[0]) ** 2
                + (ball_pos[1] - Field.get_blue_goal_center()[1]) ** 2
            )
            < DISTANCE_FROM_GOAL_FOR_SHOT_SQUARED
        ) or (
            player.get_team() == "Team Blue"
            and MatchStats.__lineLine(
                ball_pos, ball_pos + ball_v, *Field.get_orange_goal_line()
            )
            and (
                (ball_pos[0] - Field.get_orange_goal_center()[0]) ** 2
                + (ball_pos[1] - Field.get_orange_goal_center()[1]) ** 2
            )
            < DISTANCE_FROM_GOAL_FOR_SHOT_SQUARED
        ):
            # shot for player
            MatchStats.__player_stats[player.get_name()].shots += 1

        return True
