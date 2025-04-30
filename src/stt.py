import whisper
import numpy as np
import sounddevice as sd
import queue
import tempfile
import wave
import threading
import time
import os

# Load Whisper model (Use 'tiny' for better performance on Raspberry Pi)
model = whisper.load_model("medium")

# Audio parameters
SAMPLE_RATE = 16000  # Whisper requires 16kHz audio
CHANNELS = 1  # Mono
BLOCK_SIZE = 1024  # Block size for continuous recording
SILENCE_THRESHOLD = 1000  # Adjustable silence detection threshold
SILENCE_TIME = 1.5  # Time (seconds) to confirm silence before processing

# Queue to store recorded audio chunks
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    """Callback function that continuously records audio."""
    if status:
        print(status)
    audio_queue.put(indata.copy())

def detect_silence(audio_buffer):
    """Detects when the user stops speaking based on volume level."""
    volume = np.abs(audio_buffer).mean()
    return volume < SILENCE_THRESHOLD

def audio_generator():
    """Generates complete speech segments by detecting silence."""
    buffer = np.array([], dtype=np.int16)
    silence_start_time = None

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=np.int16,
                        blocksize=BLOCK_SIZE, callback=audio_callback):
        while True:
            data = audio_queue.get()
            buffer = np.concatenate((buffer, data.flatten()))

            # Check for silence
            if detect_silence(buffer):
                if silence_start_time is None:
                    silence_start_time = time.time()  # Start silence timer
                elif time.time() - silence_start_time > SILENCE_TIME:
                    if len(buffer) > SAMPLE_RATE * 0.5:  # Ensure at least 0.5s of speech
                        yield transcribe_audio(buffer)  # Return transcribed text
                    buffer = np.array([], dtype=np.int16)  # Reset buffer
                    silence_start_time = None  # Reset silence detection
            else:
                silence_start_time = None  # Reset timer if voice is detected

def transcribe_audio(audio_buffer):
    """Transcribes the recorded speech and returns the text."""
    fd, temp_wav = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    with wave.open(temp_wav, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_buffer.tobytes())

    print("Transcribing...")
    result = model.transcribe(audio=temp_wav)
    os.unlink(temp_wav)  # Remove temporary file after use

    user_text = result.get("text", "").strip()
    if user_text:
        print(f"You said: {user_text}")
    return user_text

if __name__ == "__main__":
    for text in audio_generator():
        print(f"Received: {text}")