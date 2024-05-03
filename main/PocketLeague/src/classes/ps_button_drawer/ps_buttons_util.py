import pygame

from ...files.colors import SOFT_WHITE
from ...files.config import BUTTON_DRAWER_LINE_WIDTH, BUTTON_DRAWER_SIZE


def outline(surface, center):
    pygame.draw.circle(
        surface, SOFT_WHITE, center, BUTTON_DRAWER_SIZE, BUTTON_DRAWER_LINE_WIDTH
    )

def draw_lines(surface, center, offset_points):
    for i in range(len(offset_points)):
        pygame.draw.line(
            surface,
            SOFT_WHITE,
            (
                center[0] + offset_points[i][0],
                center[1] + offset_points[i][1],
            ),
            (
                center[0] + offset_points[i - 1][0],
                center[1] + offset_points[i - 1][1],
            ),
            BUTTON_DRAWER_LINE_WIDTH
        )

def left():
    points = []

    angle = 110

    v = pygame.Vector2(-1, 0)
    v.scale_to_length(BUTTON_DRAWER_SIZE * 0.4)
    points.append((v.x, v.y))

    v.scale_to_length(BUTTON_DRAWER_SIZE * 0.55)
    v.rotate_ip(angle)
    points.append((v.x, v.y))

    v.rotate_ip((180 - angle) * 2)
    points.append((v.x, v.y))

    return points

def up():
    points = []

    angle = 110

    v = pygame.Vector2(0, -1)
    v.scale_to_length(BUTTON_DRAWER_SIZE * 0.4)
    points.append((v.x, v.y))

    v.scale_to_length(BUTTON_DRAWER_SIZE * 0.55)
    v.rotate_ip(angle)
    points.append((v.x, v.y))

    v.rotate_ip((180 - angle) * 2)
    points.append((v.x, v.y))

    return points

def square():
    points = []

    v = pygame.Vector2(1, 1)
    v.scale_to_length(BUTTON_DRAWER_SIZE * 0.6)
    for _ in range(4):
        v.rotate_ip(90)
        points.append((v.x, v.y))
    
    return points

def triangle():
    points = []

    v = pygame.Vector2(0, -1)
    v.scale_to_length(BUTTON_DRAWER_SIZE * 0.6)
    points.append((v.x, v.y))

    v.rotate_ip(120)
    points.append((v.x, v.y))

    v.rotate_ip(120)
    points.append((v.x, v.y))

    return points

def slash():
    points = []

    v = pygame.Vector2(0, -1)
    v.scale_to_length(BUTTON_DRAWER_SIZE * 1.2)
    v.rotate_ip(25)
    points.append((v.x, v.y))
    v.rotate_ip(180)
    points.append((v.x, v.y))

    return points
