# speaker.py
# Author: Pedro Lucas
# Project: AIXY2.0

from gtts import gTTS
from playsound import playsound

# Define the speech function that uses gTTS
def speak(message):
    print(f"Converting message to speech: {message}\n")
    print(f'TTS: {message.strip()}\n')
    try:
        print("Converting message to speech\n")
        
        # Use gTTS to convert the message to speech (Google TTS API)
        tts = gTTS(text=message, lang='en', slow=False)
        tts.save("message.mp3")  # Save the speech to a file
        
        # Play the saved speech file
        playsound('message.mp3')
        
        print("Speech playback completed\n")
    except Exception as e:
        print(f"An error occurred during speech playback: {str(e)}\n")