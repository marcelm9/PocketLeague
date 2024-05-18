import pygame
import pymunk
from ..files.config import CENTER, FIELD_WIDTH, FIELD_HEIGHT, GOAL_SIZE, GOAL_DEPTH, FIELD_CORNER_SMOOTHING, FIELD_LINE_SIZE, TEAM_COLOR_MAP
from .line import Line
from PygameXtras import C
from .space import Space

class Field:

    lines: list[Line] = []
    goals: list[Line] = []

    __rl: pygame.Rect # rect left
    __rc: pygame.Rect # rect center
    __rr: pygame.Rect # rect right

    def init():
        rect_center = pygame.Rect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        rect_center.center = CENTER
        rect_left = pygame.Rect(0, 0, GOAL_DEPTH, GOAL_SIZE)
        rect_left.midright = rect_center.midleft
        rect_right = pygame.Rect(0, 0, GOAL_DEPTH, GOAL_SIZE)
        rect_right.midleft = rect_center.midright

        rc = rect_center
        rl = rect_left
        rr = rect_right

        Field.__rc = rc
        Field.__rl = rl
        Field.__rr = rr

        center_ditch = 0

        
        # clockwise
        point_list = [
            C(rc.topleft) + C(FIELD_CORNER_SMOOTHING, 0),
            C(CENTER[0], rc.top + center_ditch),
            C(rc.topright) - C(FIELD_CORNER_SMOOTHING, 0),
            C(rc.topright) + C(0, FIELD_CORNER_SMOOTHING),
            C(rr.topleft),
            C(rr.topright),
            C(rr.bottomright),
            C(rr.bottomleft),
            C(rc.bottomright) - C(0, FIELD_CORNER_SMOOTHING),
            C(rc.bottomright) - C(FIELD_CORNER_SMOOTHING, 0),
            C(CENTER[0], rc.bottom - center_ditch),
            C(rc.bottomleft) + C(FIELD_CORNER_SMOOTHING, 0),
            C(rc.bottomleft) - C(0, FIELD_CORNER_SMOOTHING),
            C(rl.bottomright),
            C(rl.bottomleft),
            C(rl.topleft),
            C(rl.topright),
            C(rc.topleft) + C(0, FIELD_CORNER_SMOOTHING),
            C(rc.topleft) + C(FIELD_CORNER_SMOOTHING, 0),
        ]

        wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        wall.position = (0, 0)

        wall_shapes = []

        for i in range(len(point_list) - 1):

            start = point_list[i]
            end = point_list[i+1]

            # for ball collision
            shape = pymunk.Segment(wall, tuple(start), tuple(end), FIELD_LINE_SIZE)
            shape.elasticity = 1
            wall_shapes.append(shape)

            # for player collision
            vector = pygame.Vector2(
                end[0] - start[0],
                end[1] - start[1]
            )
            vector.rotate_ip(90)
            vector.scale_to_length(1)
            goal_line = False
            if start[0] < rc.left or end[0] < rc.left:
                collisions = False
                color = TEAM_COLOR_MAP["Team Blue"]
                goal_line = True
            elif start[0] > rc.right or end[0] > rc.right:
                collisions = False
                color = TEAM_COLOR_MAP["Team Orange"]
                goal_line = True
            else:
                collisions = True
                color = (255,255,255)
            if goal_line:
                Field.goals.append(
                    Line(start, end, vector, collisions, color)
                )
            else:
                Field.lines.append(
                    Line(start, end, vector, collisions, color)
                )

        Space.space.add(wall, *wall_shapes)

    def get_lines():
        return Field.lines
    
    def get_goal_lines():
        return Field.goals

    def get_blue_goal_line():
        return (Field.__rl.topright, Field.__rl.bottomright)

    def get_orange_goal_line():
        return (Field.__rr.topleft, Field.__rr.bottomleft)

    def get_blue_goal_center():
        return Field.__rl.midright

    def get_orange_goal_center():
        return Field.__rr.midleft
