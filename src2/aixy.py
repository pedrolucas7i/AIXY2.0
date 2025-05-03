# aixy.py
# Author: Pedro Lucas
# Project: AIXY2.0

""" Large Vision Model Automonous Drive """
LVMAD = False 

""" Large Languade Model Autonomous Conversations """
LLMAC = False

""" Obstacle Avoidance """
OA = False

""" Switch Between Modes """
SBM = False

""" Web Camera Stream """
WCS = False

""" Text to Speech """
TTS = False

""" Speech to Text """
STT = False

""" AIXY COMMANDS """
COMMANDS = False

""" Motors """
MOTORS = False

""" Camera """
CAMERA = False

""" Camera Connection """
CAMERA_USB=True


# Variables
manual_mode = False
thingToSearch = None
additionalPrompt = None


def decide(additionalPrompt=None):
    """ Decide the action of AIXY based in camera image, and, if passed, the additional prompt"""

    if CAMERA_USB:
        from camera import CameraUSB
        camera = CameraUSB()
    else:
        from camera import Camera
        camera = Camera()
    
    camera = camera.CameraUSB()
    if additionalPrompt:
        decision = llm.get(env.OLLAMA_VISION_MODEL, env.OLLAMA_VISION_DECISION_PROMPT, camera.get_frame() if CAMERA else None)
    else:
        decision = llm.get(env.OLLAMA_VISION_MODEL, env.OLLAMA_VISION_DECISION_PROMPT, camera.get_frame() if CAMERA else None)
    
    print(f"Decided: {decision}")
    return decision


def find(thing, additionalPrompt=None):
    """ Decide the action of AIXY based in camera image and the thing to search, and, if passed, the additional prompt"""
    
    if CAMERA_USB:
        from camera import CameraUSB
        camera = CameraUSB()
    else:
        from camera import Camera
        camera = Camera()

    if additionalPrompt:
        decision = llm.get(env.OLLAMA_VISION_MODEL, None, camera.get_frame() if CAMERA else None)
    else:
        decision = llm.get(env.OLLAMA_VISION_MODEL, None, camera.get_frame() if CAMERA else None)
    
    print(f"Decided: {decision}")
    return decision


def drive(direction):
    import hardware

    if 'forward' in direction:
        hardware.drive_forward()
    elif 'backward' in direction:
        hardware.drive_backward()()
    elif 'left' in direction:
        hardware.drive_left()()
    elif 'right' in direction:
        hardware.drive_right()()
    elif 'finded' in direction:
        hardware.clamp_catch()
    
    sleep(0.35)
    hardware.drive_forward()


def manualControl():
    pygame.init()
    controller = xbox360_controller.Controller()
    while True:
        pygame.event.get()
        a, y = controller.get_left_stick()
        x, b = controller.get_right_stick()
        if x < 0:
            drive('left')
        elif x > 0:
            drive('right')
        elif y < 0:
            drive('forward')
        elif y > 0:
            drive('backward')


def LVMAD_thread(thingToSearch=None, additionalPrompt=None):
    import time
    while True:
        if MOTORS:
            import hardware

            if manual_mode:
                manualControl()
                continue  # Skip AI processing while in manual mode

            # If the distance to the ultrassonic sensor is more than 8cm, AIXY think and execute the decision, if not, avoid Obstacle
            if hardware.get_distance() > 8:
                if thingToSearch == None:
                    decision = decide(additionalPrompt).strip().strip("'").lower()
                else:
                    decision = find(thing, additionalPrompt).strip().strip("'").lower()
                
                drive(decision)
            else:
                hardware.drive_left()
        else:
            if thingToSearch == None:
                decision = decide(additionalPrompt).strip().strip("'").lower()
            else:
                decision = find(thing, additionalPrompt).strip().strip("'").lower()

        time.sleep(0.7)


def main():
    import threading

    if LVMAD:
        LVMAD_PROCESSOR = threading.Thread(target=LVMAD_thread, args=(thingToSearch, additionalPrompt), daemon=True)
        LVMAD_PROCESSOR.start()
