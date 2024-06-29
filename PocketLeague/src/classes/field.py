import math

import pygame
import pymunk
from PygameXtras import C

from ..files.config import (
    CENTER,
    DISTANCE_FROM_GOAL_FOR_SHOT,
    FIELD_CORNER_SMOOTHING,
    FIELD_HEIGHT,
    FIELD_LINE_SIZE,
    FIELD_WIDTH,
    GOAL_DEPTH,
    GOAL_SIZE,
    TEAM_COLOR_MAP,
    WIN_HEIGHT,
    WIN_WIDTH,
)
from .line import Line
from .space import Space


class Field:

    lines: list[Line] = []
    goal_lines: list[Line] = []  # goal lines should be drawn on top of regular lines

    blue_goal: tuple  # (topleft, bottomright)
    orange_goal: tuple  # (topleft, bottomright)

    __map_image = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    __boostpads = []

    __rc = pygame.Rect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
    __rc.center = CENTER
    __rl = pygame.Rect(0, 0, GOAL_DEPTH, GOAL_SIZE)
    __rl.midright = __rc.midleft
    __rr = pygame.Rect(0, 0, GOAL_DEPTH, GOAL_SIZE)
    __rr.midleft = __rc.midright

    def init(map_name: str):
        Field.reset()

        wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        wall.position = (0, 0)
        wall_shapes = []

        rc = Field.__rc
        rl = Field.__rl
        rr = Field.__rr

        # always add points clockwise so that the normal vector points inwards
        # each point should only be contained ONCE (first != last)
        # also set Field.blue_goal and Field.orange_goal
        if map_name == "Regular":

            Field.blue_goal = (
                rl.topleft,
                rl.bottomright,
            )
            Field.orange_goal = (
                rr.topleft,
                rr.bottomright,
            )

            point_list = [
                (C(rc.topleft) + C(FIELD_CORNER_SMOOTHING, 0), "field"),
                (C(rc.topright) - C(FIELD_CORNER_SMOOTHING, 0), "field"),
                (C(rc.topright) + C(0, FIELD_CORNER_SMOOTHING), "field"),
                (C(rr.topleft), "orange"),
                (C(rr.topright), "orange"),
                (C(rr.bottomright), "orange"),
                (C(rr.bottomleft), "orange"),
                (C(rc.bottomright) - C(0, FIELD_CORNER_SMOOTHING), "field"),
                (C(rc.bottomright) - C(FIELD_CORNER_SMOOTHING, 0), "field"),
                (C(rc.bottomleft) + C(FIELD_CORNER_SMOOTHING, 0), "field"),
                (C(rc.bottomleft) - C(0, FIELD_CORNER_SMOOTHING), "field"),
                (C(rl.bottomright), "blue"),
                (C(rl.bottomleft), "blue"),
                (C(rl.topleft), "blue"),
                (C(rl.topright), "blue"),
                (C(rc.topleft) + C(0, FIELD_CORNER_SMOOTHING), "field"),
            ]

        elif map_name == "Diagonal":

            Field.blue_goal = (
                (rc.left - GOAL_DEPTH, rc.top),
                (rc.left, rc.top + GOAL_SIZE),
            )

            Field.orange_goal = (
                (rc.right, rc.bottom - GOAL_SIZE),
                (rc.right + GOAL_DEPTH, rc.bottom),
            )

            point_list = [
                (rc.topleft, "blue"),
                ((rc.right - FIELD_CORNER_SMOOTHING, rc.top), "field"),
                ((rc.right, rc.top + FIELD_CORNER_SMOOTHING), "field"),
                ((rc.right, rc.bottom - GOAL_SIZE), "orange"),
                ((rc.right + GOAL_DEPTH, rc.bottom - GOAL_SIZE), "orange"),
                ((rc.right + GOAL_DEPTH, rc.bottom), "orange"),
                (rc.bottomright, "orange"),
                ((rc.left + FIELD_CORNER_SMOOTHING, rc.bottom), "field"),
                ((rc.left, rc.bottom - FIELD_CORNER_SMOOTHING), "field"),
                ((rc.left, rc.top + GOAL_SIZE), "blue"),
                ((rc.left - GOAL_DEPTH, rc.top + GOAL_SIZE), "blue"),
                ((rc.left - GOAL_DEPTH, rc.top), "blue"),
            ]

        # creating background image
        Field.__set_map_image(map_name)
        Field.__set_map_boostpads(map_name)

        # creating lines
        for i in range(len(point_list)):

            p1_pos, p1_type = point_list[i]
            p2_pos, p2_type = point_list[(i + 1) % len(point_list)]

            # for ball collision
            shape = pymunk.Segment(wall, tuple(p1_pos), tuple(p2_pos), FIELD_LINE_SIZE)
            shape.elasticity = 1
            shape.filter = pymunk.ShapeFilter(mask=0b1)
            wall_shapes.append(shape)

            # for player collision
            vector = pygame.Vector2(p2_pos[0] - p1_pos[0], p2_pos[1] - p1_pos[1])
            vector.rotate_ip(90)
            vector.scale_to_length(1)

            if p1_type == "blue" and p2_type == "blue":
                color = TEAM_COLOR_MAP["Team Blue"]
                goal_line = True
            elif p1_type == "orange" and p2_type == "orange":
                color = TEAM_COLOR_MAP["Team Orange"]
                goal_line = True
            else:
                # field
                color = (255, 255, 255)
                goal_line = False

            if goal_line:
                Field.goal_lines.append(Line(p1_pos, p2_pos, vector, color))
            else:
                Field.lines.append(Line(p1_pos, p2_pos, vector, color))

        Space.space.add(wall, *wall_shapes)

    def is_in_blue_goal(circle_pos, circle_radius):
        return (
            (circle_pos[0] - circle_radius >= Field.blue_goal[0][0])
            and (circle_pos[0] + circle_radius <= Field.blue_goal[1][0])
            and (circle_pos[1] - circle_radius >= Field.blue_goal[0][1])
            and (circle_pos[1] + circle_radius <= Field.blue_goal[1][1])
        )

    def is_in_orange_goal(circle_pos, circle_radius):
        return (
            (circle_pos[0] - circle_radius >= Field.orange_goal[0][0])
            and (circle_pos[0] + circle_radius <= Field.orange_goal[1][0])
            and (circle_pos[1] - circle_radius >= Field.orange_goal[0][1])
            and (circle_pos[1] + circle_radius <= Field.orange_goal[1][1])
        )

    def get_lines():
        return Field.lines

    def get_goal_lines():
        return Field.goal_lines

    def get_blue_goal_line():
        """rightmost line of blue goal rect"""
        return ((Field.blue_goal[1][0], Field.blue_goal[0][1]), Field.blue_goal[1])

    def get_orange_goal_line():
        """leftmost line of orange goal rect"""
        return (
            Field.orange_goal[0],
            (Field.orange_goal[0][0], Field.orange_goal[1][1]),
        )

    def get_center_of_blue_goal_line():
        return (
            Field.blue_goal[1][0],
            Field.blue_goal[0][1] + (Field.blue_goal[1][1] - Field.blue_goal[0][1]) / 2,
        )

    def get_center_of_orange_goal_line():
        return (
            Field.orange_goal[0][0],
            Field.orange_goal[0][1]
            + (Field.orange_goal[1][1] - Field.orange_goal[0][1]) / 2,
        )

    def reset():
        Field.lines.clear()
        Field.goal_lines.clear()
        Field.__map_image.fill((0, 0, 0))

    def __set_map_image(map_name: str):
        """sets Field.__map_image"""

        surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))

        if map_name == "Regular":
            __goal_blue = pygame.Rect(
                0, 0, DISTANCE_FROM_GOAL_FOR_SHOT * 2, DISTANCE_FROM_GOAL_FOR_SHOT * 2
            )
            __goal_blue.center = Field.get_center_of_blue_goal_line()
            __goal_orange = pygame.Rect(
                0, 0, DISTANCE_FROM_GOAL_FOR_SHOT * 2, DISTANCE_FROM_GOAL_FOR_SHOT * 2
            )
            __goal_orange.center = Field.get_center_of_orange_goal_line()

            __boost_pad_top = pygame.Rect(0, 0, 200, 200)
            __boost_pad_top.center = Field.__rc.midtop
            __boost_pad_bottom = pygame.Rect(0, 0, 200, 200)
            __boost_pad_bottom.center = Field.__rc.midbottom

            # draw circles around center
            pygame.draw.circle(surface, (255, 255, 255), CENTER, 110, 1)
            pygame.draw.circle(surface, (255, 255, 255), CENTER, 140, 1)

            # draw lines for "shot" radius
            pygame.draw.arc(
                surface,
                (255, 255, 255),
                __goal_blue,
                math.radians(277),
                math.radians(83),
            )
            pygame.draw.arc(
                surface,
                (255, 255, 255),
                __goal_orange,
                math.radians(97),
                math.radians(263),
            )

            # draw lines around top and bottom center boost pad
            pygame.draw.arc(
                surface,
                (255, 255, 255),
                __boost_pad_top,
                math.radians(180),
                math.radians(0),
            )
            pygame.draw.arc(
                surface,
                (255, 255, 255),
                __boost_pad_bottom,
                math.radians(0),
                math.radians(180),
            )

            # draw horizontal lines from center to "shot" lines
            pygame.draw.line(
                surface,
                (255, 255, 255),
                __goal_blue.midright,
                (CENTER[0] - 140, CENTER[1]),
            )
            pygame.draw.line(
                surface,
                (255, 255, 255),
                (CENTER[0] + 140, CENTER[1]),
                __goal_orange.midleft,
            )

            # draw vertical lines from center to boost pads
            pygame.draw.line(
                surface,
                (255, 255, 255),
                (Field.__rc.midtop[0], Field.__rc.midtop[1] + 100),
                (CENTER[0], CENTER[1] - 140),
            )
            pygame.draw.line(
                surface,
                (255, 255, 255),
                (CENTER[0], CENTER[1] + 140),
                (Field.__rc.midbottom[0], Field.__rc.midbottom[1] - 100),
            )

        elif map_name == "Diagonal":

            # goal to goal lines
            pygame.draw.line(
                surface,
                (255, 255, 255),
                (Field.blue_goal[1][0], Field.blue_goal[0][1]),
                Field.orange_goal[0],
            )
            pygame.draw.line(
                surface,
                (255, 255, 255),
                Field.blue_goal[1],
                (Field.orange_goal[0][0], Field.orange_goal[1][1]),
            )

            # center
            pygame.draw.circle(surface, (0, 0, 0), CENTER, 140)
            pygame.draw.circle(surface, (255, 255, 255), CENTER, 110, 1)
            pygame.draw.circle(surface, (255, 255, 255), CENTER, 140, 1)

            # shot_distance lines
            __goal_blue = pygame.Rect(
                0, 0, DISTANCE_FROM_GOAL_FOR_SHOT * 2, DISTANCE_FROM_GOAL_FOR_SHOT * 2
            )
            __goal_blue.center = Field.get_center_of_blue_goal_line()
            pygame.draw.circle(
                surface,
                (0, 0, 0),
                __goal_blue.center,
                DISTANCE_FROM_GOAL_FOR_SHOT,
            )
            pygame.draw.arc(
                surface,
                (255, 255, 255),
                __goal_blue,
                math.radians(270),
                math.radians(13),
            )
            __goal_orange = pygame.Rect(
                0, 0, DISTANCE_FROM_GOAL_FOR_SHOT * 2, DISTANCE_FROM_GOAL_FOR_SHOT * 2
            )
            __goal_orange.center = Field.get_center_of_orange_goal_line()
            pygame.draw.circle(
                surface,
                (0, 0, 0),
                __goal_orange.center,
                DISTANCE_FROM_GOAL_FOR_SHOT,
            )
            pygame.draw.arc(
                surface,
                (255, 255, 255),
                __goal_orange,
                math.radians(90),
                math.radians(193),
            )

        Field.__map_image = surface

    def __set_map_boostpads(map_name: str):
        spawns: list[tuple[int, int]] = []

        if map_name == "Regular":
            fw = 0.9
            fh1 = 0.83
            fh2 = 0.9
            spawns = (
                (
                    CENTER[0] - (FIELD_WIDTH // 2) * fw,
                    CENTER[1] - (FIELD_HEIGHT // 2) * fh1,
                ),
                (CENTER[0], CENTER[1] - (FIELD_HEIGHT // 2) * fh2),
                (
                    CENTER[0] + (FIELD_WIDTH // 2) * fw,
                    CENTER[1] - (FIELD_HEIGHT // 2) * fh1,
                ),
                (
                    CENTER[0] + (FIELD_WIDTH // 2) * fw,
                    CENTER[1] + (FIELD_HEIGHT // 2) * fh1,
                ),
                (CENTER[0], CENTER[1] + (FIELD_HEIGHT // 2) * fh2),
                (
                    CENTER[0] - (FIELD_WIDTH // 2) * fw,
                    CENTER[1] + (FIELD_HEIGHT // 2) * fh1,
                ),
            )

        elif map_name == "Diagonal":
            d = 60
            f = 2
            spawns = (
                (CENTER[0] - d * f, CENTER[1] - (FIELD_HEIGHT // 2) + d),  # midtop
                (CENTER[0] + d * f, CENTER[1] + (FIELD_HEIGHT // 2) - d),  # midbottom
                (CENTER[0] - (FIELD_WIDTH // 2) + d, CENTER[1] - d * f),  # midleft
                (CENTER[0] + (FIELD_WIDTH // 2) - d, CENTER[1] + d * f),  # midright
                (
                    CENTER[0] - (FIELD_WIDTH // 2) + d,
                    CENTER[1] + (FIELD_HEIGHT // 2) - d,
                ),  # bottomleft
                (
                    CENTER[0] + (FIELD_WIDTH // 2) - d,
                    CENTER[1] - (FIELD_HEIGHT // 2) + d,
                ),  # topright
            )

        Field.__boostpads = spawns

    def draw(surface: pygame.Surface):
        surface.blit(Field.__map_image, (0, 0))

    def get_boostpads() -> list[tuple[int, int]]:
        return Field.__boostpads
