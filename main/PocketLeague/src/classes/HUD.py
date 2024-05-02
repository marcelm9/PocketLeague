import math

import pygame
import PygameXtras as px

from ..files.config import *
from .boost_display import BoostDisplay
from .match_stats import MatchStats
from .player import Player


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

    def init(screen):
        assert len(Player.players) in (2, 4)
        team_color = [
            TEAM0_COLOR,
            TEAM1_COLOR,
        ]
        if len(Player.players) == 2:
            HUD.labels.append(
                px.Label(
                    screen,
                    Player.players[0].name,
                    HUD_TEXT_SIZE,
                    HUD_SIDE_DISTANCE,
                    "topleft",
                    f=HUD_FONT,
                    bgc=Player.players[0].color,
                    fd=HUD_DIMENSIONS,
                    bc=team_color[Player.players[0].team],
                    bw=HUD_BW,
                    br=HUD_BR,
                    to=HUD_TEXT_OFFSET,
                )
            )
            HUD.boost_displays.append(
                BoostDisplay((
                    HUD.labels[0].midright[0] + 100,
                    HUD.labels[0].center[1]
                ))
            )
            HUD.labels.append(
                px.Label(
                    screen,
                    Player.players[1].name,
                    HUD_TEXT_SIZE,
                    (WIN_WIDTH - HUD_SIDE_DISTANCE[0], HUD_SIDE_DISTANCE[1]),
                    "topright",
                    f=HUD_FONT,
                    bgc=Player.players[1].color,
                    fd=HUD_DIMENSIONS,
                    bc=team_color[Player.players[1].team],
                    bw=HUD_BW,
                    br=HUD_BR,
                    to=HUD_TEXT_OFFSET,
                )
            )
            HUD.boost_displays.append(
                BoostDisplay((
                    HUD.labels[1].midleft[0] - 100,
                    HUD.labels[1].center[1]
                ))
            )
        if len(Player.players) == 4:
            HUD.labels.append(
                px.Label(
                    screen,
                    Player.players[0].name,
                    HUD_TEXT_SIZE,
                    HUD_SIDE_DISTANCE,
                    "topleft",
                    f=HUD_FONT,
                    bgc=Player.players[0].color,
                    fd=HUD_DIMENSIONS,
                    bc=team_color[Player.players[0].team],
                    bw=HUD_BW,
                    br=HUD_BR,
                    to=HUD_TEXT_OFFSET,
                )
            )
            HUD.labels.append(
                px.Label(
                    screen,
                    Player.players[1].name,
                    HUD_TEXT_SIZE,
                    (HUD_SIDE_DISTANCE[0], WIN_HEIGHT - HUD_SIDE_DISTANCE[1]),
                    "bottomleft",
                    f=HUD_FONT,
                    bgc=Player.players[1].color,
                    fd=HUD_DIMENSIONS,
                    bc=team_color[Player.players[1].team],
                    bw=HUD_BW,
                    br=HUD_BR,
                    to=HUD_TEXT_OFFSET,
                )
            )
            HUD.labels.append(
                px.Label(
                    screen,
                    Player.players[2].name,
                    HUD_TEXT_SIZE,
                    (WIN_WIDTH - HUD_SIDE_DISTANCE[0], HUD_SIDE_DISTANCE[1]),
                    "topright",
                    f=HUD_FONT,
                    bgc=Player.players[2].color,
                    fd=HUD_DIMENSIONS,
                    bc=team_color[Player.players[2].team],
                    bw=HUD_BW,
                    br=HUD_BR,
                    to=HUD_TEXT_OFFSET,
                )
            )
            HUD.labels.append(
                px.Label(
                    screen,
                    Player.players[3].name,
                    HUD_TEXT_SIZE,
                    (
                        WIN_WIDTH - HUD_SIDE_DISTANCE[0],
                        WIN_HEIGHT - HUD_SIDE_DISTANCE[1],
                    ),
                    "bottomright",
                    f=HUD_FONT,
                    bgc=Player.players[3].color,
                    fd=HUD_DIMENSIONS,
                    bc=team_color[Player.players[3].team],
                    bw=HUD_BW,
                    br=HUD_BR,
                    to=HUD_TEXT_OFFSET,
                )
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
        for i in range(len(Player.players)):
            HUD.boost_displays[i].update(Player.players[i].get_boost())

