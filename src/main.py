import threading
import logging
import time
import pygame
import controller
import vision
import utils
import conversation
import brain
import webserver
import tts
import env

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable to switch between AI and manual mode
manual_mode = False

# Function to handle autonomous driving
def drive(thing, localization=None):
    while True:
        if manual_mode:
            controller.manualControl()
            continue  # Skip AI processing while in manual mode

        utils.verifyObstacules()

        if thing is None:
            decision = vision.decide().strip().strip("'").lower()
        else:
            decision = vision.find(thing, localization).strip().strip("'").lower()

        utils.drive(decision, utils.movements[decision].get('speed'))
        utils.calculatedWaitingTime(0.7)

# Function to handle conversation
def human_interaction():
    while True:
        conversation.commonConversations()

def joystick_listener():
    global manual_mode
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No controller connected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller connected: {joystick.get_name()}")

    while True:
        pygame.event.pump()
        xbox_button = joystick.get_button(8)

        if xbox_button:
            manual_mode = not manual_mode
            mode = "MANUAL" if manual_mode else "AUTONOMOUS"
            print(f"Switched to {mode} mode.")
            tts.speak(f"{mode} mode activated.")
            time.sleep(1.5)  # Prevent multiple toggles from one press
        else:
            time.sleep(0.05)  # When nothing happens wait (50ms)

def start_threads():
    # Start AI driving thread
    LVMAD_processor = threading.Thread(target=drive, args=(None, None), daemon=True)
    LVMAD_processor.start()
    

    # Start human interaction thread
    LLMAC_processor = threading.Thread(target=human_interaction, daemon=True)
    LLMAC_processor.start()

    # Start obstacle detection thread
    OA_processor = threading.Thread(target=utils.verifyObstacules, daemon=True)
    OA_processor.start()

    # Start Xbox controller switcher mode listener
    SBM_processor = threading.Thread(target=joystick_listener, daemon=True)
    SBM_processor.start()

    # Start Web Camera Stream to can be seen the image of camera in others devices
    WCS_processor = threading.Thread(target=webserver.run, daemon=True)
    WCS_processor.start()

def main():
    print(f"AIXY (V{env.AIXY_SOFTWARE_VERSION}) ALIVE!!!")
    
    # Speak the first message
    tts.speak(env.FIRST_EN_MESSAGE)
    
    # Start other threads
    start_threads()

if __name__ == "__main__":
    main()