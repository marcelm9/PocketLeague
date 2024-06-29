from .boost_pad import BoostPad
from .field import Field


class BoostPadsManager:

    __pads: list[BoostPad] = []

    def init():
        for pos in Field.get_boostpads():
            BoostPadsManager.__pads.append(BoostPad(pos))

    def reset():
        BoostPadsManager.__pads.clear()

    def reset_pads():
        for pad in BoostPadsManager.__pads:
            pad.reset()

    def update(dt_s):
        for pad in BoostPadsManager.__pads:
            pad.update(dt_s)

    def draw(surface):
        for pad in BoostPadsManager.__pads:
            pad.draw(surface)
