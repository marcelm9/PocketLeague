from dataclasses import dataclass
from ..files.config import (
    POINTS_WEIGHT_TOUCH,
    POINTS_WEIGHT_GOAL,
    POINTS_WEIGHT_SHOT,
    POINTS_WEIGHT_SAVE,
    POINTS_WEIGHT_ASSIST,
)


@dataclass
class PlayerStats:
    touches: int = 0
    goals: int = 0
    shots: int = 0
    saves: int = 0
    assists: int = 0

    def get_points(self):
        return (
            self.touches * POINTS_WEIGHT_TOUCH
            + self.goals * POINTS_WEIGHT_GOAL
            + self.shots * POINTS_WEIGHT_SHOT
            + self.saves * POINTS_WEIGHT_SAVE
            + self.assists * POINTS_WEIGHT_ASSIST
        )
