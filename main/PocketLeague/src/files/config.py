WIN_WIDTH = 1920
WIN_HEIGHT = 1080
CENTER = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
FPS = 60

CONTROLLERS_NEEDED = 1
CONTROLLER_INPUT = True

FIELD_WIDTH = 1600
FIELD_HEIGHT = 900
FIELD_CORNER_SMOOTHING = 50
FIELD_LINE_SIZE = 9
GOAL_SIZE = 200
GOAL_DEPTH = 50

PLAYER_RADIUS = 20
PLAYER_MAX_SPEED = 0.5
BALL_RADIUS = 12
BALL_MAX_SPEED = 15
BALL_COLOR = (255, 255, 255)
BALL_SPAWN = (
    WIN_WIDTH // 2,
    WIN_HEIGHT // 2
)

# for goal detection
FIELD_LEFT_EDGE = WIN_WIDTH // 2 - FIELD_WIDTH // 2 - BALL_RADIUS
FIELD_RIGHT_EDGE = WIN_WIDTH // 2 + FIELD_WIDTH // 2 + BALL_RADIUS

TEAM0_COLOR = (0,0,190)
TEAM1_COLOR = (255,128,0)
PLAYER_TEAM0_COLORS = [
    (0,0,255),
    (255,0,255),
    (0,255,0),
    (0,128,0),
]
PLAYER_TEAM1_COLORS = [
    (255,0,0),
    (255,255,0),
    (170,0,0),
    (139,69,19),
]

HUD_BW = 10
HUD_BR = 10 
HUD_TEXT_SIZE = 40
HUD_FONT = "verdana"
HUD_DIMENSIONS = (250,70)
HUD_TEXT_OFFSET = (0,0)
HUD_SIDE_DISTANCE = (10,10)

HUD_GOAL_COLON_MIDTOP_POS = (WIN_WIDTH // 2, 4)
HUD_GOAL_TEXTSIZE = 60
HUD_GOAL_FONT = "verdana"
HUD_GOAL_TC = (255, 255, 255)
HUD_GOAL_TO = (0, 2)
HUD_GOAL_FH = HUD_DIMENSIONS[1]

BALL_SPEED_REDUCTION_FACTOR = 0.99

# vectors from center, for left side of field (right side is mirrored)
PLAYER_SPAWNS_2_PLAYERS = (
    (-500, -200),
    (-600, 0),
    (-500, 200)
)
PLAYER_SPAWNS_4_PLAYERS = (
    # TODO
)
