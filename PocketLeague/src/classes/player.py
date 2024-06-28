import random

import pygame
import PygameXtras as px
import pymunk

from ..files.config import *
from .ball_manager import BallManager
from .field import Field
from .module_collisions import Collisions
from .particle_manager import ParticleManager
from .sounds import Sounds
from .space import Space


class Player:

    def __init__(self):
        self.__name = None

        # controller input
        self.__controller_index = None
        self.__controller: px.PSController = None
        self.__joystick: int = None  # 0 for left, 1 for right
        self.__boost_button = None
        self.__boost = BOOST_CAPACITY_MAP["regular"] * BOOST_PERCENT_ON_SPAWN
        self.__max_boost = BOOST_CAPACITY_MAP["regular"]

        # stats
        self.__radius = PLAYER_OUTER_RADIUS
        self.__current_speed = 0
        self.__current_direction = pygame.Vector2(0, 0)

        # pymunk stuff
        self.__body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.__body.position = (0, 0)
        self.__shape = pymunk.Circle(self.__body, self.__radius)
        self.__shape.elasticity = 0.9
        id = Space.get_and_incr_id()
        self.__shape.collision_type = id

        # bot
        self.__is_bot = False

        Space.space.add(self.__body, self.__shape)
        Space.add_mapping(id, self)

    def collides_with(self, circle_center, circle_radius) -> bool:
        return (self.get_pos()[0] - circle_center[0]) ** 2 + (
            self.get_pos()[1] - circle_center[1]
        ) ** 2 <= (self.get_radius() + circle_radius) ** 2

    def draw(self, surface):
        pygame.draw.circle(
            surface, self.__team_color, self.__body.position, PLAYER_OUTER_RADIUS
        )
        pygame.draw.circle(
            surface, self.__color, self.__body.position, PLAYER_INNER_RADIUS
        )

    def get_boost(self):
        return self.__boost

    def get_max_boost(self):
        return self.__max_boost

    def get_color(self):
        return self.__color

    def get_direction(self):
        return self.__current_direction

    def get_input_for_boost(self) -> bool:
        self.__controller.update()
        if self.__boost_button == 9:
            return self.__controller.l1
        elif self.__boost_button == 10:
            return self.__controller.r1

    def get_input_for_direction(self) -> pygame.Vector2:
        """
        Returns a vector pointing into the desired movement direction (SCALED to be between 0 (min) to 1 (max))
        """
        if self.__joystick == 0:
            return pygame.Vector2(self.__controller.get_left_stick())
        elif self.__joystick == 1:
            return pygame.Vector2(self.__controller.get_right_stick())

    def get_name(self):
        return self.__name

    def get_pos(self):
        return self.__body.position

    def get_radius(self):
        return self.__radius

    def get_speed(self):
        return self.__current_speed

    def get_team(self):
        return self.__team

    def keep_in_bounds(self):
        for line in Field.get_lines() + Field.get_goal_lines():
            if Collisions.lineCircle(
                line.pos1, line.pos2, self.__body.position, self.__radius
            ):
                dist_center_from_line = Collisions.distance_from_center_to_line(
                    line.pos1, line.pos2, self.__body.position
                )
                dist_move = self.__radius - dist_center_from_line
                v = pygame.Vector2(line.get_bounce_direction())
                v.scale_to_length(dist_move)
                # pymunk
                self.__body.position = (
                    self.__body.position[0] + v[0],
                    self.__body.position[1] + v[1],
                )

    def make_bot(self):
        self.__is_bot = True

    def recharge_boost(self):
        self.__boost = self.__max_boost

    def reset_boost(self):
        self.__boost = self.__max_boost * BOOST_PERCENT_ON_SPAWN

    def set_boost_type(self, boost_type: str):
        self.__boost_color = COLOR_MAP[boost_type]

    def set_color(self, color):
        self.__color = COLOR_MAP[color]

    def set_controller_input(
        self, controller_index: int, joystick: int, boost_button: int
    ):
        assert joystick in [0, 1]
        self.__controller_index = controller_index
        self.__joystick = joystick
        self.__boost_button = boost_button
        print(boost_button)
        self.__controller = px.PSController(self.__controller_index)

    def set_name(self, name):
        self.__name = name

    def set_pos(self, pos):
        self.__body.position = pos

    def set_team(self, team: str):
        assert team in ("Team Blue", "Team Orange")
        self.__team = team
        self.__team_color = TEAM_COLOR_MAP[team]

    def set_boost_capacity(self, boost_capacity: str):
        self.__max_boost = BOOST_CAPACITY_MAP[boost_capacity]

    def update(self, dt_s, all_players: list):
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
                ParticleManager.create_particle(
                    self.get_pos(),
                    (-inp[0] * random.random() * 3, -inp[1] * random.random() * 3),
                    self.__boost_color,
                    0.6,
                    9,
                    0,
                )
                Sounds.start_boost(self.__name)
            else:
                max_length = PLAYER_MAX_SPEED
                Sounds.end_boost(self.__name)
            inp.scale_to_length(min(max_length, inp.length() * max_length))
            self.__current_speed = inp.length()
            self.__current_direction = inp.normalize()
            # pymunk
            self.__body.velocity = tuple(inp)
            for player in all_players:
                if player is self:
                    continue
                if Collisions.circleCircle(
                    self.get_pos(),
                    self.get_radius(),
                    player.get_pos(),
                    player.get_radius(),
                ):
                    distance_between_players = px.get_distance(
                        self.get_pos(), player.get_pos()
                    )
                    distance_to_be_moved = (
                        self.get_radius()
                        + player.get_radius()
                        - distance_between_players
                    )
                    direction_to_be_moved = pygame.Vector2(
                        self.get_pos()[0] - player.get_pos()[0],
                        self.get_pos()[1] - player.get_pos()[1],
                    )
                    direction_to_be_moved.scale_to_length(distance_to_be_moved)
                    self.set_pos(
                        (
                            self.get_pos()[0] + direction_to_be_moved[0],
                            self.get_pos()[1] + direction_to_be_moved[1],
                        )
                    )
        else:
            self.__current_direction = pygame.Vector2(0, 0)
            self.__current_speed = 0
            self.__body.velocity = (0, 0)
