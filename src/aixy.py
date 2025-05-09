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

import env

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


def decide():
    """ Decide the action of AIXY based in camera image"""

    if env.CAMERA_USB:
        from camera import CameraUSB
        camera = CameraUSB()
    else:
        from camera import Camera
        camera = Camera()
    
    decision = llm.get(
        env.OLLAMA_VISION_MODEL,
        """
        Analyze the received image and determine the best action for a mobile robot based on the visible environment. Choose only one of the following words as output:

        'forward'
        'slow forward'
        'fast forward'
        'left'
        'right'
        'left fast'   (default decision to avoid colisions and obstacules)
        'right fast'
        'left very fast'
        'right very fast'
        'left hiper fast'
        'right hiper fast'

        Decide based on the following principles:

        Avoid collisions: Never select a direction that would lead the robot into an obstacle.
        Optimize the route: Prioritize paths that lead the robot to its destination in the most efficient and safe manner.
        Avoid being stationary: The robot should keep moving whenever it is safe and feasible.
        Minimize 'backward' usage: The camera does not cover this area, making this option less reliable and recommended only when no other safe solution exists.
        Adjust speed to the environment: In open areas, increase speed; in tight spaces, slow down.
        Provide only one word as a response, with no additional explanations.
        """,
        camera.get_frame() if CAMERA else None
    )
    
    print(f"Decided: {decision}")
    return decision


def find(thing):
    """ Decide the action of AIXY based in camera image and the thing to search"""
    
    if env.CAMERA_USB:
        from camera import CameraUSB
        camera = CameraUSB()
    else:
        from camera import Camera
        camera = Camera()

    decision = llm.get(
        env.OLLAMA_VISION_MODEL, F"""
        Analyze the received image and determine the best action for a mobile robot to locate and reach the object called: '{thing}'. Once the object is clearly identified and the robot is within 10 centimeters of it, respond only with the word:

        'finded'

        Otherwise, choose and respond with only one of the following action words to guide the robot:

        'forward'
        'slow forward'
        'fast forward'
        'left'
        'right'
        'left fast' (default to avoid collisions and obstacles)
        'right fast'
        'left very fast'
        'right very fast'
        'left hiper fast'
        'right hiper fast'

        Decision principles:

        Find the object: Prioritize paths that move toward the object '{thing}'.

        Confirm proximity: When the object is visually confirmed and estimated to be within 10 cm, return only 'finded'.

        Avoid collisions: Never choose a direction that would result in hitting an obstacle.

        Keep moving: Do not stop unless the object is found.

        Adjust speed: In open areas, prefer faster speeds; in tight or cluttered areas, go slower.

        One-word output only: Return only the chosen word — no explanations or additional text.

        """,
        camera.get_frame() if CAMERA else None
    )
    
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

            # Get joystick axes and pad buttons
            ax, y = controller.get_left_stick()
            x, by = controller.get_right_stick()
            up, right, down, left = controller.get_pad()

            A, B, X, Y, LEFT_BUMP, RIGHT_BUMP, BACK, START, NONE, LEFT_STICK_BTN, RIGHT_STICK_BTN = controller.get_buttons()

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

            if up == 1:
                command = "arm_up"
            elif down == 1:
                command = "arm_down"

            if LEFT_BUMP == 1:
                command = "clamp_catch"
            elif RIGHT_BUMP == 1:
                command = "clamp_release"

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
        if env.MOTORS:
            import hardware

            if manual_mode:
                manualControl()
                continue  # Skip AI processing while in manual mode

            # If OA is defined as true, and the distance to the ultrassonic sensor is more than 8cm, AIXY think and execute the decision, if not, avoid Obstacle, if OA is not set as true (false) just think and execute the action
            if env.OA:
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
        "You are AIXY an AI assistant that responds clearly and efficiently.\n"
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

    if env.TTS:
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

            if env.TTS:
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


def WCS_thread():
    from flask import Flask, render_template, Response
    import env

    if env.CAMERA:
        from camera import CameraUSB
        camera = CameraUSB()

    if env.MOTORS:
        import hardware


    #Initialize the Flask app
    app = Flask(__name__, template_folder="./WCS_thread/webserver", static_folder="./WCS_thread/static")

    @app.route('/')
    def index():
        return render_template('index.html', camera=env.CAMERA)

    if env.MOTORS:
        @app.route('/forward')
        def forward():
            hardware.drive_forward()
            return render_template('index.html', camera=env.CAMERA)

        @app.route('/left')
        def left():
            hardware.drive_left()
            return render_template('index.html', camera=env.CAMERA)

        @app.route('/right')
        def right():
            hardware.drive_right()
            return render_template('index.html', camera=env.CAMERA)

        @app.route('/backward')
        def backward():
            hardware.drive_backward()
            return render_template('index.html', camera=env.CAMERA)

        @app.route('/release')
        def release():
            hardware.drive_release()
            return render_template('index.html', camera=env.CAMERA)

    if env.CAMERA:
        @app.route('/stream')
        def stream():
            return Response(camera.get_web_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def run():
        app.run(debug=True, port=9900, host="0.0.0.0")

    run()

"""
===========================================================================================================================================
===========================================================================================================================================
                                                                MAIN AIXY2.0 CODE
===========================================================================================================================================
===========================================================================================================================================
"""
    

def main():
    import threading
    import env

    if env.ONLY_MANUAL_CONTROL:
        MC_PROCESSOR = threading.Thread(target=manualControl, daemon=True)
        MC_PROCESSOR.start()
    else:

        if env.LVMAD:
            print("🟢 Starting Large Vision Model Autonomous Drive thread...")
            LVMAD_PROCESSOR = threading.Thread(target=LVMAD_thread, args=(thingToSearch, additionalPrompt), daemon=True)
            LVMAD_PROCESSOR.start()


    if env.LLMAC:
        print("🟢 Starting Large Languade Model Autonomous Conversation thread...")
        LLMAC_PROCESSOR = threading.Thread(target=LLMAC_thread, daemon=True)
        LLMAC_PROCESSOR.start()
    

    if env.SBM:
        print("🟢 Starting Switch Between Modes thread...")
        SBM_PROCESSOR = threading.Thread(target=SBM_thread, daemon=True)
        SBM_PROCESSOR.start()


    if env.WCS:
        print("🟢 Starting Web Camera Stream thread...")
        WCS_thread()