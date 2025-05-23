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

from gtts import gTTS
from playsound import playsound
import tempfile
import os
import db

# Define the speech function that uses gTTS
def speak(message):
    print(f"Converting message to speech: {message}\n")
    try:
        print("Converting message to speech\n")
        
        # Create a temporary file for the speech audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            temp_path = tmp_file.name

        # Save TTS output to temp file
        tts = gTTS(text=message, lang='en', slow=False)
        tts.save(temp_path)

        # Play the temporary audio file
        playsound(temp_path)
        
        # Clean up temporary file after playback
        os.remove(temp_path)

        print("Speech playback completed\n")
    except Exception as e:
        print(f"An error occurred during speech playback: {str(e)}\n")
