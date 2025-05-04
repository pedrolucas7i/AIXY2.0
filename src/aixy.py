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

"""
===========================================================================================================================================
===========================================================================================================================================
                                                LARGE VISION MODEL AUTONOMOUS DRIVE PROCESSOR CODE
===========================================================================================================================================
===========================================================================================================================================
"""


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

        # If MOTORS has set as true, use motors, if not, just print the decision without execute the action
        if MOTORS:
            import hardware

            if manual_mode:
                manualControl()
                continue  # Skip AI processing while in manual mode

            # If OA is defined as true, and the distance to the ultrassonic sensor is more than 8cm, AIXY think and execute the decision, if not, avoid Obstacle, if OA is not set as true (false) just think and execute the action
            if OA:
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
                
                drive(decision)
        else:
            if thingToSearch == None:
                decision = decide(additionalPrompt).strip().strip("'").lower()
            else:
                decision = find(thing, additionalPrompt).strip().strip("'").lower()

        time.sleep(0.7)


"""
===========================================================================================================================================
===========================================================================================================================================
                                            LARGE LANGUAGE MODEL AUTONOMOUS CONVERSATION PROCESSOR CODE
===========================================================================================================================================
===========================================================================================================================================
"""


def generate_response(user_text):
    import env
    prompt = (
        "You are an AI assistant that responds clearly and efficiently.\n"
        f"- Purpose: {env.PURPOSE}\n"
        f"- Personality: {env.PERSONALITY}\n"
        f"- Model: {env.OLLAMA_LANGUAGE_MODEL}\n"
        f"The user said: {user_text.strip()}\n\n"
        "Provide a direct and relevant response. Do not over-explain."
    )
    return llm.get(env.OLLAMA_LANGUAGE_MODEL, prompt)


def clean_text(text):
    text = re.sub(r'[.,!?]', '', text)
    text = text.strip().lower()
    text = re.sub(r'\s{2,}', ' ||| ', text)
    text = text.replace(' ', '')
    text = text.replace('|||', ' ')
    return re.sub(r'\s+', ' ', text).strip()


def LLMAC_thread():
    import env
    import listener
    import speaker

    try:
        stt_data_raw = ' '.join(listener.transcribe_speech())
        if not stt_data_raw:
            print("No speech recognized.")
            return

        else:

            cleaned_text = clean_text(stt_data_raw)
            print(f"> User said: {cleaned_text}")

            if cleaned_text in env.COMMANDS:
                commands.executeCommand(cleaned_text)
                return

            response = generate_response(cleaned_text)
            if response:
                speaker.speak(response)
            else:
                print("No response generated.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")


"""
===========================================================================================================================================
===========================================================================================================================================
                                                                SWITCH BETWEEN MODES
===========================================================================================================================================
===========================================================================================================================================
"""


def SBM_thread():
    import pygame

    if TTS:
        import speaker

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

            if TTS:
                tts.speak(f"{mode} mode activated.")
            
            time.sleep(1.5)  # Prevent multiple toggles from one press
        else:
            time.sleep(0.05)  # When nothing happens wait (50ms)


"""
===========================================================================================================================================
===========================================================================================================================================
                                                                WEB CAMERA STREAM
===========================================================================================================================================
===========================================================================================================================================
"""
    

def main():
    import threading
    import WCS_thread

    if LVMAD:
        print("🟢 Starting Large Vision Model Autonomous Drive thread...")
        LVMAD_PROCESSOR = threading.Thread(target=LVMAD_thread, args=(thingToSearch, additionalPrompt), daemon=True)
        LVMAD_PROCESSOR.start()


    if LLMAC:
        print("🟢 Starting Large Languade Model Autonomous Conversation thread...")
        LLMAC_PROCESSOR = threading.Thread(target=LLMAC_thread, daemon=True)
        LLMAC_PROCESSOR.start()
    

    if SBM:
        print("🟢 Starting Switch Between Modes thread...")
        SBM_PROCESSOR = threading.Thread(target=SBM_thread, daemon=True)
        SBM_PROCESSOR.start()


    if WCS:
        print("🟢 Starting Web Camera Stream thread...")
        WCS_PROCESSOR = threading.Thread(target=WCS_thread.run(), daemon=True)
        WCS_PROCESSOR.start()



main()
