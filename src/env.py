"""
===============================================================================================================================================================
===============================================================================================================================================================

                                                                   _      ___  __  __ __   __  ____         ___  
                                                                  / \    |_ _| \ \/ / \ \ / / |___ \       / _ \ 
                                                                 / _ \    | |   \  /   \ V /    __) |     | | | |
                                                                / ___ \   | |   /  \    | |    / __/   _  | |_| |
                                                               /_/   \_\ |___| /_/\_\   |_|   |_____| (_)  \___/ 

                                                               
                                                                            COMPUTER   ENV    CODE
                                                                            by Pedro Ribeiro Lucas
                                                                                                                  
===============================================================================================================================================================
===============================================================================================================================================================
"""

# Import the necessary module
from dotenv import load_dotenv
import os

""" Large Vision Model Automonous Drive """
LVMAD = True

""" Large Languade Model Autonomous Conversations """
LLMAC = False

""" Obstacle Avoidance """
OA = False

""" Switch Between Modes """
SBM = False

""" Web Camera Stream """
WCS = False

""" Text to Speech """
TTS = True

""" Speech to Text """
STT = True

""" ONLY MANUAL CONTROL"""
ONLY_MANUAL_CONTROL = False

""" AIXY COMMANDS """
COMMANDS = True

""" Motors """
MOTORS = True

""" Camera """
CAMERA = True

""" Camera Connection """
CAMERA_USB = True

# Load environment variables from the .env file
load_dotenv()
AIXY_SOFTWARE_VERSION = os.getenv('AIXY_SOFTWARE_VERSION')
FIRST_MESSAGE = os.getenv('FIRST_MESSAGE')
OLLAMA_VISION_MODEL = os.getenv('OLLAMA_VISION_MODEL')
OLLAMA_LANGUAGE_MODEL = os.getenv('OLLAMA_LANGUAGE_MODEL')
OLLAMA_VISUAL_FINDING_PROMPT = os.getenv('OLLAMA_VISUAL_FINDING_PROMPT')
OLLAMA_VISUAL_DECISION_PROMPT = os.getenv('OLLAMA_VISUAL_DECISION_PROMPT')
OLLAMA_USER_ADDITIONAL_PROMPT = os.getenv('OLLAMA_USER_ADDITIONAL_PROMPT')
OLLAMA_HOST = os.getenv('OLLAMA_HOST')
WHISPER_HOST = os.getenv('WHISPER_HOST')

PERSONALITY = (lambda f: f.read())(open("personality.info", "r", encoding="utf-8"))
PURPOSE = (lambda f: f.read())(open("purpose.info", "r", encoding="utf-8"))

COMMANDS = [
    'get ultrasonic data',
    'analyze object',
    'say',
    'flash lights',
    'listen for command',
    'report status',
    'reboot system',
    'turn the light on',
    'turn the light off'
]

if MOTORS:
    COMMANDS += [
        'catch the object',
        'release object',
        'drive forward',
        'turn left',
        'turn right',
        'drive backward',
        'stop now',
    ]

RESPONSES = [
    'centimeters to the obstacle',
    'analyzing object...',
    'saying message',
    'flashing lights',
    'listening...',
    'status report: all systems nominal',
    'rebooting system...',
    'light turned on',
    'light turned off'
]

if MOTORS:
    RESPONSES += [
        'catching the object',
        'releasing the object',
        'Driving forward',
        'turning left',
        'turning right',
        'driving backward',
        'stopped for 30 seconds',
    ]



"""
movements = {
    "forward": {"direction": "forward", "speed": 2},
    "backward": {"direction": "backward", "speed": 2},
    "slow forward": {"direction": "forward", "speed": 1},
    "slow backward": {"direction": "backward", "speed": 1},
    "fast forward": {"direction": "forward", "speed": 3},
    "fast backward": {"direction": "backward", "speed": 3},
    "faster forward": {"direction": "forward", "speed": 4},
    "left": {"direction": "left", "speed": 2},
    "right": {"direction": "right", "speed": 2},
    "left fast": {"direction": "left", "speed": 3},
    "right fast": {"direction": "right", "speed": 3},
    "left very fast": {"direction": "left", "speed": 4},
    "right very fast": {"direction": "right", "speed": 4},
    "left hiper fast": {"direction": "left", "speed": 4},
    "right hiper fast": {"direction": "right", "speed": 4},
}
"""
