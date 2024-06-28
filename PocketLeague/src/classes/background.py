import math

import pygame

from ..files.config import CENTER, DISTANCE_FROM_GOAL_FOR_SHOT, WIN_HEIGHT, WIN_WIDTH
from .field import Field


class Background:

    __goal_blue = pygame.Rect(
        0, 0, DISTANCE_FROM_GOAL_FOR_SHOT * 2, DISTANCE_FROM_GOAL_FOR_SHOT * 2
    )
    __goal_blue.center = Field.get_blue_goal_center()
    __goal_orange = pygame.Rect(
        0, 0, DISTANCE_FROM_GOAL_FOR_SHOT * 2, DISTANCE_FROM_GOAL_FOR_SHOT * 2
    )
    __goal_orange.center = Field.get_orange_goal_center()

    __boost_pad_top = pygame.Rect(0, 0, 200, 200)
    __boost_pad_top.center = Field.rect_center.midtop
    __boost_pad_bottom = pygame.Rect(0, 0, 200, 200)
    __boost_pad_bottom.center = Field.rect_center.midbottom

    @staticmethod
    def draw(surface: pygame.Surface):

        # draw circles around center
        pygame.draw.circle(surface, (255, 255, 255), CENTER, 110, 1)
        pygame.draw.circle(surface, (255, 255, 255), CENTER, 140, 1)

        # draw lines for "shot" radius
        pygame.draw.arc(
            surface,
            (255, 255, 255),
            Background.__goal_blue,
            math.radians(277),
            math.radians(83),
        )
        pygame.draw.arc(
            surface,
            (255, 255, 255),
            Background.__goal_orange,
            math.radians(97),
            math.radians(263),
        )

        # draw lines around top and bottom center boost pad
        pygame.draw.arc(
            surface,
            (255, 255, 255),
            Background.__boost_pad_top,
            math.radians(180),
            math.radians(0),
        )
        pygame.draw.arc(
            surface,
            (255, 255, 255),
            Background.__boost_pad_bottom,
            math.radians(0),
            math.radians(180),
        )

        # draw horizontal lines from center to "shot" lines
        pygame.draw.line(
            surface,
            (255, 255, 255),
            Background.__goal_blue.midright,
            (CENTER[0] - 140, CENTER[1]),
        )
        pygame.draw.line(
            surface,
            (255, 255, 255),
            (CENTER[0] + 140, CENTER[1]),
            Background.__goal_orange.midleft,
        )

        # draw vertical lines from center to boost pads
        pygame.draw.line(
            surface,
            (255, 255, 255),
            (Field.rect_center.midtop[0], Field.rect_center.midtop[1] + 100),
            (CENTER[0], CENTER[1] - 140),
        )
        pygame.draw.line(
            surface,
            (255, 255, 255),
            (CENTER[0], CENTER[1] + 140),
            (Field.rect_center.midbottom[0], Field.rect_center.midbottom[1] - 100),
        )
