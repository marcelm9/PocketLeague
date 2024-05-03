from dataclasses import dataclass

@dataclass
class PlayerConfig:
    name: str
    team: str
    color: str
    boost: str
    goal_explosion: str

    controller_id: int
    controller_side: str
