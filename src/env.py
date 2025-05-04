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

# Load environment variables from the .env file
load_dotenv()
AIXY_SOFTWARE_VERSION = os.getenv('AIXY_SOFTWARE_VERSION')
FIRST_EN_MESSAGE = os.getenv('FIRST_EN_MESSAGE')
OLLAMA_VISION_MODEL = os.getenv('OLLAMA_VISION_MODEL')
OLLAMA_LANGUAGE_MODEL = os.getenv('OLLAMA_LANGUAGE_MODEL')
OLLAMA_EN_SEARCH_VISUAL_PROMPT = os.getenv('OLLAMA_EN_SEARCH_VISUAL_PROMPT')
OLLAMA_VISION_DECISION_PROMPT = os.getenv('OLLAMA_VISION_DECISION_PROMPT')
OLLAMA_USER_ADDITIONAL_PROMPT = os.getenv('OLLAMA_USER_ADDITIONAL_PROMPT')
DB_FILE = os.getenv('DB_FILE')
OLLAMA_HOST = os.getenv('OLLAMA_HOST')
WHISPER_HOST = os.getenv('WHISPER_HOST')

PERSONALITY = (lambda f: f.read())(open("personality.info", "r", encoding="utf-8"))
PURPOSE = (lambda f: f.read())(open("purpose.info", "r", encoding="utf-8"))

COMMANDS = [
    'get ultrasonic data',
    'drive forward',
    'turn left',
    'turn right',
    'drive backward',
    'catch the object',
    'stop now',
]

RESPONSES = [
    'centimeters to the obstacle',
    'Driving forward',
    'turning left',
    'turning right',
    'driving backward',
    'catching the object',
    'stoped for 40 seconds',
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