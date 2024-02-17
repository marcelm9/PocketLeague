import pygame
import PygameXtras as px
from .field import Field
from ..files.config import CONTROLLER_INPUT, PLAYER_RADIUS, PLAYER_MAX_SPEED
from .module_collisions import Collisions

class Player:

    players = []

    def __init__(self):
        self.name = None
        self.team = None
        self.color = None

        # controller input
        self.__controller_index = None
        self.__controller: px.PlayStationController = None
        self.__joystick: int = None # 0 for left, 1 for right
        self.__dash_button = None

        # keyboard input
        self.__keys = [
            None, # up
            None, # down
            None, # left
            None, # right
            None, # dash
        ]

        # stats
        self.__pos = (0,0)
        self.__radius = PLAYER_RADIUS
        self.__speed = PLAYER_MAX_SPEED
        self.__current_speed = 0
        self.__current_direction = pygame.Vector2(0,0)

        Player.players.append(self)

    def set_name(self, name):
        self.name = name

    def set_team(self, team):
        self.team = team
        assert team in [0, 1]

    def set_color(self, color):
        self.color = color

    def set_pos(self, pos):
        self.__pos = list(pos)

    def get_pos(self):
        return self.__pos
    
    def get_radius(self):
        return self.__radius

    def set_keyboard_input(self, up, down, left, right, dash):
        self.__keys[0] = up
        self.__keys[1] = down
        self.__keys[2] = left
        self.__keys[3] = right
        self.__keys[4] = dash

    def set_controller_input(self, controller_index: int, joystick: int, dash_button: int):
        assert joystick in [0, 1]

        self.__controller_index = controller_index
        self.__joystick = joystick
        self.__dash_button = dash_button

        self.__controller = px.PlayStationController(self.__controller_index)

    def get_input_for_direction(self) -> pygame.Vector2:
        """
        Returns a vector pointing into the desired movement direction (SCALED to be between 0 (min) to 1 (max))
        """
        if CONTROLLER_INPUT:
            assert self.__controller is not None
            if self.__joystick == 0:
                return pygame.Vector2(self.__controller.get_left_stick())
            elif self.__joystick == 1:
                return pygame.Vector2(self.__controller.get_right_stick())

        else:
            keys = pygame.key.get_pressed()
            v = pygame.Vector2(0, 0)
            if keys[self.__keys[0]]: # up
                v[1] -= 1
            if keys[self.__keys[1]]: # down
                v[1] += 1
            if keys[self.__keys[2]]: # left
                v[0] -= 1
            if keys[self.__keys[3]]: # right
                v[0] += 1

            if v.length() > 0:
                v.scale_to_length(1)
            return v

    def get_input_for_dash(self) -> bool:
        if CONTROLLER_INPUT:
            return self.__controller.get_pressed()[self.__dash_button]
        else:
            keys = pygame.key.get_pressed()
            return keys[self.__keys[4]] # dash

    def update(self):
        inp = self.get_input_for_direction()
        if inp.length() > 0:
            inp.scale_to_length(
                min(self.__speed, inp.length() * self.__speed)
            )
            self.__pos[0] += inp[0]
            self.__pos[1] += inp[1]
            self.__current_speed = inp.length()
            self.__current_direction = inp.normalize()
        else:
            self.__current_direction = pygame.Vector2(0,0)
            self.__current_speed = 0

        for line in Field.get_lines():
            if Collisions.lineCircle(line.pos1, line.pos2, self.__pos, self.__radius):
                dist_center_from_line = Collisions.distance_from_center_to_line(line.pos1, line.pos2, self.__pos)
                dist_move = self.__radius - dist_center_from_line
                v = pygame.Vector2(line.bounce_direction)
                v.scale_to_length(dist_move)
                self.__pos[0] += v[0]
                self.__pos[1] += v[1]

    def draw(self, surface):
        if self.team == 0:
            pygame.draw.circle(surface, (0,0,255), self.__pos, self.__radius)
        elif self.team == 1:
            pygame.draw.circle(surface, (255,255,0), self.__pos, self.__radius)
        pygame.draw.circle(surface, self.color, self.__pos, self.__radius * 0.5)

    def get_speed(self):
        return self.__current_speed

    def get_direction(self):
        return self.__current_direction