from .boost_pad import BoostPad
from ..files.config import BOOST_SPAWNS

class BoostPadsManager:

    __pads: list[BoostPad] = []

    def init():
        for pos in BOOST_SPAWNS:
            BoostPadsManager.__pads.append(BoostPad(pos))

    def reset_pads():
        for pad in BoostPadsManager.__pads:
            pad.reset()

    def update():
        for pad in BoostPadsManager.__pads:
            pad.update()

    def draw(surface):
        for pad in BoostPadsManager.__pads:
            pad.draw(surface)
