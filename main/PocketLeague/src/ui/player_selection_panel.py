import pygame
import PygameXtras as px

from ..files.config import HUD_FONT, PLAYER_SELECTION_PANEL_SIZE

from ..classes.controller_manager import ControllerManager

from ..files.colors import SOFT_WHITE

class PlayerSelectionPanel:
    def __init__(self, center, controller_index, controller_input_side: str):
        assert controller_index in [0, 1]
        assert controller_input_side in ["left", "right"]

        self.__controller_index = controller_index
        self.__controller_input_side = controller_input_side

        self.__rect = pygame.Rect(0,0,*PLAYER_SELECTION_PANEL_SIZE)
        self.__rect.center = center


        self.__no_player_label = px.Label(
            None,
            "No player",
            40,
            center,
            tc=SOFT_WHITE,
            f="Comic Sans"
        )

        self.__active = False

        # lets also show the player how they would look like in game (as first thing of the panel, above the name)
        labels = ("Name", "Team", "Color", "Boost Color", "Goal Explosion")
        defaults = ("Marcel", "Team Blue", "Green", "Yellow", "Default")

        self.__labels = [
            px.Label(
                None,
                item,
                40,
                self.__offset((PLAYER_SELECTION_PANEL_SIZE[0] // 2, 200 + 110 * i)),
                tc=SOFT_WHITE,
                f="Comic Sans"
            ) for i, item in enumerate(labels)
        ]

    def __offset(self, pos):
        return (
            self.__rect[0] + pos[0],
            self.__rect[1] + pos[1]
        )

    def update(self):
        keys = ControllerManager.get_pressed_by(self.__controller_index, self.__controller_input_side)
        if not self.__active:
            if keys[0]:
                self.__active = True

    def draw(self, surface):
        if self.__active:
            for label in self.__labels:
                label.draw_to(surface)
        else:
            self.__no_player_label.draw_to(surface)
        pygame.draw.rect(surface, SOFT_WHITE, self.__rect, 5, 30)
        
