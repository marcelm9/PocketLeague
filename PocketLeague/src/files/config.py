WIN_WIDTH = 1920
WIN_HEIGHT = 1080
CENTER = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
FPS = 0

CONTROLLERS_NEEDED = 1

FIELD_WIDTH = 1600
FIELD_HEIGHT = 900
FIELD_CORNER_SMOOTHING = 50
FIELD_LINE_SIZE = 3
GOAL_SIZE = 200
GOAL_DEPTH = 50

PLAYER_OUTER_RADIUS = 20
PLAYER_INNER_RADIUS = PLAYER_OUTER_RADIUS // 2
PLAYER_MAX_SPEED = 500
BALL_RADIUS = 12
BALL_MAX_SPEED = 4_000
BALL_COLOR = (255, 255, 255)
BALL_SPAWN = CENTER
BOOST_PERCENT_ON_SPAWN = 0.33
PLAYER_BOOST_FACTOR = 1.8
PLAYER_MAX_SPEED_WHEN_BOOSTING = PLAYER_MAX_SPEED * PLAYER_BOOST_FACTOR

# for goal detection
FIELD_LEFT_EDGE = WIN_WIDTH // 2 - FIELD_WIDTH // 2 - BALL_RADIUS
FIELD_RIGHT_EDGE = WIN_WIDTH // 2 + FIELD_WIDTH // 2 + BALL_RADIUS
FIELD_TOP_EDGE = WIN_HEIGHT // 2 - FIELD_HEIGHT // 2
FIELD_BOTTOM_EDGE = WIN_HEIGHT // 2 + FIELD_HEIGHT // 2

TEAM_COLOR_MAP = {"Team Blue": (0, 0, 190), "Team Orange": (255, 128, 0)}
COLOR_MAP = {
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "chartreuse": (128, 255, 0),
    "spring green": (0, 255, 128),
    "azure": (0, 128, 255),
    "violet": (128, 0, 255),
    "rose": (255, 0, 128),
}
COLOR_NAMES = list(COLOR_MAP.keys())
COLOR_VALUES = list(COLOR_MAP.items())
NAMES = [
    "Lena",
    "Nahee",
    "Pascal",
    "Marcel",
    "Leninator99",
    "Nachodip03",
    "BlackRice_",
    "Golfmensch99",
    "GoatRice",
]
TEAM_NAMES = ["Team Blue", "Team Orange"]
BOOST_TYPES = list(COLOR_MAP.keys())
GOAL_EXPLOSION_TYPES = [
    "regular",
    "red explosion",
    "green explosion",
    "dragons",
]

HUD_BW = 10
HUD_BR = 10
HUD_TEXT_SIZE = 40
HUD_FONT = "verdana"
HUD_DIMENSIONS = (320, 70)
HUD_TEXT_OFFSET = (0, 0)
HUD_SIDE_DISTANCE = (10, 10)

HUD_GOAL_COLON_MIDTOP_POS = (WIN_WIDTH // 2, 4)
HUD_GOAL_TEXTSIZE = 60
HUD_GOAL_FONT = "verdana"
HUD_GOAL_TC = (255, 255, 255)
HUD_GOAL_TO = (0, 2)
HUD_GOAL_FH = HUD_DIMENSIONS[1]
HUD_TIME_MIDBOTTOM_POS = (WIN_WIDTH // 2, WIN_HEIGHT - 9)

# vectors from center, for left side of field (right side is mirrored)
PLAYER_SPAWNS = ((-500, -200), (-600, 0), (-500, 200))

MATCH_COUNTDOWN = 3

BOOST_PAD_RECHARGE_TIME = 13
BOOST_PAD_RADIUS = 13

BOOST_DISPLAY_SIZE = 65
BOOST_DISPLAY_LINE_SIZE = 20

PLAYER_SELECTION_PANEL_POSITIONS = (
    (WIN_WIDTH / 5 * 1, CENTER[1] - 40),
    (WIN_WIDTH / 5 * 2, CENTER[1] - 40),
    (WIN_WIDTH / 5 * 3, CENTER[1] - 40),
    (WIN_WIDTH / 5 * 4, CENTER[1] - 40),
)
PLAYER_SELECTION_PANEL_SIZE = (340, 850)
PLAYER_SELECTION_PANEL_PREVIEW_OFFSET = (PLAYER_SELECTION_PANEL_SIZE[0] // 2, 60)

BUTTON_DRAWER_SIZE = 40
BUTTON_DRAWER_LINE_WIDTH = 5

AFTER_MATCH_SCREEN_SIZE = 1200, 800

POINTS_WEIGHT_TOUCH = 2
POINTS_WEIGHT_GOAL = 100
POINTS_WEIGHT_SHOT = 10
POINTS_WEIGHT_SAVE = 50
POINTS_WEIGHT_ASSIST = 75
DISTANCE_FROM_GOAL_FOR_SHOT = 450
DISTANCE_FROM_GOAL_FOR_SHOT_SQUARED = DISTANCE_FROM_GOAL_FOR_SHOT**2

AFTER_GOAL_SECONDS = 3

# modifiers
MAPS = ["Regular", "Diagonal"]
MATCH_TIMES = [i for i in range(60, 301, 30)]
BALL_BOUNCINESS_MAP = {
    "very low": 0.2,
    "low": 0.5,
    "regular": 1,
    "high": 1.3,
    "very high": 1.7,
}
SIMULATION_PRECISION_MAP = {
    "very low": 10,
    "low": 10,
    "regular": 15,
    "high": 25,
    "very high": 100,
}
BOOST_CAPACITY_MAP = {  # in seconds
    "off": 0,
    "low": 0.75,
    "regular": 1.5,
    "high": 2,
    "very high": 3,
    "unlimited": 99999,
}
