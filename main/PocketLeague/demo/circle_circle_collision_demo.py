import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Collision and Reflection")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define Circle class
class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Define Vector class
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def distance(circle1, circle2):
    return math.sqrt((circle1.x - circle2.x)**2 + (circle1.y - circle2.y)**2)

def normalize(vector):
    magnitude = math.sqrt(vector.x**2 + vector.y**2)
    if magnitude == 0:
        return Vector(0, 0)
    return Vector(vector.x / magnitude, vector.y / magnitude)

def dot_product(vector1, vector2):
    return vector1.x * vector2.x + vector1.y * vector2.y

def reflect(velocity, normal):
    dot = dot_product(velocity, normal)
    reflected = Vector(velocity.x - 2 * dot * normal.x, velocity.y - 2 * dot * normal.y)
    return reflected

def handle_collision(moving_circle, static_circle, moving_velocity):
    if distance(moving_circle, static_circle) <= moving_circle.radius + static_circle.radius:
        # Calculate normal vector at the point of collision
        normal = Vector(static_circle.x - moving_circle.x, static_circle.y - moving_circle.y)
        normal = normalize(normal)

        # Calculate angle of incidence
        incidence_angle = math.atan2(moving_velocity.y, moving_velocity.x) - math.atan2(normal.y, normal.x)

        # Reflect velocity vector
        reflected_velocity = reflect(moving_velocity, normal)

        return reflected_velocity

    return moving_velocity  # No collision

# Create circles
static_circle = Circle(200, 200, 50, RED)
moving_circle = Circle(300, 300, 30, BLUE)
moving_velocity = Vector(-0.8, -0.2)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the moving circle
    moving_circle.x += moving_velocity.x
    moving_circle.y += moving_velocity.y

    # Handle collision
    moving_velocity = handle_collision(moving_circle, static_circle, moving_velocity)

    # Clear the screen
    screen.fill(WHITE)

    # Draw circles
    static_circle.draw()
    moving_circle.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
