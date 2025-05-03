import pygame
import xbox360_controller
import tank
import utils
from time import sleep

def manualControl():
    pygame.init()

    try:
        controller = xbox360_controller.Controller()
        while True:
            pygame.event.get()
            a, y = controller.get_left_stick()
            x, b = controller.get_right_stick()
            if x < 0:
                utils.drive('left', 2)
            elif x > 0:
                utils.drive('right', 2)
            elif y < 0:
                utils.drive('forward', 2)
            elif y > 0:
                utils.drive('backward', 1)

    except KeyboardInterrupt:
        print("\nEncerrando...")
