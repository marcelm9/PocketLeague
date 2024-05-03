import random

import pygame
import PygameXtras as px
import pymunk

from ..files.config import *
from .ball_manager import BallManager
from .field import Field
from .module_collisions import Collisions
from .space import Space


class Player:

    players = [] # TODO: do not store players here but in a seperate class

    @staticmethod
    def reset_all_player_positions():
        random_pos = random.choice(PLAYER_SPAWNS_2_PLAYERS)
        for player in Player.players:
            if player.team == 0:
                player.set_pos(
                    (BALL_SPAWN[0] + random_pos[0], BALL_SPAWN[1] + random_pos[1])
                )
            else:
                # inverse
                player.set_pos(
                    (BALL_SPAWN[0] - random_pos[0], BALL_SPAWN[1] - random_pos[1])
                )

    @staticmethod
    def reset_boosts():
        for player in Player.players:
            player.__boost = PLAYER_BOOST_SECONDS_ON_SPAWN

    def __init__(self):
        self.name = None
        self.team = None
        self.color = None

        # controller input
        self.__controller_index = None
        self.__controller: px.PlayStationController = None
        self.__joystick: int = None # 0 for left, 1 for right
        self.__boost_button = None
        self.__boost = PLAYER_BOOST_SECONDS_ON_SPAWN

        # keyboard input
        self.__keys = [
            pygame.K_w, # up
            pygame.K_s, # down
            pygame.K_a, # left
            pygame.K_d, # right
            pygame.K_SPACE, # boost
        ]

        # stats
        self.__radius = PLAYER_OUTER_RADIUS
        self.__current_speed = 0
        self.__current_direction = pygame.Vector2(0,0)

        # pymunk stuff
        self.__body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.__body.position = (0, 0)
        self.__shape = pymunk.Circle(self.__body, self.__radius)
        self.__shape.elasticity = 0.9

        # bot
        self.__is_bot = False

        Player.players.append(self)
        Space.space.add(self.__body, self.__shape)

    def get_boost(self):
        return self.__boost

    def set_boost_type(self, boost_type: str):
        pass

    def set_goal_explosion(self, goal_explosion: str):
        pass

    def make_bot(self):
        self.__is_bot = True

    def set_name(self, name):
        self.name = name

    def set_team(self, team):
        self.team = team
        assert team in [0, 1]

    def set_color(self, color):
        self.color = color

    def set_pos(self, pos):
        self.__body.position = pos

    def get_pos(self):
        return self.__body.position
    
    def get_radius(self):
        return self.__radius

    def set_keyboard_input(self, up, down, left, right, boost):
        self.__keys[0] = up
        self.__keys[1] = down
        self.__keys[2] = left
        self.__keys[3] = right
        self.__keys[4] = boost

    def set_controller_input(self, controller_index: int, joystick: int, boost_button: int):
        assert joystick in [0, 1]

        self.__controller_index = controller_index
        self.__joystick = joystick
        self.__boost_button = boost_button

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

    def get_input_for_boost(self) -> bool:
        if CONTROLLER_INPUT:
            return self.__controller.get_pressed()[self.__boost_button]
        else:
            keys = pygame.key.get_pressed()
            return keys[self.__keys[4]] # boost

    def update(self, dt_s):

        if self.__is_bot:
            ball = BallManager.get_ball()
            inp = pygame.Vector2(
                ball[0].get_pos()[0] - self.get_pos()[0],
                ball[0].get_pos()[1] - self.get_pos()[1],
            )

        else:
            inp = self.get_input_for_direction()

        if inp.length() > 0:
            if self.get_input_for_boost() and self.__boost > 0:
                max_length = PLAYER_MAX_SPEED_WHEN_BOOSTING
                self.__boost = max(0, self.__boost - dt_s)
            else:
                max_length = PLAYER_MAX_SPEED
            inp.scale_to_length(
                min(max_length, inp.length() * max_length)
            )
            self.__current_speed = inp.length()
            self.__current_direction = inp.normalize()

            # pymunk
            self.__body.velocity = tuple(inp)

            for player in Player.players:
                if player is self:
                    continue
                if Collisions.circleCircle(self.get_pos(), self.get_radius(), player.get_pos(), player.get_radius()):
                    distance_between_players = px.get_distance(self.get_pos(), player.get_pos())
                    distance_to_be_moved = self.get_radius() + player.get_radius() - distance_between_players
                    direction_to_be_moved = pygame.Vector2(
                        self.get_pos()[0] - player.get_pos()[0],
                        self.get_pos()[1] - player.get_pos()[1],
                    )
                    direction_to_be_moved.scale_to_length(distance_to_be_moved)
                    self.set_pos((
                        self.get_pos()[0] + direction_to_be_moved[0],
                        self.get_pos()[1] + direction_to_be_moved[1],
                    ))

        else:
            self.__current_direction = pygame.Vector2(0,0)
            self.__current_speed = 0
            self.__body.velocity = (0,0)

    def keep_in_bounds(self):
        for line in Field.get_lines():
            if Collisions.lineCircle(line.pos1, line.pos2, self.__body.position, self.__radius):
                dist_center_from_line = Collisions.distance_from_center_to_line(line.pos1, line.pos2, self.__body.position)
                dist_move = self.__radius - dist_center_from_line
                v = pygame.Vector2(line.bounce_direction)
                v.scale_to_length(dist_move)

                # pymunk
                self.__body.position = (
                    self.__body.position[0] + v[0],
                    self.__body.position[1] + v[1],
                )

    def draw(self, surface):
        if self.team == 0:
            pygame.draw.circle(surface, TEAM0_COLOR, self.__body.position, PLAYER_OUTER_RADIUS)
        elif self.team == 1:
            pygame.draw.circle(surface, TEAM1_COLOR, self.__body.position, PLAYER_OUTER_RADIUS)
        pygame.draw.circle(surface, self.color, self.__body.position, PLAYER_INNER_RADIUS)

    def get_speed(self):
        return self.__current_speed

    def get_direction(self):
        return self.__current_direction

    def collides_with(self, circle_center, circle_radius) -> bool:
        return ((self.get_pos()[0] - circle_center[0]) ** 2 + (self.get_pos()[1] - circle_center[1]) ** 2) <= (self.get_radius() + circle_radius) ** 2

    def recharge_boost(self):
        self.__boost = PLAYER_BOOST_SECONDS
