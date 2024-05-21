import sys
import pygame
import PygameXtras as px

from ..files.colors import SOFT_WHITE

from ..classes.player_stats import PlayerStats

from ..classes.match_stats import MatchStats

from ..classes.player_config_manager import PlayerConfigManager

from ..files.config import AFTER_MATCH_SCREEN_SIZE, CENTER


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

        configs = PlayerConfigManager.get_player_configs()

        l_player_names = [
            px.Label(
                AfterMatchScreen.__surface,
                name,
                30,
                table.get((0, i)),
                tc=SOFT_WHITE,
                f="Verdana",
            )
            for i, name in enumerate([player.name for player in configs], 1)
        ]

        l_headers = [
            px.Label(
                AfterMatchScreen.__surface,
                name,
                30,
                (table.get((i, 0))[0], table.get((i, 0))[1] + 10),
                tc=SOFT_WHITE,
                f="Verdana",
            )
            for i, name in enumerate(
                ["Points", "Goals", "Assists", "Saves", "Shots"], 1
            )
        ]

        stat_labels = []
        stats = MatchStats.get_player_stats()
        for i, player in enumerate([player.name for player in configs], 1):
            stat_labels.append(
                px.Label(
                    AfterMatchScreen.__surface,
                    stats[player].get_points(),
                    30,
                    table.get((1, i)),
                    tc=SOFT_WHITE,
                    f="Verdana",
                )
            )
            stat_labels.append(
                px.Label(
                    AfterMatchScreen.__surface,
                    stats[player].goals,
                    30,
                    table.get((2, i)),
                    tc=SOFT_WHITE,
                    f="Verdana",
                )
            )
            stat_labels.append(
                px.Label(
                    AfterMatchScreen.__surface,
                    stats[player].assists,
                    30,
                    table.get((3, i)),
                    tc=SOFT_WHITE,
                    f="Verdana",
                )
            )
            stat_labels.append(
                px.Label(
                    AfterMatchScreen.__surface,
                    stats[player].saves,
                    30,
                    table.get((4, i)),
                    tc=SOFT_WHITE,
                    f="Verdana",
                )
            )
            stat_labels.append(
                px.Label(
                    AfterMatchScreen.__surface,
                    stats[player].shots,
                    30,
                    table.get((5, i)),
                    tc=SOFT_WHITE,
                    f="Verdana",
                )
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

            AfterMatchScreen.__surface.fill((30, 30, 30))
            for l in l_headers + l_player_names + stat_labels:
                l.draw()

            AfterMatchScreen.__screen.blit(
                AfterMatchScreen.__surface, AfterMatchScreen.__rect
            )
            pygame.display.flip()
            AfterMatchScreen.__fpsclock.tick(60)
