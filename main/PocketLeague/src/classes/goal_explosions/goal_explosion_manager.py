import pygame

from .dragons_goal_explosion import DragonGoalExplosion

from ...files.config import TEAM_COLOR_MAP

from ..player_config_manager import PlayerConfigManager

from .regular_goal_explosion import RegularGoalExplosion


class GoalExplosionManager:

    __explosions: list[RegularGoalExplosion] = []

    def summon_goal_explosion(player_name, pos):
        player_config = PlayerConfigManager.get_by_name(player_name)
        if player_config.goal_explosion == "regular":
            GoalExplosionManager.__explosions.append(
                RegularGoalExplosion(
                    color=TEAM_COLOR_MAP[player_config.team], thickness=10, radius=700, duration=1.2, position=pos
                )
            )
        elif player_config.goal_explosion == "dragons":
            direction_factor = {"Team Blue": -1, "Team Orange": 1}[player_config.team]
            GoalExplosionManager.__explosions.append(
                DragonGoalExplosion(
                    position=pos, direction_factor=direction_factor, duration=1.5, distance=600
                )
            )

    def update(dt_s):
        GoalExplosionManager.__explosions = [
            g for g in GoalExplosionManager.__explosions if not g.is_over()
        ]
        for expl in GoalExplosionManager.__explosions:
            expl.update(dt_s)

    def draw(surface: pygame.Surface):
        for expl in GoalExplosionManager.__explosions:
            expl.draw(surface)

    def reset():
        GoalExplosionManager.__explosions.clear()
