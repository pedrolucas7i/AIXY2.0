# Import the necessary module
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
AIXY_SOFTWARE_VERSION = os.getenv('AIXY_SOFTWARE_VERSION')
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE')
FIRST_EN_MESSAGE = os.getenv('FIRST_EN_MESSAGE')
OLLAMA_VISION_MODEL = os.getenv('OLLAMA_VISION_MODEL')
OLLAMA_LANGUAGE_MODEL = os.getenv('OLLAMA_LANGUAGE_MODEL')
WHISPER_MODEL = os.getenv('WHISPER_MODEL')
LEFT_MOTOR_CORRECTION_PWM_VALUE = os.getenv('LEFT_MOTOR_CORRECTION_PWM_VALUE')
RIGHT_MOTOR_CORRECTION_PWM_VALUE = os.getenv('RIGHT_MOTOR_CORRECTION_PWM_VALUE')
OLLAMA_EN_SEARCH_PROMPT = os.getenv('OLLAMA_EN_SEARCH_PROMPT')
OLLAMA_PT_SEARCH_PROMPT = os.getenv('OLLAMA_PT_SEARCH_PROMPT')
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