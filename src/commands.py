import env
import speaker
import subprocess

def drive_forward():
    import hardware
    speaker.speak(env.RESPONSES[9])
    hardware.drive_forward()

def turn_left():
    import hardware
    speaker.speak(env.RESPONSES[10])
    hardware.drive_left()

def turn_right():
    import hardware
    speaker.speak(env.RESPONSES[11])
    hardware.drive_right()

def drive_backward():
    import hardware
    speaker.speak(env.RESPONSES[12])
    hardware.drive_backward()

def stop_now():
    import hardware
    speaker.speak(env.RESPONSES[13])
    hardware.drive_stop()

def light_on():
    import hardware
    hardware.ligthON()
    speaker.speak(env.RESPONSES[5])

def light_off():
    import hardware
    hardware.ligthOFF()
    speaker.speak(env.RESPONSES[6])

def flash_light():
    import hardware
    hardware.flasklight()
    speaker.speak(env.RESPONSES[3])

def catch_object():
    import hardware
    speaker.speak(env.RESPONSES[7])
    hardware.clamp_catch()

def release_object():
    import hardware
    speaker.speak(env.RESPONSES[8])
    hardware.clamp_release()

def getDistance():
    import hardware
    speaker.speak(f"{hardware.get_distance()} {env.RESPONSES[0]}")

def reboot():
    subprocess.run("reboot")

def executeCommand(stt_data):

    def say_message():
        message = stt_data.split("say", 1)[-1].strip()
        if message:
            speaker.speak(message)
        else:
            speaker.speak(env.RESPONSES[2])

    commands_actions = {
        'get ultrasonic data': getDistance,
        'analyze object': lambda: speaker.speak(env.RESPONSES[1]),
        'say': say_message,
        'flash lights': flash_light,
        'reboot system': lambda: (reboot(), speaker.speak(env.RESPONSES[4])),
        'turn the light on': light_on,
        'turn the light off': light_off,
    }

    if env.MOTORS:
        commands_actions.update({
            'catch the object': catch_object,
            'release object': release_object,
            'drive forward': drive_forward,
            'turn left': turn_left,
            'turn right': turn_right,
            'drive backward': drive_backward,
            'stop now': stop_now,
        })

    for command, action in commands_actions.items():
        if command in stt_data:
            action()
            return True

    return False