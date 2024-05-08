import math

import pygame
import PygameXtras as px

from .player_manager import PlayerManager

from ..files.config import *
from .boost_display import BoostDisplay
from .match_stats import MatchStats


class HUD:

    screen: pygame.Surface
    labels: list[px.Label] = []
    boost_displays: list[BoostDisplay] = []

    goal_colon: px.Label
    team_0_goal_label: px.Label
    team_1_goal_label: px.Label
    time_label: px.Label

    # for now
    player_0_boost_rect = pygame.Rect(0,0,200,40)
    player_0_boost_rect.midtop = (500, 10)
    player_1_boost_rect = pygame.Rect(0,0,200,40)
    player_1_boost_rect.midtop = (WIN_WIDTH - 500, 10)

    def init(screen: pygame.Surface):
        HUD.screen = screen
        positions = [
            # label position, label anchor, boost_display offset
            ((10, 10), "topleft", (225, 0)),
            ((screen.get_width() - 10, 10), "topright", (-225, 0)),
            ((10, screen.get_height() - 10), "bottomleft", (225, 0)),
            ((screen.get_width() - 10, screen.get_height() - 10), "bottomright", (-225, 0)),
        ]
        for i, player in enumerate(PlayerManager.get_players()):
            HUD.labels.append(
                px.Label(
                    screen,
                    player.get_name(),
                    HUD_TEXT_SIZE,
                    positions[i][0],
                    positions[i][1],
                    bgc=player.get_color(),
                    bc=TEAM_COLOR_MAP[player.get_team()],
                    f=HUD_FONT,
                    fd=HUD_DIMENSIONS,
                    bw=HUD_BW,
                    br=HUD_BR,
                    to=HUD_TEXT_OFFSET,
                )
            )
            HUD.boost_displays.append(
                BoostDisplay((
                    HUD.labels[i].center[0] + positions[i][2][0],
                    HUD.labels[i].center[1] + positions[i][2][1]
                ))
            )

        HUD.goal_colon = px.Label(
            screen,
            ":",
            HUD_GOAL_TEXTSIZE,
            HUD_GOAL_COLON_MIDTOP_POS,
            "midtop",
            fh=HUD_GOAL_FH,
            tc=HUD_GOAL_TC,
            f=HUD_GOAL_FONT
        )
        HUD.team_0_goal_label = px.Label(
            screen,
            MatchStats.get_goals_team0(),
            HUD_GOAL_TEXTSIZE,
            HUD.goal_colon.midleft,
            "midright",
            fh=HUD_GOAL_FH,
            f=HUD_GOAL_FONT,
            tc=HUD_GOAL_TC,
            to=HUD_GOAL_TO
        )
        HUD.team_1_goal_label = px.Label(
            screen,
            MatchStats.get_goals_team1(),
            HUD_GOAL_TEXTSIZE,
            HUD.goal_colon.midright,
            "midleft",
            fh=HUD_GOAL_FH,
            f=HUD_GOAL_FONT,
            tc=HUD_GOAL_TC,
            to=HUD_GOAL_TO
        )
        HUD.time_label = px.Label(
            screen,
            "n/a",
            HUD_GOAL_TEXTSIZE,
            HUD_TIME_MIDBOTTOM_POS,
            "midbottom",
            fh=HUD_GOAL_FH,
            tc=HUD_GOAL_TC,
            f=HUD_GOAL_FONT
        )
        HUD.countdown_label = px.Label(
            screen,
            "n/a",
            HUD_GOAL_TEXTSIZE * 2,
            (screen.get_width() // 2, screen.get_height() // 2),
            tc=(255, 255, 255),
            bgc=(0,0,0),
            fd=(200, 200),
            br=200,
            bw=6,
            bc=(255,255,255),
            to=(0, 3)
        )

    def update_score():
        HUD.team_0_goal_label.update_text(MatchStats.get_goals_team0())
        HUD.team_1_goal_label.update_text(MatchStats.get_goals_team1())

    def update_time_display():
        m, s = int(MatchStats.get_match_seconds_left() // 60), int(MatchStats.get_match_seconds_left() % 60)
        HUD.time_label.update_text(f"{m}:{s:02}")

    def update():
        HUD.update_time_display()
        HUD.update_boosts()

    def draw():
        for label in HUD.labels:
            label.draw()
        for boost_display in HUD.boost_displays:
            boost_display.draw(HUD.screen)
        HUD.goal_colon.draw()
        HUD.team_0_goal_label.draw()
        HUD.team_1_goal_label.draw()
        HUD.time_label.draw()

        if MatchStats.get_countdown() > 0:
            HUD.countdown_label.update_text(math.ceil(MatchStats.get_countdown()))
            HUD.countdown_label.draw()

    def update_boosts():
        for i, player in enumerate(PlayerManager.get_players()):
            HUD.boost_displays[i].update(player.get_boost())

