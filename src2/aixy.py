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

""" Motors """
MOTORS = False

""" AIXY COMMANDS """
COMMANDS = False

# Variable used to define the actual mode
manual_mode = False

def decide(additionalPrompt=None):
    if additionalPrompt:
        decision = llm.get(env.OLLAMA_VISION_MODEL, env.OLLAMA_VISION_DECISION_PROMPT, camera.get_frame())
    else:
        decision = llm.get(env.OLLAMA_VISION_MODEL, env.OLLAMA_VISION_DECISION_PROMPT, camera.get_frame())
    print(f"Decided: {decision}")
    return decision

def find(thing, additionalPrompt=None):
    if additionalPrompt:
        decision = llm.get(env.OLLAMA_VISION_MODEL, None, camera.get_frame())
    else:
        decision = llm.get(env.OLLAMA_VISION_MODEL, None, camera.get_frame())
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
    while True:
        if manual_mode:
            manualControl()
            continue  # Skip AI processing while in manual mode

        utils.verifyObstacules()

        if thingToSearch is None:
            decision = decide(additionalPrompt).strip().strip("'").lower()
        else:
            decision = find(thing, additionalPrompt).strip().strip("'").lower()

        utils.drive(decision)
        utils.calculatedWaitingTime(0.7)