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
decision = None

if env.CAMERA:
    if env.CAMERA_USB:
        from camera import CameraUSB
        camera = CameraUSB()
        print("🟢 Using USB Camera")
    else:
        from camera import Camera
        camera = Camera()
        print("🟢 Using Raspberry Pi Camera")
"""
===========================================================================================================================================
===========================================================================================================================================
                                                LARGE VISION MODEL AUTONOMOUS DRIVE PROCESSOR CODE
===========================================================================================================================================
===========================================================================================================================================
"""


def decide():
    """ Decide the action of AIXY based in camera image"""
    global decision, camera
    import llm
    
    decision = llm.get(
        env.OLLAMA_VISION_MODEL,
        """
        Analyze the received image and determine the best action for a mobile robot based on the visible environment. Choose only one of the following words as output:

        'backward' (Try not use this, except in danger cases)
        'forward'
        'left' (Default decision to avoid colisions and obstacles)
        'right'

        Decide based on the following principles:

        Avoid collisions: Never select a direction that would lead the robot into an obstacle.
        Optimize the route: Prioritize paths that lead the robot to its destination in the most efficient and safe manner.
        Avoid being stationary: The robot should keep moving whenever it is safe and feasible.
        Minimize 'backward' usage: The camera does not cover this area, making this option less reliable and recommended only when no other safe solution exists.
        Adjust speed to the environment: In open areas, increase speed; in tight spaces, slow down.
        Provide only one word as a response, with no additional explanations.
        """,
        camera.get_frame()
    ).lower().strip()

    print(f"Decided: {decision}")
    return decision


def find(thing):
    """ Decide the action of AIXY based in camera image and the thing to search"""
    global decision, camera
    import llm

    decision = llm.get(
        env.OLLAMA_VISION_MODEL, f"""
        Analyze the received image and determine the best action for a mobile robot to locate and reach the object called: '{thing}'. Once the object is clearly identified and the robot is within 10 centimeters of it, respond only with the word:

        'finded'

        Otherwise, choose and respond with only one of the following action words to guide the robot:

        'backward' (Try not use this, except in danger cases)
        'forward'
        'left' (Default decision to avoid collisions and obstacles)
        'right'

        Decision principles:

        Find the object: Prioritize paths that move toward the object '{thing}'.

        Confirm proximity: When the object is visually confirmed and estimated to be within 10 cm, return only 'finded'.

        Avoid collisions: Never choose a direction that would result in hitting an obstacle.

        Keep moving: Do not stop unless the object is found.

        Adjust speed: In open areas, prefer faster speeds; in tight or cluttered areas, go slower.

        One-word output only: Return only the chosen word — no explanations or additional text.
        """,
        camera.get_frame()
    ).lower().strip()

    print(f"Decided: {decision}")
    return decision


def drive(direction):
    import hardware

    if not isinstance(direction, str):
        return
    elif 'forward' in direction:
        hardware.drive_forward()
    elif 'backward' in direction:
        hardware.drive_backward()
    elif 'left' in direction:
        hardware.drive_left()
    elif 'right' in direction:
        hardware.drive_right()
    elif 'finded' in direction:
        hardware.clamp_catch()
    hardware.drive_release()


def manualControl():
    # === Manual joystick control using Xbox360 controller ===
    # === Handles axis interpretation and sends clean commands to hardware ===

    from time import sleep
    import pygame
    import hardware
    import xbox360_controller

    global decision

    pygame.init()
    clock = pygame.time.Clock()
    controller = xbox360_controller.Controller()

    prev_command = None

    try:
        while True:
            pygame.event.pump()

            ax, y = controller.get_left_stick()
            x, by = controller.get_right_stick()
            up, right, down, left = controller.get_pad()

            A, B, X, Y, LB, RB, BACK, START, _, LSB, RSB = controller.get_buttons()

            threshold = 0.2
            x = x if abs(x) > threshold else 0
            y = y if abs(y) > threshold else 0

            if x == 0 and y == 0:
                command = "drive_release"
            elif abs(x) > abs(y):
                command = "drive_left" if x < 0 else "drive_right"
            else:
                command = "drive_forward" if y < 0 else "drive_backward"

            if up == 1:
                hardware.arm_up()
            elif down == 1:
                hardware.arm_down()

            if LB == 1:
                hardware.clamp_catch()
            elif RB == 1:
                hardware.clamp_release()

            if command != prev_command:
                getattr(hardware, command)()
                prev_command = command

            if command == "drive_left":
                decision = "left"
            elif command == "drive_right":
                decision = "right"
            elif command == "drive_forward":
                decision = "forward"
            elif command == "drive_backward":
                decision = "backward"

            sleep(0.1)
            clock.tick(30)

    except KeyboardInterrupt:
        print("Manual control stopped by user.")
    finally:
        pygame.quit()


