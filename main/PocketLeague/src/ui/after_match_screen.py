import sys

import pygame
import PygameXtras as px

from ..classes.match_stats import MatchStats
from ..classes.player_config_manager import PlayerConfigManager
from ..files.colors import SOFT_WHITE
from ..files.config import AFTER_MATCH_SCREEN_SIZE, CENTER, TEAM_COLOR_MAP


class AfterMatchScreen:

    __screen: pygame.Surface
    __fpsclock: pygame.time.Clock

    __surface = pygame.Surface(AFTER_MATCH_SCREEN_SIZE)
    __rect = __surface.get_rect()
    __rect.center = CENTER

    def init(fpsclock, screen):
        AfterMatchScreen.__fpsclock = fpsclock
        AfterMatchScreen.__screen = screen

    def show():

        table = px.Table(
            AfterMatchScreen.__surface,
            (
                AfterMatchScreen.__surface.get_width() // 2,
                AfterMatchScreen.__surface.get_height() // 2,
            ),
            (6, 1 + len(PlayerConfigManager.get_player_configs())),
            (190, 100),
        )

        stats = MatchStats.get_player_stats()
        configs = sorted(sorted(PlayerConfigManager.get_player_configs(), key = lambda x: stats[x.name].get_points(), reverse = True), key = lambda x: x.team, reverse = MatchStats.get_goals_team_orange() > MatchStats.get_goals_team_blue())
        font = "Comic Sans"
        fw, fh = 300, 80

        l_player_names = [
            px.Label(
                AfterMatchScreen.__surface,
                player.name,
                30,
                table.get((0, i)),
                tc=SOFT_WHITE,
                fd=(fw, fh),
                bgc=TEAM_COLOR_MAP[player.team],
                f=font,
            )
            for i, player in enumerate(configs, 1)
        ]

        l_headers = [
            px.Label(
                AfterMatchScreen.__surface,
                name,
                30,
                (table.get((i, 0))[0], table.get((i, 0))[1] + 10),
                tc=SOFT_WHITE,
                f=font,
            )
            for i, name in enumerate(
                ["Points", "Goals", "Assists", "Saves", "Shots"], 1
            )
        ]

        stat_labels = []
        for i, player in enumerate(configs, 1):
            stat_labels.append(
                px.Label(
                    AfterMatchScreen.__surface,
                    stats[player.name].get_points(),
                    30,
                    table.get((1, i)),
                    tc=SOFT_WHITE,
                    fd=(fw, fh),
                    bgc=TEAM_COLOR_MAP[player.team],
                    f=font,
                )
            )
            stat_labels.append(
                px.Label(
                    AfterMatchScreen.__surface,
                    stats[player.name].goals,
                    30,
                    table.get((2, i)),
                    tc=SOFT_WHITE,
                    fd=(fw, fh),
                    bgc=TEAM_COLOR_MAP[player.team],
                    f=font,
                )
            )
            stat_labels.append(
                px.Label(
                    AfterMatchScreen.__surface,
                    stats[player.name].assists,
                    30,
                    table.get((3, i)),
                    tc=SOFT_WHITE,
                    fd=(fw, fh),
                    bgc=TEAM_COLOR_MAP[player.team],
                    f=font,
                )
            )
            stat_labels.append(
                px.Label(
                    AfterMatchScreen.__surface,
                    stats[player.name].saves,
                    30,
                    table.get((4, i)),
                    tc=SOFT_WHITE,
                    fd=(fw, fh),
                    bgc=TEAM_COLOR_MAP[player.team],
                    f=font,
                )
            )
            stat_labels.append(
                px.Label(
                    AfterMatchScreen.__surface,
                    stats[player.name].shots,
                    30,
                    table.get((5, i)),
                    tc=SOFT_WHITE,
                    fd=(fw, fh),
                    bgc=TEAM_COLOR_MAP[player.team],
                    f=font,
                )
            )

        if MatchStats.get_goals_team_blue() > MatchStats.get_goals_team_orange():
            winner_name = "Blue"
            winner_color = TEAM_COLOR_MAP["Team Blue"]
        elif MatchStats.get_goals_team_orange() > MatchStats.get_goals_team_blue():
            winner_name = "Orange"
            winner_color = TEAM_COLOR_MAP["Team Orange"]
        else:
            raise Exception("This should not happen")

        winning_team_label = px.Label(
            AfterMatchScreen.__surface,
            f"{winner_name} won!",
            130,
            (
                AfterMatchScreen.__surface.get_width() // 2,
                50 - 24 * (len(configs) - 2),
            ),
            "midtop",
            tc=winner_color,
            f=font,
        )

        play_again_label = px.Label(
            AfterMatchScreen.__surface,
            "Play again",
            50,
            (
                AfterMatchScreen.__surface.get_width() // 2 - 300 + 110,
                AfterMatchScreen.__surface.get_height() - 50,
            ),
            "midbottom",
            tc=SOFT_WHITE,
            f="Comic Sans",
        )

        main_menu_label = px.Label(
            AfterMatchScreen.__surface,
            "Main Menu",
            50,
            (
                AfterMatchScreen.__surface.get_width() // 2 + 300 + 110,
                AfterMatchScreen.__surface.get_height() - 50,
            ),
            "midbottom",
            tc=SOFT_WHITE,
            f="Comic Sans",
        )

        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # draw gray background
            pygame.draw.rect(
                AfterMatchScreen.__surface,
                (50, 50, 50),
                (0, 0, AfterMatchScreen.__rect.width, AfterMatchScreen.__rect.height),
                0,
                15,
            )

            winning_team_label.draw()

            for l in l_headers + stat_labels + l_player_names:
                l.draw()

            play_again_label.draw()
            main_menu_label.draw()
            px.PSVG.right(
                AfterMatchScreen.__surface,
                (play_again_label.left - 200, play_again_label.center[1]),
            )
            px.PSVG.slash(
                AfterMatchScreen.__surface,
                (play_again_label.left - 130, play_again_label.center[1]),
            )
            px.PSVG.circle(
                AfterMatchScreen.__surface,
                (play_again_label.left - 60, play_again_label.center[1]),
            )
            px.PSVG.down(
                AfterMatchScreen.__surface,
                (main_menu_label.left - 200, main_menu_label.center[1]),
            )
            px.PSVG.slash(
                AfterMatchScreen.__surface,
                (main_menu_label.left - 130, main_menu_label.center[1]),
            )
            px.PSVG.cross(
                AfterMatchScreen.__surface,
                (main_menu_label.left - 60, main_menu_label.center[1]),
            )

            # draw white outline
            pygame.draw.rect(
                AfterMatchScreen.__surface,
                (255, 255, 255),
                (0, 0, AfterMatchScreen.__rect.width, AfterMatchScreen.__rect.height),
                5,
                15,
            )

            AfterMatchScreen.__screen.blit(
                AfterMatchScreen.__surface, AfterMatchScreen.__rect
            )
            pygame.display.flip()
            AfterMatchScreen.__fpsclock.tick(60)
