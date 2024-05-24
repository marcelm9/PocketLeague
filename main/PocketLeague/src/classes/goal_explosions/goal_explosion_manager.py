import pygame

from ...files.config import TEAM_COLOR_MAP
from ..particle_manager import ParticleManager
from ..player_config_manager import PlayerConfigManager
from .dragons_goal_explosion import DragonGoalExplosion
from .regular_goal_explosion import RegularGoalExplosion


class GoalExplosionManager:

    __explosions: list[RegularGoalExplosion] = []

    def summon_goal_explosion(player_name, pos):
        player_config = PlayerConfigManager.get_by_name(player_name)
        match player_config.goal_explosion:
            case "regular":
                GoalExplosionManager.__explosions.append(
                    RegularGoalExplosion(
                        position=pos, color=TEAM_COLOR_MAP[player_config.team]
                    )
                )
            case "dragons":
                direction_factor = {"Team Blue": -1, "Team Orange": 1}[
                    player_config.team
                ]
                GoalExplosionManager.__explosions.append(
                    DragonGoalExplosion(position=pos, direction_factor=direction_factor)
                )
            case "red explosion":
                ParticleManager.create_explosion(pos, 250, 5, (255, 0, 0), 2.5, 7)
            case "green explosion":
                ParticleManager.create_explosion(pos, 250, 5, (0, 255, 0), 2.5, 7)

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