def LVMAD_thread(thingToSearch=None):
    """Main thread for Large Vision Model Autonomous Drive."""
    import time
    import traceback

    try:
        if env.CAMERA_USB:
            from camera import CameraUSB
            camera = CameraUSB()
        else:
            from camera import Camera
            camera = Camera()
        if env.MOTORS:
            import hardware

        while True:
            if manual_mode:
                manualControl()
                continue

            handle_decision(thingToSearch)
            time.sleep(0.1)

    except Exception as e:
        print("Erro na thread LVMAD_thread:")
        traceback.print_exc()


def handle_decision(thingToSearch):
    """Handle decision-making logic."""
    decision = make_decision(thingToSearch)
    if decision is not None:
        drive(decision)
    else:
        print("No decision made.")


def make_decision(thingToSearch):
    """Make a decision based on the environment."""
    if thingToSearch is None:
        return decide()
    else:
        return find(thingToSearch)


"""
===========================================================================================================================================
===========================================================================================================================================
                                            LARGE LANGUAGE MODEL AUTONOMOUS CONVERSATION PROCESSOR CODE
===========================================================================================================================================
===========================================================================================================================================
"""


def generate_response(user_text):
    import env
    import llm
    from db import getConversations, getLastConversation, getLastAssistentConversation

    history = getConversations()
    last_entry = getLastConversation()
    last_exit = getLastAssistentConversation()

    prompt = "<|begin_of_text|>\n<|start_header_id|>system<|end_header_id|>\n"
    prompt += "You are AIXY, an advanced conversational AI created by Pedro Ribeiro Lucas.\n\n"
    prompt += F"- Purpose: {env.PURPOSE}\n"
    prompt += F"- Personality: {env.PERSONALITY}\n"
    prompt += "Your main goal is to maintain natural, friendly, and helpful conversations about any topic.\n\n"
    prompt += "Instructions:\n"
    prompt += "- Focus mainly on the user's last message and the immediately previous conversation to generate your response.\n"
    prompt += "- Give highest priority to the most recent user input and recent context; use older history only if directly relevant.\n"
    prompt += "- Detect if the topic has changed from previous messages; if yes, DO NOT associate the new topic with unrelated prior contexts.\n"
    prompt += "- DO NOT include your internal reasoning, thought process, or any explanations in your output.\n"
    prompt += "- Respond naturally, clearly, and concisely, avoiding any unnecessary or irrelevant content.\n"
    prompt += "<|eot_id|>\n"
    prompt += f"<|start_header_id|>user<|end_header_id|>\n{last_entry}\n<|eot_id|>\n"
    prompt += f"<|start_header_id|>assistant<|end_header_id|>\n{last_exit}\n<|eot_id|>\n"
    prompt += f"<|start_header_id|>user<|end_header_id|>\n{user_text}\n<|eot_id|>\n"
    prompt += "<|start_header_id|>assistant<|end_header_id|>\n"



    return llm.get(env.OLLAMA_LANGUAGE_MODEL, prompt)

def LLMAC_thread():
    import env
    import listener
    import speaker
    import commands
    import db

    while True:
        try:
            stt_data_raw = listener.transcribe_speech()
            if not stt_data_raw:
                print("No speech recognized.")
            else:

                print(f"> User said: {stt_data_raw}")

                if not (commands.executeCommand(stt_data_raw.lower())):
                    response = generate_response(stt_data_raw)
                    if response:
                        db.insertConversation(stt_data_raw, response)   # Save in DB
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
    import time

    global manual_mode

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
                speaker.speak(f"{mode} mode activated.")
            
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

import threading
import os
import pty
import socket
from flask import Flask, render_template, Response, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit
import env

child_fd = None

app = Flask(__name__, template_folder="./WCS_thread/webserver", static_folder="./WCS_thread/static")
app.secret_key = "aixy-secret"
socketio = SocketIO(app, async_mode='threading')

def find_camera_index(max_index=10):
    try:
        import cv2
        for idx in range(max_index):
            cap = cv2.VideoCapture(idx)
            if cap is not None and cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret:
                    return idx
        return None
    except Exception:
        return None

