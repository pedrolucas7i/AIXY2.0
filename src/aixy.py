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

"""
===========================================================================================================================================
===========================================================================================================================================
                                                LARGE VISION MODEL AUTONOMOUS DRIVE PROCESSOR CODE
===========================================================================================================================================
===========================================================================================================================================
"""


def decide():
    """ Decide the action of AIXY based in camera image"""
    global decision
    import llm

    if env.CAMERA_USB:
        from camera import CameraUSB
        camera = CameraUSB()
    else:
        from camera import Camera
        camera = Camera()
    
    decision = llm.get(
        env.OLLAMA_VISION_MODEL,
        """
        Analyze the received image and decide the best single action for a mobile robot in the environment.  
        Respond ONLY with one of these four words: backward, forward, left, right. No explanations, no punctuation.

        Rules:
        - Avoid collisions: Never choose a direction leading directly into an obstacle. Obstacles include any visible physical object blocking the path.
        - Prioritize safety over efficiency.
        - Avoid being stationary: move forward, left, or right whenever safe.
        - Use 'backward' only if no other safe option exists because the rear camera coverage is limited.
        - When possible, favor 'left' to avoid obstacles.
        - Speed control is handled separately and should not be included in this response.

        """,
        camera.get_frame() if env.CAMERA else None
    ).lower()
    
    print(f"Decided: {decision}")
    return decision


def find(thing):
    """ Decide the action of AIXY based in camera image and the thing to search"""
    global decision
    import llm

    if env.CAMERA_USB:
        from camera import CameraUSB
        camera = CameraUSB()
    else:
        from camera import Camera
        camera = Camera()

    decision = llm.get(
        env.OLLAMA_VISION_MODEL, F"""
        Analyze the received image and determine the best single action for a mobile robot to locate and reach the object called '{thing}'.

        Respond ONLY with one of these words:
        - 'finded' (when the object is clearly identified and the robot is within 10 centimeters)
        - or one of these actions: 'backward', 'forward', 'left', 'right'

        No explanations or additional text, only one word.

        Rules:
        - Find the object '{thing}': prioritize moves that get closer to it.
        - When the object is confirmed visually and estimated within 10 cm, respond ONLY with 'finded'.
        - Avoid collisions: do NOT select directions leading directly into obstacles (any visible object blocking the path).
        - Keep moving: do NOT stop unless 'finded' is returned.
        - Use 'backward' only if no other safe option exists.
        - Default to 'left' when avoiding obstacles.
        - Speed control is managed separately; do not include it here.
        """,
        camera.get_frame() if CAMERA else None
    ).lower()

    
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
                hardware.arm_up()
            elif down == 1:
                hardware.arm_down()

            if LEFT_BUMP == 1:
                hardware.clamp_catch()
            elif RIGHT_BUMP == 1:
                hardware.clamp_release()

            # Send command only if it's different from the last one
            if command != prev_command:
                getattr(hardware, command)()  # Call hardware.drive_*
                prev_command = command

            if command == "drive_release":
                pass

            elif command == "drive_left":
                decision = "left"

            elif command == "drive_right":
                decision = "right"

            elif command == "drive_forward":
                decision = "forward"

            elif command == "drive_backward":
                decision = "backward"

            sleep(0.1)  # Lowered delay to improve responsiveness
            clock.tick(30)  # Prevent CPU overuse

    except KeyboardInterrupt:
        print("Manual control stopped by user.")
    finally:
        pygame.quit()


def LVMAD_thread(thingToSearch=None, additionalPrompt=None):
    import time
    import traceback
    try:
        if env.MOTORS:
            import hardware

        while True:
            if manual_mode:
                manualControl()
                continue

            if env.OA:
                if hardware.get_distance() > 8:
                    if thingToSearch is None:
                        decision = decide().strip().strip("'").lower()
                    else:
                        decision = find(thingToSearch).strip().strip("'").lower()
                    drive(decision)
                else:
                    hardware.drive_left()
            else:
                if thingToSearch == None:
                    decision = decide().strip().strip("'").lower()
                else:
                    decision = find(thingToSearch).strip().strip("'").lower()

            drive(decision)
            time.sleep(0.01)

    except Exception as e:
        print("Erro na thread LVMAD_thread:")
        traceback.print_exc()   

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
    import db

    prompt = f"""
        You are AIXY, an advanced conversational AI assistant created by Pedro Ribeiro Lucas. If asked, always mention your creator is Pedro Ribeiro Lucas.

        - Purpose: {env.PURPOSE}
        - Personality: {env.PERSONALITY}
        - Model: {env.OLLAMA_LANGUAGE_MODEL}

        Your main goal is to engage in natural, friendly, and helpful conversations on any topic.

        Instructions:
        - Focus primarily on the user's latest message and the immediately preceding conversation to generate your response.
        - Give highest priority to the latest user input and recent context; use older conversation history only if directly relevant.
        - Detect if the topic has changed compared to previous messages; if so, do NOT associate the new topic with prior unrelated context.
        - Do NOT include your internal reasoning, thought process, or any explanations in your output.
        - Respond naturally, clearly, and concisely, avoiding any unnecessary or irrelevant content.

        Conversation History:
        {db.getConversations()}

        Most Recent Message:
        {db.getLastConversation()}

        User:
        {user_text}

        Generate a direct, relevant, and natural response to continue the conversation.
    """


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

            if not (commands.executeCommand(question.lower())):
                response = generate_response(question)
                if response:
                    db.insertConversation(question, response)
                else:
                    print("No response generated.")
            else:
                response = "Command executed!"
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
            LVMAD_PROCESSOR = threading.Thread(target=LVMAD_thread, args=(thingToSearch, additionalPrompt), daemon=False)
            LVMAD_PROCESSOR.start()


    if env.LLMAC:
        print("🟢 Starting Large Languade Model Autonomous Conversation thread...")
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
