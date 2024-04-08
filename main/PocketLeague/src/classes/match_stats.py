class MatchStats:

    __goals_team_0: int = 0
    __goals_team_1: int = 0

    def goal_team0():
        MatchStats.__goals_team_0 += 1

    def goal_team1():
        MatchStats.__goals_team_1 += 1

    def get_goals_team0():
        return MatchStats.__goals_team_0

    def get_goals_team1():
        return MatchStats.__goals_team_1

    def reset():
        MatchStats.__goals_team_0 = 0
        MatchStats.__goals_team_1 = 0
