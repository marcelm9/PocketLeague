import pygame
from .field import Field
from .player import Player
from .module_collisions import Collisions
from ..files.config import BALL_MAX_SPEED, BALL_COLOR, BALL_SPEED_REDUCTION_FACTOR

class Ball:
    def __init__(self, pos, radius, vector = (0,0)):
        self.pos = list(pos)
        self.vector = pygame.Vector2(vector)
        self.radius = radius

    def update(self):
        for player in Player.players:
            if Collisions.circleCircle(player.get_pos(), player.get_radius(), self.pos, self.radius):
                self.vector = pygame.Vector2(
                    self.pos[0] - player.get_pos()[0],
                    self.pos[1] - player.get_pos()[1]
                )
                self.vector.scale_to_length(player.get_speed())
                # TODO: if the player only hits the side of the ball, the ball should receive less speed from the player
                if self.vector.length() > BALL_MAX_SPEED:
                    self.vector.scale_to_length(BALL_MAX_SPEED)

        if self.vector.length() > 0:
            self.pos[0] += self.vector[0]
            self.pos[1] += self.vector[1]
            self.vector.scale_to_length(
                self.vector.length() * BALL_SPEED_REDUCTION_FACTOR
            )

            for line in Field.get_lines():
                if dist := Collisions.lineCircle(line.pos1, line.pos2, self.pos, self.radius):
                    self.mirror_around_vector(line.bounce_direction)
                    v = pygame.Vector2(line.bounce_direction)
                    v.scale_to_length(dist * 2)
                    self.pos[0] += v[0]
                    self.pos[1] += v[1]

    def draw(self, surface):
        pygame.draw.circle(surface, BALL_COLOR, self.pos, self.radius)

    def mirror_around_vector(self, vector):
        dot_product = 2 * self.vector.dot(vector)
        self.vector -= dot_product * vector
