from .player_config import PlayerConfig


class PlayerConfigManager:

    __players: list[PlayerConfig] = []

    @staticmethod
    def add_player(player_config):
        assert isinstance(player_config, PlayerConfig)
        PlayerConfigManager.__players.append(player_config)

    @staticmethod
    def clear_players():
        PlayerConfigManager.__players.clear()

    @staticmethod
    def get_player_configs():
        return PlayerConfigManager.__players

    @staticmethod    
    def get_by_controller(controller_index: int, controller_side: str):
        for p in PlayerConfigManager.__players:
            if p.controller_id == controller_index and p.controller_side == controller_side:
                return p
        return None

    def _use_debug_configs():
        PlayerConfigManager.__players = [
            PlayerConfig(
                "Marcel",
                "Team Blue",
                "red",
                "regular",
                "regular",
                0,
                "left"
            ),
            PlayerConfig(
                "Pascal",
                "Team Orange",
                "azure",
                "regular",
                "regular",
                0,
                "right"
            )
        ]
        print("Using debug player configs")
