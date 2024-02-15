import pygame
import PygameXtras as px
from ..files.config import FPS, CENTER, CONTROLLERS_NEEDED
from ..files.colors import SOFT_WHITE

class ControllerManager:

    screen: pygame.Surface
    fpsclock: pygame.time.Clock
    controllers: list[px.PlayStationController] = []
    
    def init(screen: pygame.Surface, fpsclock: pygame.time.Clock):
        ControllerManager.screen = screen
        ControllerManager.fpsclock = fpsclock

    def enough_controllers():
        """
        Always has to be called before taking input from a controller
        """
        if pygame.joystick.get_count() < CONTROLLERS_NEEDED:

            label1 = px.Label(ControllerManager.screen, f"Please connect {CONTROLLERS_NEEDED} controllers", 50, CENTER, "midbottom", f="Comic Sans", tc=SOFT_WHITE)
            label2 = px.Label(ControllerManager.screen, f"Currently connected: {pygame.joystick.get_count()}", 50, CENTER, "midtop", f="Comic Sans", tc=SOFT_WHITE)

            run = True
            while run:
                event_list = pygame.event.get()
                for event in event_list:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                
                if pygame.joystick.get_count() == CONTROLLERS_NEEDED:
                    run = False

                ControllerManager.screen.fill((50, 30, 30))
                label1.draw()
                label2.draw()
                
                pygame.display.flip()
                ControllerManager.fpsclock.tick(FPS)

    def declare_controllers():
        ControllerManager.controllers.clear()
        for i in range(CONTROLLERS_NEEDED):
            ControllerManager.controllers.append(
                px.PlayStationController(i)
            )

    def someone_pressed_x_or_down():
        ControllerManager.enough_controllers()
        for c in ControllerManager.controllers:
            c.update()
            if c.cross or c.arrow_down:
                return True
        return False
