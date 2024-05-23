import random
from ..files.config import PLAYER_SPAWNS, CENTER
from .player import Player


class PlayerManager:

    __players: list[Player] = []

    @staticmethod
    def summon_player(
        name: str,
        team: str,
        color: str,
        boost_type: str,
        goal_explosion: str,
        controller_index: int,
        controller_side: str,
    ):
        p = Player()
        p.set_name(name)
        p.set_team(team)
        p.set_color(color)
        p.set_boost_type(boost_type)
        p.set_goal_explosion(goal_explosion)
        p.set_controller_input(
            controller_index, *({"left": (0, 9), "right": (1, 10)}[controller_side])
        )

        PlayerManager.__players.append(p)

    @staticmethod
    def respawn_players():
        # respawns players and resets their boosts

        spawns = list(PLAYER_SPAWNS[:])
        random.shuffle(spawns)
        blue_i = 0
        orange_i = 0
        for p in PlayerManager.__players:
            p.reset_boost()
            if p.get_team() == "Team Blue":
                p.set_pos((
                    CENTER[0] + spawns[blue_i][0],
                    CENTER[1] + spawns[blue_i][1],
                ))
                blue_i += 1
            else:
                p.set_pos((
                    CENTER[0] + spawns[orange_i][0] * -1,
                    CENTER[1] + spawns[orange_i][1] * -1,
                ))
                orange_i += 1

    @staticmethod
    def reset():
        PlayerManager.__players.clear()

    @staticmethod
    def get_players():
        return PlayerManager.__players

    @staticmethod
    def update(dt_s):
        for player in PlayerManager.__players:
            player.update(dt_s, PlayerManager.__players)

    @staticmethod
    def draw(surface):
        for player in PlayerManager.__players:
            player.draw(surface)

    @staticmethod
    def keep_in_bounds():
        for player in PlayerManager.__players:
            player.keep_in_bounds()
