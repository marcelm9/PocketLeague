from ..files.config import MATCH_COUNTDOWN, MATCH_DURATION_IN_SECONDS

class MatchStats:

    __match_time_left: float
    __countdown: float = 0
    __goals_team_0: int = 0
    __goals_team_1: int = 0

    def start_match():
        MatchStats.__match_time_left = MATCH_DURATION_IN_SECONDS
        MatchStats.start_countdown()

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
        MatchStats.__match_time_left -= dt

    def reduce_countdown(dt: float):
        MatchStats.__countdown = max(MatchStats.__countdown - dt, 0)

    def get_countdown():
        return MatchStats.__countdown
    
    def start_countdown():
        MatchStats.__countdown = MATCH_COUNTDOWN

    def reset():
        MatchStats.__goals_team_0 = 0
        MatchStats.__goals_team_1 = 0
