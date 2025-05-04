"""
===============================================================================================================================================================
===============================================================================================================================================================

                                                                   _      ___  __  __ __   __  ____         ___  
                                                                  / \    |_ _| \ \/ / \ \ / / |___ \       / _ \ 
                                                                 / _ \    | |   \  /   \ V /    __) |     | | | |
                                                                / ___ \   | |   /  \    | |    / __/   _  | |_| |
                                                               /_/   \_\ |___| /_/\_\   |_|   |_____| (_)  \___/ 

                                                               
                                                                            COMPUTER  LLM API CODE
                                                                            by Pedro Ribeiro Lucas
                                                                                                                  
===============================================================================================================================================================
===============================================================================================================================================================
"""

from ollama import Client
from time import sleep
import env

def get(model, prompt, image_stream=None):
    client = Client(host=env.OLLAMA_HOST)
    if image_stream is None:
        try:
            return client.generate(model, prompt)['response']
        except Exception as e:
            print(f"An error occurred in llm.get(): {str(e)}\n")
    else:
        try:
            return client.generate(model, prompt, images=[image_stream])['response']
        except Exception as e:
            print(f"An error occurred in llm.get(image): {str(e)}\n")