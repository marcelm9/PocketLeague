import random
from typing import Literal
import pygame
import PygameXtras as px
from .player_stats import PlayerStats
from ..files.config import (
    MATCH_COUNTDOWN,
    MATCH_DURATION_IN_SECONDS,
    WIN_WIDTH,
    DISTANCE_FROM_GOAL_FOR_SHOT_SQUARED,
    AFTER_GOAL_SECONDS
)

from .field import Field

from .ball_manager import BallManager


class MatchStats:

    __match_time_left: float
    __countdown: float = 0
    __goals_team_blue: int = 0
    __goals_team_orange: int = 0
    __player_stats: dict[str, PlayerStats] = {}
    __last_touches_dict: dict[str, str] = {}
    __last_shot_by = None
    __last_touches_list: list[str] = [] # oldest touch ... newest touch
    __player_team_map: dict[str, str]

    __state = "game" # game, aftergoal
    __aftergoal_time = 0

    def reset_aftergoal_time():
        MatchStats.__aftergoal_time = AFTER_GOAL_SECONDS

    def get_aftergoal_time():
        return MatchStats.__aftergoal_time

    def reduce_aftergoal_time(dt: float):
        MatchStats.__aftergoal_time = max(MatchStats.__aftergoal_time - dt, 0)

    def set_state(state: str):
        assert state in ["game", "aftergoal"]
        MatchStats.__state = state

    def get_last_player_touch_by_team(team: Literal["Team Blue", "Team Orange"]):
        return MatchStats.__last_touches_dict[team]

    def get_state():
        return MatchStats.__state

    def _finish_game():
        MatchStats.__match_time_left = 1

    def start_match(players):
        MatchStats.__goals_team_blue = 0
        MatchStats.__goals_team_orange = 0
        MatchStats.__last_touches_dict = {
            "Team Blue": None,
            "Team Orange": None
        }
        MatchStats.__last_shot_by = None
        MatchStats.__match_time_left = MATCH_DURATION_IN_SECONDS
        MatchStats.__last_touches_list.clear()
        MatchStats.__player_team_map = {
            p: t for p, t in [
                (player_.get_name(), player_.get_team()) for player_ in players
            ]
        }
        MatchStats.start_countdown()
        MatchStats.__player_stats.clear()
        for player in players:
            MatchStats.__player_stats[player.get_name()] = PlayerStats()

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

    def register_goal(team_name: str):
        assert team_name in ["Team Blue", "Team Orange"]

        if team_name == "Team Blue":
            MatchStats.__goals_team_blue += 1
            if MatchStats.__last_touches_dict.get("Team Blue", None) is not None:
                MatchStats.__player_stats[MatchStats.__last_touches_dict["Team Blue"]].goals += 1
            
                # if there is a player of the blue team in the last three touches, award an assist
                for name in MatchStats.__last_touches_list[::-1]:
                    if name != MatchStats.__last_touches_dict["Team Blue"] and MatchStats.__player_team_map[name] == "Team Blue":
                        MatchStats.__player_stats[name].assists += 1
                        break
        elif team_name == "Team Orange":
            MatchStats.__goals_team_orange += 1
            if MatchStats.__last_touches_dict.get("Team Orange", None) is not None:
                MatchStats.__player_stats[MatchStats.__last_touches_dict["Team Orange"]].goals += 1
            
                # if there is a player of the orangeteam in the last three touches, award an assist
                for name in MatchStats.__last_touches_list[::-1]:
                    if name != MatchStats.__last_touches_dict["Team Orange"] and MatchStats.__player_team_map[name] == "Team Orange":
                        MatchStats.__player_stats[name].assists += 1
                        break

    def handle_player_ball_collision(arbiter, space, data):
        player = data["player"]

        MatchStats.__last_touches_list.append(player.get_name())
        if len(MatchStats.__last_touches_list) > 3:
            MatchStats.__last_touches_list = MatchStats.__last_touches_list[-3:]

        MatchStats.__player_stats[player.get_name()].touches += 1
        MatchStats.__last_touches_dict[player.get_team()] = player.get_name()

        ball_vect = pygame.Vector2(BallManager.get_ball().get_direction())
        if ball_vect.length() > 0:
            ball_vect.scale_to_length(WIN_WIDTH)
        ball_pos = pygame.Vector2(BallManager.get_ball().get_pos())

        if MatchStats.__last_shot_by is not None:
            if (
                player.get_team() == "Team Orange"
                and MatchStats.__last_shot_by == "Team Blue"
                and not px.Collisions.line_line(
                    ball_pos, ball_pos + ball_vect, *Field.get_orange_goal_line()
                )
            ) or (
                player.get_team() == "Team Blue"
                and MatchStats.__last_shot_by == "Team Orange"
                and not px.Collisions.line_line(
                    ball_pos, ball_pos + ball_vect, *Field.get_blue_goal_line()
                )
            ):
                # save for player
                MatchStats.__player_stats[player.get_name()].saves += 1
            MatchStats.__last_shot_by = None

        if (
            player.get_team() == "Team Orange"
            and px.Collisions.line_line(
                ball_pos, ball_pos + ball_vect, *Field.get_blue_goal_line()
            )
            and (
                (ball_pos[0] - Field.get_blue_goal_center()[0]) ** 2
                + (ball_pos[1] - Field.get_blue_goal_center()[1]) ** 2
            )
            < DISTANCE_FROM_GOAL_FOR_SHOT_SQUARED
        ) or (
            player.get_team() == "Team Blue"
            and px.Collisions.line_line(
                ball_pos, ball_pos + ball_vect, *Field.get_orange_goal_line()
            )
            and (
                (ball_pos[0] - Field.get_orange_goal_center()[0]) ** 2
                + (ball_pos[1] - Field.get_orange_goal_center()[1]) ** 2
            )
            < DISTANCE_FROM_GOAL_FOR_SHOT_SQUARED
        ):
            # shot for player
            MatchStats.__player_stats[player.get_name()].shots += 1
            MatchStats.__last_shot_by = player.get_team()

        return True

    def _inject_test(players):
        goals = [3, 1]
        MatchStats.__goals_team_blue = goals.pop(random.randint(0, 1))
        MatchStats.__goals_team_orange = goals.pop(0)

        for p in players:
            MatchStats.__player_stats[p[0]] = PlayerStats()
            MatchStats.__player_stats[p[0]].touches = random.randint(5, 30)
            MatchStats.__player_stats[p[0]].goals = random.randint(0, 1)
            MatchStats.__player_stats[p[0]].saves = random.randint(0, 2)
            MatchStats.__player_stats[p[0]].assists = random.randint(0, 2)
            MatchStats.__player_stats[p[0]].shots = random.randint(0, 5)
