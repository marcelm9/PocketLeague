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
    
    def get_pressed_by_everyone():
        # bools for the following values in the following order:
        # [confirm, up, down, left, right]
        buttons = [False for _ in range(5)]
        for c in ControllerManager.controllers:
            c.update()
            if c.l1 or c.r1:
                buttons[0] = True
            if c.arrow_up or c.triangle:
                buttons[1] = True
            if c.arrow_down or c.cross:
                buttons[2] = True
            if c.arrow_left or c.square:
                buttons[3] = True
            if c.arrow_right or c.circle:
                buttons[4] = True
        return buttons

    def get_controller_count():
        return len(ControllerManager.controllers)

    def get_pressed_by(controller_index: int, controller_input_side: str):
        assert controller_index in [0, 1]
        assert controller_input_side in ["left", "right"]

        if controller_index >= ControllerManager.get_controller_count():
            return [False for _ in range(5)]
        c = ControllerManager.controllers[controller_index]
        c.update()
        if controller_input_side == "left":
            return [
                c.l1,
                c.arrow_up,
                c.arrow_down,
                c.arrow_left,
                c.arrow_right
            ]
        elif controller_input_side == "right":
            return [
                c.r1,
                c.triangle,
                c.cross,
                c.square,
                c.circle
            ]
