"""
===============================================================================================================================================================
===============================================================================================================================================================

                                                                   _      ___  __  __ __   __  ____         ___  
                                                                  / \    |_ _| \ \/ / \ \ / / |___ \       / _ \ 
                                                                 / _ \    | |   \  /   \ V /    __) |     | | | |
                                                                / ___ \   | |   /  \    | |    / __/   _  | |_| |
                                                               /_/   \_\ |___| /_/\_\   |_|   |_____| (_)  \___/ 

                                                               
                                                                            COMPUTER SPEAKER  CODE
                                                                            by Pedro Ribeiro Lucas
                                                                                                                  
===============================================================================================================================================================
===============================================================================================================================================================
"""

import requests
from playsound import playsound
import tempfile
import os
import env

# Define the speech function using custom TTS server
def speak(message):
    print(f"Converting message to speech: {message}\n")
    try:
        print("Sending message to TTS server...\n")
        
        # Send POST request to TTS server
        response = requests.post(
            env.TTS_HOST,
            headers={"Content-Type": "application/json"},
            json={"text": message}
        )
        
        if response.status_code != 200:
            raise Exception(f"TTS server returned error: {response.status_code} - {response.text}")
        
        # Create temporary file for WAV audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(response.content)
            temp_path = tmp_file.name

        # Play the audio
        playsound(temp_path)

        # Clean up
        os.remove(temp_path)
        print("Speech playback completed\n")

    except Exception as e:
        print(f"An error occurred during speech playback: {str(e)}\n")
