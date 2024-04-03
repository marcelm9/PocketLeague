from .player import Player
from ..files.config import *
import pygame
import PygameXtras as px

class HUD:

    screen: pygame.Surface
    labels = [] 

    def init(screen):
        assert len(Player.players) in (2,4)
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
                    f = HUD_FONT,
                    bgc = Player.players[0].color,
                    fd = HUD_DIMENSIONS,
                    bc = team_color[Player.players[0].team],
                    bw = HUD_BW,
                    br = HUD_BR,
                    to = HUD_TEXT_OFFSET
                )
            )
            HUD.labels.append(
                px.Label(
                    screen,
                    Player.players[1].name,
                    HUD_TEXT_SIZE,
                    (WIN_WIDTH - HUD_SIDE_DISTANCE[0], HUD_SIDE_DISTANCE[1]),
                    "topright",
                    f = HUD_FONT,
                    bgc = Player.players[1].color,
                    fd = HUD_DIMENSIONS,
                    bc = team_color[Player.players[1].team],
                    bw = HUD_BW,
                    br = HUD_BR,
                    to = HUD_TEXT_OFFSET
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
                    f = HUD_FONT,
                    bgc = Player.players[0].color,
                    fd = HUD_DIMENSIONS,
                    bc = team_color[Player.players[0].team],
                    bw = HUD_BW,
                    br = HUD_BR,
                    to = HUD_TEXT_OFFSET
                )
            )
            HUD.labels.append(
                px.Label(
                    screen,
                    Player.players[1].name,
                    HUD_TEXT_SIZE,
                    (HUD_SIDE_DISTANCE[0], WIN_HEIGHT - HUD_SIDE_DISTANCE[1]),
                    "bottomleft",
                    f = HUD_FONT,
                    bgc = Player.players[1].color,
                    fd = HUD_DIMENSIONS,
                    bc = team_color[Player.players[1].team],
                    bw = HUD_BW,
                    br = HUD_BR,
                    to = HUD_TEXT_OFFSET
                )
            )
            HUD.labels.append(
                px.Label(
                    screen,
                    Player.players[2].name,
                    HUD_TEXT_SIZE,
                    (WIN_WIDTH - HUD_SIDE_DISTANCE[0], HUD_SIDE_DISTANCE[1]),
                    "topright",
                    f = HUD_FONT,
                    bgc = Player.players[2].color,
                    fd = HUD_DIMENSIONS,
                    bc = team_color[Player.players[2].team],
                    bw = HUD_BW,
                    br = HUD_BR,
                    to = HUD_TEXT_OFFSET
                )
            )
            HUD.labels.append(
                px.Label(
                    screen,
                    Player.players[3].name,
                    HUD_TEXT_SIZE,
                    (WIN_WIDTH - HUD_SIDE_DISTANCE[0], WIN_HEIGHT -  HUD_SIDE_DISTANCE[1]),
                    "bottomright",
                    f = HUD_FONT,
                    bgc = Player.players[3].color,
                    fd = HUD_DIMENSIONS,
                    bc = team_color[Player.players[3].team],
                    bw = HUD_BW,
                    br = HUD_BR,
                    to = HUD_TEXT_OFFSET
                )
            )
        
    def goal_team_1():
        pass

    def goal_team_2():
        pass

    def draw():
        for label in HUD.labels:
            label.draw()
