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
    def get_by_name(name: str):
        player = [p for p in PlayerConfigManager.__players if p.name == name]
        if len(player) > 1:
            raise Exception(f"multiple players with name {name}")
        elif len(player) == 0:
            raise Exception(f"no player with name {name} found")
        return player[0]

    @staticmethod
    def get_by_controller(controller_index: int, controller_side: str):
        for p in PlayerConfigManager.__players:
            if (
                p.controller_id == controller_index
                and p.controller_side == controller_side
            ):
                return p
        return None

    @staticmethod
    def get_errors():
        errors = []
        len_of_blue_team = len(
            [p for p in PlayerConfigManager.__players if p.team == "Team Blue"]
        )
        len_of_orange_team = len(
            [p for p in PlayerConfigManager.__players if p.team == "Team Orange"]
        )
        nonunique_players = [
            p1.name
            for p1 in PlayerConfigManager.__players
            for p2 in PlayerConfigManager.__players
            if p1 != p2 and p1.name == p2.name
        ]
        identical_players = [
            p1.name
            for p1 in PlayerConfigManager.__players
            for p2 in PlayerConfigManager.__players
            if p1 != p2 and p1.color == p2.color and p1.team == p2.team
        ]
        if len(PlayerConfigManager.__players) < 2:
            errors.append("Not enough players")
        elif len_of_blue_team == 0:
            errors.append("Blue Team has no players")
        elif len_of_orange_team == 0:
            errors.append("Orange Team has no players")
        if len(nonunique_players) > 0:
            errors.append(f"Nonunique player names: {', '.join(list(set(nonunique_players)))}")
        if len(identical_players) > 0:
            errors.append(f"Identical players: {', '.join(identical_players)}")
        return errors

    def _use_debug_configs():
        PlayerConfigManager.__players = [
            PlayerConfig("Marcel", "Team Blue", "red", "red", "regular", 0, "left"),
            PlayerConfig(
                "Pascal", "Team Orange", "azure", "yellow", "dragons", 0, "right"
            ),
        ]
        print("Using debug player configs")

    def _inject_test(players):
        for p in players:
            PlayerConfigManager.__players.append(
                PlayerConfig(p[0], p[1], None, None, None, None, None)
            )
