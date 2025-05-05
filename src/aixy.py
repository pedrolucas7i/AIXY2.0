"""
===============================================================================================================================================================
===============================================================================================================================================================

                                                                   _      ___  __  __ __   __  ____         ___  
                                                                  / \    |_ _| \ \/ / \ \ / / |___ \       / _ \ 
                                                                 / _ \    | |   \  /   \ V /    __) |     | | | |
                                                                / ___ \   | |   /  \    | |    / __/   _  | |_| |
                                                               /_/   \_\ |___| /_/\_\   |_|   |_____| (_)  \___/ 

                                                               
                                                                            COMPUTER AIXY 2.0 CODE
                                                                            by Pedro Ribeiro Lucas
                                                                                                                  
===============================================================================================================================================================
===============================================================================================================================================================
"""

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

""" ONLY MANUAL CONTROL"""
ONLY_MANUAL_CONTROL=False


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
    from time import sleep

    if 'forward' in direction:
        hardware.drive_forward()
    elif 'backward' in direction:
        hardware.drive_backward()
    elif 'left' in direction:
        hardware.drive_left()
    elif 'right' in direction:
        hardware.drive_right()
    elif 'finded' in direction:
        hardware.clamp_catch()
    
    sleep(0.35)


def manualControl():
    # === Manual joystick control using Xbox360 controller ===
    # === Handles axis interpretation and sends clean commands to hardware ===

    from time import sleep
    import pygame
    import hardware
    import xbox360_controller

    pygame.init()
    clock = pygame.time.Clock()
    controller = xbox360_controller.Controller()

    prev_command = None  # Store last command sent to avoid repeats

    try:
        while True:
            pygame.event.pump()  # Update internal pygame state

            # Get joystick axes
            a, y = controller.get_left_stick()
            x, b = controller.get_right_stick()

            # Deadzone filter
            threshold = 0.2
            x = x if abs(x) > threshold else 0
            y = y if abs(y) > threshold else 0

            # Decide movement command
            if x == 0 and y == 0:
                command = "drive_release"
            elif abs(x) > abs(y):
                command = "drive_left" if x < 0 else "drive_right"
            else:
                command = "drive_forward" if y < 0 else "drive_backward"

            # Send command only if it's different from the last one
            if command != prev_command:
                getattr(hardware, command)()  # Call hardware.drive_*
                prev_command = command

            sleep(0.1)  # Lowered delay to improve responsiveness
            clock.tick(30)  # Prevent CPU overuse

    except KeyboardInterrupt:
        print("Manual control stopped by user.")
    finally:
        pygame.quit()


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
    if ONLY_MANUAL_CONTROL:
        manualControl()
    else:
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