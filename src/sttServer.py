import os
import tempfile
import wave
from flask import Flask, request, jsonify
import whisper
import torch

# Set the environment variable to restrict to CUDA device 0
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

app = Flask(__name__)

# Ensure the model is loaded onto GPU 0 (if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("medium").to(device)  # Explicitly move the model to GPU 0

@app.route("/transcribe", methods=["POST"])
def transcribe():
    # Check if the audio file is part of the request
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    # Save the uploaded audio file to a temporary location
    audio_file = request.files["audio"]
    fd, temp_wav = tempfile.mkstemp(suffix=".wav")
    with open(temp_wav, "wb") as f:
        f.write(audio_file.read())
    os.close(fd)
    
    print("Transcribing...")
    
    # Transcribe the audio file using Whisper
    result = model.transcribe(temp_wav)
    
    # Remove the temporary audio file
    os.unlink(temp_wav)
    
    # Return the transcribed text as a JSON response
    return jsonify({"text": result.get("text", "").strip()})

if __name__ == "__main__":
    # Run the Flask app on all available IP addresses (0.0.0.0) and port 5000
    app.run(host="0.0.0.0", port=5000)
