from ollama import Client
from time import sleep
import logging
import env

def get(model, prompt, image_stream=None):
    client = Client(host=env.OLLAMA_HOST)
    if image_stream is None:
        try:
            return client.generate(model, prompt)['response']
        except Exception as e:
            logging.error(f"An error occurred in llm.get(): {str(e)}")
    else:
        try:
            return client.generate(model, prompt, images=[image_stream])['response']
        except Exception as e:
            logging.error(f"An error occurred in llm.get(image): {str(e)}")