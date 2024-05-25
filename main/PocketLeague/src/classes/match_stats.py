import random
from typing import Literal

import pygame
import PygameXtras as px

from ..files.config import (
    AFTER_GOAL_SECONDS,
    DISTANCE_FROM_GOAL_FOR_SHOT_SQUARED,
    MATCH_COUNTDOWN,
    MATCH_DURATION_IN_SECONDS,
    TEAM_COLOR_MAP,
    WIN_WIDTH,
)
from .ball_manager import BallManager
from .field import Field
from .player_stats import PlayerStats
from .sounds import Sounds


class MatchStats:

    __match_time_left: float
    __countdown: float = 0
    __countdown_last_integer: int = None
    __goals_team_blue: int
    __goals_team_orange: int
    __player_stats: dict[str, PlayerStats] = {}
    __last_touches_dict: dict[str, str] = {}
    __last_shot_by = None
    __last_touches_list: list[str] = []  # oldest touch ... newest touch
    __player_team_map: dict[str, str]

    __state: Literal["game", "aftergoal", "overtime", "aftergoal_ot"] = "game"
    __aftergoal_time = 0

    __overtime: float = 0

    __goal_label = px.Label(
        None, "", 140, (WIN_WIDTH // 2, 180), "midtop", f="Comic Sans"
    )

    def reset():
        MatchStats.__state = "game"
        MatchStats.__overtime = 0

    def get_goal_label():
        return MatchStats.__goal_label

    def update_goal_label(team: Literal["Team Blue", "Team Orange"], player_name: str):
        MatchStats.__goal_label.update_colors(textcolor=TEAM_COLOR_MAP[team])
        MatchStats.__goal_label.update_text(f"{player_name} scored!")

    def reset_aftergoal_time():
        MatchStats.__aftergoal_time = AFTER_GOAL_SECONDS

    def get_aftergoal_time():
        return MatchStats.__aftergoal_time

    def reduce_aftergoal_time(dt: float):
        MatchStats.__aftergoal_time = max(MatchStats.__aftergoal_time - dt, 0)

    def set_state(state: str):
        assert state in ["game", "aftergoal", "overtime", "aftergoal_ot"]
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
        MatchStats.__last_shot_by = None
        MatchStats.__last_touches_dict = {
            "Team Blue": "Team Blue",
            "Team Orange": "Team Orange",
        }
        MatchStats.__last_touches_list.clear()
        MatchStats.__match_time_left = MATCH_DURATION_IN_SECONDS
        MatchStats.__player_team_map = {
            p: t
            for p, t in [
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

    def reduce_match_time(dt_s: float):
        MatchStats.__match_time_left = max(MatchStats.__match_time_left - dt_s, 0)

    def reduce_countdown(dt_s: float):
        MatchStats.__countdown = max(MatchStats.__countdown - dt_s, 0)
        if MatchStats.__countdown_last_integer == None or (
            MatchStats.__countdown_last_integer > int(MatchStats.__countdown)
        ):
            MatchStats.__countdown_last_integer = int(MatchStats.__countdown)
            Sounds.play("countdown")
        if MatchStats.__countdown == 0:
            Sounds.play("countdown_end")

    def increase_overtime(dt_s):
        MatchStats.__overtime += dt_s

    def get_overtime_seconds():
        return MatchStats.__overtime

    def get_countdown():
        return MatchStats.__countdown

    def start_countdown():
        MatchStats.__countdown = MATCH_COUNTDOWN
        MatchStats.__countdown_last_integer = None

    def get_player_stats() -> dict[str, PlayerStats]:
        return MatchStats.__player_stats

    def register_goal(team_name: str):
        assert team_name in ["Team Blue", "Team Orange"]

        if team_name == "Team Blue":
            MatchStats.__goals_team_blue += 1
            if MatchStats.__last_touches_dict["Team Blue"] != "Team Blue":
                MatchStats.__player_stats[
                    MatchStats.__last_touches_dict["Team Blue"]
                ].goals += 1

                # if there is a player of the blue team in the last three touches, award an assist
                for name in MatchStats.__last_touches_list[::-1]:
                    if (
                        name != MatchStats.__last_touches_dict["Team Blue"]
                        and MatchStats.__player_team_map[name] == "Team Blue"
                    ):
                        MatchStats.__player_stats[name].assists += 1
                        break
        elif team_name == "Team Orange":
            MatchStats.__goals_team_orange += 1
            if MatchStats.__last_touches_dict["Team Orange"] != "Team Orange":
                MatchStats.__player_stats[
                    MatchStats.__last_touches_dict["Team Orange"]
                ].goals += 1

                # if there is a player of the orangeteam in the last three touches, award an assist
                for name in MatchStats.__last_touches_list[::-1]:
                    if (
                        name != MatchStats.__last_touches_dict["Team Orange"]
                        and MatchStats.__player_team_map[name] == "Team Orange"
                    ):
                        MatchStats.__player_stats[name].assists += 1
                        break

        Sounds.play("goal")

    def reset_tracking_stats():
        MatchStats.__last_shot_by = None
        MatchStats.__last_touches_dict = {
            "Team Blue": "Team Blue",
            "Team Orange": "Team Orange",
        }
        MatchStats.__last_touches_list.clear()

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

        Sounds.play("ball_touch")

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
