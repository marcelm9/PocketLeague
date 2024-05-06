import pygame

from ...files.colors import SOFT_WHITE
from ...files.config import BUTTON_DRAWER_LINE_WIDTH, BUTTON_DRAWER_SIZE
from .ps_buttons_util import *


class PSButtonDrawer:

    __left = left()
    __square = square()
    __up = up()
    __triangle = triangle()
    __slash = slash()

    @staticmethod
    def left(surface, center):
        outline(surface, center)
        draw_lines(surface, center, PSButtonDrawer.__left)

    @staticmethod
    def square(surface, center):
        outline(surface, center)
        draw_lines(surface, center, PSButtonDrawer.__square)

    @staticmethod
    def up(surface, center):
        outline(surface, center)
        draw_lines(surface, center, PSButtonDrawer.__up)

    @staticmethod
    def triangle(surface, center):
        outline(surface, center)
        draw_lines(surface, center, PSButtonDrawer.__triangle)

    @staticmethod
    def slash(surface, center):
        draw_lines(surface, center, PSButtonDrawer.__slash)
