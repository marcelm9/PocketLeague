import pygame

from .goal_explosion import GoalExplosion


class GoalExplosionManager:

    __explosions: list[GoalExplosion] = []

    def summon_goal_explosion(pos, color):
        GoalExplosionManager.__explosions.append(
            GoalExplosion(
                color=color, thickness=10, radius=700, duration=1.2, position=pos
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
            expl.render(surface)
