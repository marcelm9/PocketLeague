import time

class MatchStats:

    __match_start_time: float
    __goals_team_0: int = 0
    __goals_team_1: int = 0

    def start_match():
        MatchStats.__match_start_time = time.time()

    def goal_team0():
        MatchStats.__goals_team_0 += 1

    def goal_team1():
        MatchStats.__goals_team_1 += 1

    def get_goals_team0():
        return MatchStats.__goals_team_0

    def get_goals_team1():
        return MatchStats.__goals_team_1
    
    def get_start_time():
        return MatchStats.__match_start_time

    def reset():
        MatchStats.__goals_team_0 = 0
        MatchStats.__goals_team_1 = 0
