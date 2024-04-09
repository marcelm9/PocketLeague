import pygame
import PygameXtras as px

from ..files.config import *
from .player import Player
from .match_stats import MatchStats


class HUD:

    screen: pygame.Surface
    labels = []

    goal_colon: px.Label
    team_0_goal_label: px.Label
    team_1_goal_label: px.Label
    time_label: px.Label

    def init(screen):
        assert len(Player.players) in (2, 4)
        HUD.screen = screen
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

    def update_score():
        HUD.team_0_goal_label.update_text(MatchStats.get_goals_team0())
        HUD.team_1_goal_label.update_text(MatchStats.get_goals_team1())

    def update_time(seconds_left):
        m, s = seconds_left // 60, seconds_left % 60
        HUD.time_label.update_text(f"{m}:{s:02}")

    def draw():
        for label in HUD.labels:
            label.draw()
        HUD.goal_colon.draw()
        HUD.team_0_goal_label.draw()
        HUD.team_1_goal_label.draw()
        HUD.time_label.draw()
