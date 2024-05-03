from .player_config import PlayerConfig


class PlayerConfigManager:

    __players: list[PlayerConfig] = []

    def add_player(player_config):
        assert isinstance(player_config, PlayerConfig)
        PlayerConfigManager.__players.append(player_config)

    def clear_players():
        PlayerConfigManager.__players.clear()

    def get_player_configs():
        return PlayerConfigManager.__players
