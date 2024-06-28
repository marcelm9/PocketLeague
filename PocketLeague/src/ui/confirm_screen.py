import pygame
import PygameXtras as px

from ..classes.controller_manager import ControllerManager
from ..files.colors import SOFT_WHITE


class ConfirmScreen:

    __screen: pygame.Surface
    __clock: pygame.time.Clock

    def init(screen: pygame.Surface, fpsclock: pygame.time.Clock):
        ConfirmScreen.__screen = screen
        ConfirmScreen.__clock = fpsclock

    def ask(question: str) -> bool:

        c = px.PSVG._PSVG__color
        px.PSVG.set_color((0, 0, 0))

        q_label = px.Label(
            None,
            question,
            50,
            (0, 0),
            f="Comic Sans",
        )

        rect = pygame.Rect(0, 0, max(1100, q_label.rect.width), 300)
        rect.center = ConfirmScreen.__screen.get_rect().center
        q_label.update_pos((rect.width // 2, rect.height // 2 - 55))

        surface = pygame.Surface((rect.width, rect.height))

        confirm_label = px.Label(
            None,
            "Confirm",
            40,
            (
                rect.width // 2 - 50,
                rect.height // 2 + 70,
            ),
            "midright",
            tc=(0, 0, 0),
            f="Comic Sans",
        )

        cancel_label = px.Label(
            None,
            "Cancel",
            40,
            (
                rect.width // 2 + 250,
                rect.height // 2 + 70,
            ),
            "midleft",
            tc=(0, 0, 0),
            f="Comic Sans",
        )

        # darken screen
        ConfirmScreen.__screen.fill((50, 50, 50), special_flags=pygame.BLEND_MULT)

        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            pressed = ControllerManager.get_pressed_by_everyone()
            if pressed[2]:
                px.PSVG.set_color(c)
                return True
            elif pressed[4]:
                px.PSVG.set_color(c)
                return False

            surface.fill(SOFT_WHITE)
            q_label.draw_to(surface)
            confirm_label.draw_to(surface)
            cancel_label.draw_to(surface)
            px.PSVG.down(
                surface,
                (confirm_label.left - 200, confirm_label.center[1]),
            )
            px.PSVG.slash(
                surface,
                (confirm_label.left - 130, confirm_label.center[1]),
            )
            px.PSVG.cross(
                surface,
                (confirm_label.left - 60, confirm_label.center[1]),
            )
            px.PSVG.right(
                surface,
                (cancel_label.left - 200, cancel_label.center[1]),
            )
            px.PSVG.slash(
                surface,
                (cancel_label.left - 130, cancel_label.center[1]),
            )
            px.PSVG.circle(
                surface,
                (cancel_label.left - 60, cancel_label.center[1]),
            )

            pygame.draw.rect(surface, (0, 0, 0), (0, 0, rect.width, rect.height), 5, 1)
            ConfirmScreen.__screen.blit(surface, rect)

            pygame.display.flip()
            ConfirmScreen.__clock.tick(60)
