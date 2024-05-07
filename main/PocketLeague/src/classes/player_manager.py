from .enums import *
from .player import Player


class PlayerManager:

    __players: list[Player] = []

    @staticmethod
    def summon_player(
        name: str,
        team: str,
        color: str,
        boost: str,
        goal_explosion: str
    ):
        pass

    @staticmethod
    def respawn_players():
        # respawns players and resets their boosts
        pass

    @staticmethod
    def clear_players():
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
