import pygame
from ..files.config import CENTER, FIELD_WIDTH, FIELD_HEIGHT, GOAL_SIZE, GOAL_DEPTH, FIELD_CORNER_SMOOTHING
from .line import Line
from PygameXtras import C

class Field:

    lines: list[Line] = []

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
        
        # clockwise
        point_list = [
            C(rc.topleft) + C(FIELD_CORNER_SMOOTHING, 0),
            C(rc.topright) - C(FIELD_CORNER_SMOOTHING, 0),
            C(rc.topright) + C(0, FIELD_CORNER_SMOOTHING),
            C(rr.topleft),
            C(rr.topright),
            C(rr.bottomright),
            C(rr.bottomleft),
            C(rc.bottomright) - C(0, FIELD_CORNER_SMOOTHING),
            C(rc.bottomright) - C(FIELD_CORNER_SMOOTHING, 0),
            C(rc.bottomleft) + C(FIELD_CORNER_SMOOTHING, 0),
            C(rc.bottomleft) - C(0, FIELD_CORNER_SMOOTHING),
            C(rl.bottomright),
            C(rl.bottomleft),
            C(rl.topleft),
            C(rl.topright),
            C(rc.topleft) + C(0, FIELD_CORNER_SMOOTHING),
            C(rc.topleft) + C(FIELD_CORNER_SMOOTHING, 0),
        ]

        for i in range(len(point_list) - 1):
            start = point_list[i]
            end = point_list[i+1]

            vector = pygame.Vector2(
                end[0] - start[0],
                end[1] - start[1]
            )
            vector.rotate_ip(90)
            vector.scale_to_length(1)
            collisions = True
            if start[0] < rc.left or start[0] > rc.right or \
                start[1] < rc.top or start[1] > rc.bottom or \
                end[0] < rc.left or end[0] > rc.right or \
                end[1] < rc.top or end[1] > rc.bottom:                
                collisions = False
            Field.lines.append(
                Line(start, end, vector, collisions)
            )

    def get_lines():
        return Field.lines
