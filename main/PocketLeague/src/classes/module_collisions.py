import pygame
import math

class Collisions:

    @staticmethod
    def __clamp(value, min_value, max_value):
        """Clamp value to a range between min_value and max_value."""
        return max(min_value, min(value, max_value))

    @staticmethod
    def rectCircle(rect, circle_center, radius):
        circ_x, circ_y = circle_center
        # Find the closest point to the circle within the rect.
        closest_x = Collisions.__clamp(circ_x, rect.left, rect.right)
        closest_y = Collisions.__clamp(circ_y, rect.top, rect.bottom)
        # Calculate the distance between the circle's
        # center and this closest point.
        distance_x = circ_x - closest_x
        distance_y = circ_y - closest_y
        # If the distance is less than the circle's
        # radius, an intersection occurs.
        distance_squared = distance_x**2 + distance_y**2
        return distance_squared < radius**2

    @staticmethod
    def any_collision(rect, pos_list, radius):
        for pos in pos_list:
            if Collisions.rectCircle(rect, pos, radius):
                return True
        return False

    @staticmethod
    def lineLine(line1_start, line1_end, line2_start, line2_end):
        uA = ((line2_end[0] - line2_start[0]) * (line1_start[1] - line2_start[1]) - (line2_end[1] - line2_start[1]) *
            (line1_start[0] - line2_start[0])) / ((line2_end[1] - line2_start[1]) *
                                                    (line1_end[0] - line1_start[0]) - (line2_end[0] - line2_start[0]) * (line1_end[1] - line1_start[1]))
        uB = ((line1_end[0] - line1_start[0]) * (line1_start[1] - line2_start[1]) - (line1_end[1] - line1_start[1]) *
            (line1_start[0] - line2_start[0])) / ((line2_end[1] - line2_start[1]) *
                                                    (line1_end[0] - line1_start[0]) - (line2_end[0] - line2_start[0]) * (line1_end[1] - line1_start[1]))
        
        if (0 <= uA <= 1) and (0 <= uB <= 1):
            return (
                line1_start[0] + (uA * (line1_end[0] - line1_start[0])),
                line1_start[1] + (uA * (line1_end[1] - line1_start[1]))
            )
        return False

    @staticmethod
    def lineRect(line_start, line_end, rect) -> bool | tuple:
        assert isinstance(rect, pygame.Rect), f"invalid type for rect ({type(rect)}): {rect}"
        left = (rect.topleft, rect.bottomleft)
        right = (rect.topright, rect.bottomright)
        top = (rect.topleft, rect.topright)
        bottom = (rect.bottomleft, rect.bottomright)

        if x := Collisions.lineLine(line_start, line_end, *left):
            return x
        if x := Collisions.lineLine(line_start, line_end, *right):
            return x
        if x := Collisions.lineLine(line_start, line_end, *top):
            return x
        if x := Collisions.lineLine(line_start, line_end, *bottom):
            return x
        
        return False

    @staticmethod
    def circleCircle(c1_center, c1_radius, c2_center, c2_radius) -> bool:
        distance_squared = (c1_center[0] - c2_center[0]) ** 2 + (c1_center[1] - c2_center[1]) ** 2
        radii_squared = (c1_radius + c2_radius) ** 2
        return distance_squared <= radii_squared

    @staticmethod
    def lineCircle(line_start, line_end, circle_center, circle_radius) -> bool | tuple:
        Q = pygame.Vector2(circle_center)                           # Center of circle
        r = circle_radius                                           # Radius of circle
        P1 = pygame.Vector2(line_start)                             # Start of line segment
        V = pygame.Vector2(line_end) - pygame.Vector2(line_start)   # Vector along line segment
        a = V.dot(V)
        b = 2 * V.dot(P1 - Q)
        c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r**2
        disc = b**2 - 4 * a * c
        if disc < 0:
            return False
        sqrt_disc = math.sqrt(disc)
        t1 = (-b + sqrt_disc) / (2 * a)
        t2 = (-b - sqrt_disc) / (2 * a)
        if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
            return False
        t = max(0, min(1, - b / (2 * a)))
        return t
