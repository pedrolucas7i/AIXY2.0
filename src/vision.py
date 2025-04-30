from ollama import Client
from time import sleep
from camera import CameraUSB
import utils
import llm
import env

camera = CameraUSB()
        
def decide(additionalPrompt=None):
    if additionalPrompt:
        decision = llm.get(env.OLLAMA_VISION_MODEL, env.OLLAMA_VISION_DECISION_PROMPT, camera.get_frame())
    else:
        decision = llm.get(env.OLLAMA_VISION_MODEL, env.OLLAMA_VISION_DECISION_PROMPT, camera.get_frame())
    logging.info(f"Decided: {decision}")
    print(f"Decided: {decision}")
    return decision

def find(thing, localization=None, additionalPrompt=None):
    if additionalPrompt:
        decision = llm.get(env.OLLAMA_VISION_MODEL, utils.findObjectVisionPrompt(thing, localization, additionalPrompt=additionalPrompt), camera.get_frame())
    else:
        decision = llm.get(env.OLLAMA_VISION_MODEL, utils.findObjectVisionPrompt(thing, localization), camera.get_frame())
    logging.info(f"Decided: {decision}")
    print(f"Decided: {decision}")
    return decision
