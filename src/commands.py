import utils
import tank
import tts
import env
import time
import logging
from threading import Lock

# Cria os motores e clamp apenas uma vez
motors_lock = Lock()
Motors = tank.Motor()
Clamp = tank.Clamp()

def executeCommand(stt_data):
    commands_actions = [
        (env.COMMANDS[0], lambda: (tts.speak(f"{utils.getDistance()}{env.RESPONSES[0]}"))),
        (env.COMMANDS[1], lambda: (tts.speak(env.RESPONSES[1]), Motors.drive_forward(2))),
        (env.COMMANDS[2], lambda: (tts.speak(env.RESPONSES[2]), Motors.drive_left(3))),
        (env.COMMANDS[3], lambda: (tts.speak(env.RESPONSES[3]), Motors.drive_right(3))),
        (env.COMMANDS[4], lambda: (tts.speak(env.RESPONSES[4]), Motors.drive_backward(3))),
        (env.COMMANDS[5], lambda: (tts.speak(env.RESPONSES[5]), Clamp.up())),
        (env.COMMANDS[6], lambda: stop_for_40_seconds(Motors)),
    ]

    for command, action in commands_actions:
        if command in stt_data:
            action()
            break

def stop_for_40_seconds(motor_instance):
    tts.speak(env.RESPONSES[6])
    with motors_lock:
        motor_instance.stop()
        logging.info("Motors stopped. Holding for 40 seconds...")
        time.sleep(40)
        logging.info("Done waiting. Releasing motors.")
    tts.speak("I'm back")
