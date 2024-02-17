import pygame
import sys
import PygameXtras as px

c1 = {
    'black': (0,0,0),
    'white': (255,255,255),
    'cyan': (0,255,255),
    'magenta': (255,0,255),
    'yellow': (255,255,0),
    'red': (255,0,0),
    'green': (0,255,0),
    'blue': (0,0,255)
}

pygame.init()
screen = pygame.display.set_mode((500,500))
fpsclock = pygame.time.Clock()
fps = 60

def circle(xy, color, radius=3, width=0):
    color = c1[color] if isinstance(color, str) else color
    pygame.draw.circle(screen, color, xy, radius, width)

def line(xy1, xy2, color, width=1):
    color = c1[color] if isinstance(color, str) else color
    pygame.draw.line(screen, color, xy1, xy2, width)

def rect(r, color, width=0):
    color = c1[color] if isinstance(color, str) else color
    pygame.draw.rect(screen, color, r, width)

center = (screen.get_width() // 2, screen.get_height() // 2)

v1 = pygame.Vector2(0, -1)
v1.scale_to_length(150)
v2 = pygame.Vector2(1, 0)
v2.scale_to_length(150)

label = px.Label(screen, f"{v1.dot(v2) = }", 40, (10, 10), "topleft", tc=(255,255,255))

l_v1 = px.Label(screen, "v1", 40, (10, 50), "topleft", tc=(255,0,0))
l_v2 = px.Label(screen, "v2", 40, (10, 90), "topleft", tc=(0,255,0))

jump = 1

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        v1.rotate_ip(jump)
    if keys[pygame.K_2]:
        v1.rotate_ip(-jump)
    if keys[pygame.K_3]:
        v2.rotate_ip(jump)
    if keys[pygame.K_4]:
        v2.rotate_ip(-jump)


    label.update_text(f"{v1.dot(v2) = }")

    screen.fill((0,0,0))
    label.draw()
    l_v1.draw()
    l_v2.draw()
    line(center, (center[0] + v1[0], center[1] + v1[1]), "red")
    line(center, (center[0] + v2[0], center[1] + v2[1]), "green")


    pygame.display.flip()
    fpsclock.tick(fps)