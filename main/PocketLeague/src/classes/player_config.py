from dataclasses import dataclass

@dataclass
class PlayerConfig:
    name: str
    team: str # TODO: improve by using enum
    color: str
    boost: str
    goal_explosion: str

    controller_id: int
    controller_side: str