def WCS_thread():
    global manual_mode

    # ==================== CAMERA ====================
    camera = None
    if env.CAMERA:
        from camera import CameraUSB
        cam_idx = find_camera_index()
        if cam_idx is not None:
            camera = CameraUSB(cam_idx)
        else:
            camera = None

    # ==================== HARDWARE ====================
    if env.MOTORS:
        import hardware

    # ==================== ROUTES ====================
    @app.route('/')
    def index():
        return render_template('index.html', camera=env.CAMERA)

    @app.route('/shell')
    def terminal():
        return render_template('xterm.html')

    @app.route('/stream')
    def stream():
        if camera:
            return Response(camera.get_web_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
        return "Camera not enabled", 404

    @app.route('/control')
    def control():
        global manual_mode
        manual_mode = not manual_mode
        return render_template('index.html', camera=env.CAMERA)

    # ==================== MOTOR ROUTES ====================
    if env.MOTORS:
        @app.route('/forward')
        def forward():
            hardware.drive_forward()
            return redirect(url_for('index'))

        @app.route('/left')
        def left():
            hardware.drive_left()
            return redirect(url_for('index'))

        @app.route('/right')
        def right():
            hardware.drive_right()
            return redirect(url_for('index'))

        @app.route('/backward')
        def backward():
            hardware.drive_backward()
            return redirect(url_for('index'))

        @app.route('/release')
        def release():
            hardware.drive_release()
            return redirect(url_for('index'))

    # ==================== TERMINAL SHELL ====================
    def read_and_emit_output(fd):
        while True:
            try:
                data = os.read(fd, 1024).decode()
                if data:
                    socketio.emit('shell_output', data)
                else:
                    break
            except OSError:
                break

    @socketio.on('connect')
    def start_terminal(auth=None):
        import sys

        class WebLogger:
            def __init__(self, socketio):
                self.socketio = socketio

            def write(self, message):
                if message:
                    self.socketio.emit('shell_output', message)

            def flush(self):
                pass

        class TeeLogger:
            def __init__(self, *targets):
                self.targets = targets

            def write(self, message):
                for t in self.targets:
                    t.write(message)

            def flush(self):
                for t in self.targets:
                    t.flush()

        sys.stdout = TeeLogger(sys.stdout, WebLogger(socketio))
        sys.stderr = TeeLogger(sys.stderr, WebLogger(socketio))

        global child_fd
        if child_fd:
            os.close(child_fd)
            child_fd = None
        pid, child_fd = pty.fork()
        if pid == 0:
            os.execvp("bash", ["bash"])
        else:
            threading.Thread(target=read_and_emit_output, args=(child_fd,), daemon=True).start()

    @socketio.on('shell_input')
    def handle_terminal_input(data):
        global child_fd
        if child_fd:
            try:
                os.write(child_fd, data.encode())
            except OSError as e:
                socketio.emit('shell_output', f"Erro: {str(e)}\n")

    # ===================== AI =====================
    @socketio.on('aiquestion')
    def handle_pergunta_robo(question):
        try:
            import db
            import commands
            import speaker

            if not (commands.executeCommand(question.lower())):
                response = generate_response(question)
                if response:
                    db.insertConversation(question, response)
                else:
                    print("No response generated.")
            else:
                response = "Command executed!"
            
            speaker.speak(response) if env.TTS else None
            socketio.emit('airesponse', response)
        except Exception as e:
            socketio.emit('airesponse', f"[Error] {str(e)}")

    # ==================== JOYSTICK VIA SOCKETIO ====================
    if env.MOTORS:
        @socketio.on('joystick_manual')
        def handle_joystick_manual(data):
            action = data.get("action")
            arm = data.get("arm")
            clamp = data.get("clamp")
            
            if action:
               drive(action)
            if arm:
                if arm == "up":
                    hardware.arm_up()
                elif arm == "down":
                    hardware.arm_down()

            if clamp:
                if clamp == "close":
                    hardware.clamp_catch()
                elif clamp == "open":
                    hardware.clamp_release()

            socketio.emit("joystick_manual_ack", {"status": "ok"})

    # ==================== RUN ====================
    socketio.run(app, debug=False,  allow_unsafe_werkzeug=True, use_reloader=False, port=9900, host="0.0.0.0")

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
            LVMAD_PROCESSOR = threading.Thread(target=LVMAD_thread, daemon=False)
            LVMAD_PROCESSOR.start()


    if env.LLMAC:
        print("🟢 Starting Large Language Model Autonomous Conversation thread...")
        LLMAC_PROCESSOR = threading.Thread(target=LLMAC_thread, daemon=False)
        LLMAC_PROCESSOR.start()
    

    if env.SBM:
        print("🟢 Starting Switch Between Modes thread...")
        SBM_PROCESSOR = threading.Thread(target=SBM_thread, daemon=True)
        SBM_PROCESSOR.start()


    if env.WCS:
        print("🟢 Starting Web Camera Stream thread (Flask)...")
        WCS_PROCESSOR = threading.Thread(target=WCS_thread, daemon=False)
        WCS_PROCESSOR.start()
