import logging
import threading
import time
from gtts import gTTS
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def speak(message):
    logging.info(f"Converting message to speech: {message}")
    print('\nTTS:\n', message.strip())

    # Define the speech function that uses gTTS
    def play_speech():
        try:
            logging.info("Converting message to speech")
            
            # Use gTTS to convert the message to speech (Google TTS API)
            tts = gTTS(text=message, lang='en', slow=False)
            tts.save("message.mp3")  # Save the speech to a file
            
            # Play the saved speech file
            os.system("cvlc message.mp3")  # You can use other audio players if needed
            
            logging.info("Speech playback completed")
        except Exception as e:
            logging.error(f"An error occurred during speech playback: {str(e)}")

    # Start the speech in a separate thread
    speech_thread = threading.Thread(target=play_speech)
    speech_thread.start()
