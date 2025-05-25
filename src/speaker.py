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

import subprocess
import tempfile
import os
from playsound import playsound

def speak(message, voice="en-US-AvaMultilingualNeural"):
    print(f"Converting message to speech: {message}\n")
    try:
        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            temp_path = tmp_file.name

        print("Generating speech with edge-tts CLI...\n")
        # Montar o comando
        command = [
            "edge-tts",
            "--text", message,
            "--voice", voice,
            "--write-media", temp_path
        ]

        # Chamar o edge-tts via subprocess
        subprocess.run(command, check=True)

        # Reproduzir o áudio
        playsound(temp_path)

        # Limpar o arquivo temporário
        os.remove(temp_path)
        print("Speech playback completed\n")

    except subprocess.CalledProcessError as e:
        print(f"edge-tts failed with error: {e}\n")
    except Exception as e:
        print(f"An error occurred during speech playback: {str(e)}\n")
