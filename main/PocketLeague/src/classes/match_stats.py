from .player_manager import PlayerManager
from .player_stats import PlayerStats
from ..files.config import MATCH_COUNTDOWN, MATCH_DURATION_IN_SECONDS


class MatchStats:

    __match_time_left: float
    __countdown: float = 0
    __goals_team_0: int = 0
    __goals_team_1: int = 0
    __player_stats: dict[str, PlayerStats] = {}

    def _finish_game():
        MatchStats.__match_time_left = 1

    def start_match():
        MatchStats.__match_time_left = MATCH_DURATION_IN_SECONDS
        MatchStats.start_countdown()
        MatchStats.__player_stats.clear()
        for player in PlayerManager.get_players():
            MatchStats.__player_stats[player.get_name()] = PlayerStats()

    def goal_team0():
        MatchStats.__goals_team_0 += 1

    def goal_team1():
        MatchStats.__goals_team_1 += 1

    def get_goals_team0():
        return MatchStats.__goals_team_0

    def get_goals_team1():
        return MatchStats.__goals_team_1

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
        MatchStats.__goals_team_0 = 0
        MatchStats.__goals_team_1 = 0

    def get_player_stats() -> dict[str, PlayerStats]:
        return MatchStats.__player_stats

    def register_touch(player_name: str):
        MatchStats.__player_stats[player_name].touches += 1

    def register_goal(player_name: str):
        MatchStats.__player_stats[player_name].goals += 1

    def register_shot(player_name: str):
        MatchStats.__player_stats[player_name].shots += 1

    def register_save(player_name: str):
        MatchStats.__player_stats[player_name].saves += 1

    def register_layup(player_name: str):
        MatchStats.__player_stats[player_name].layups += 1
