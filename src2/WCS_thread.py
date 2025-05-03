from flask import Flask, render_template, Response
from camera import CameraUSB

#Initialize the Flask app
app = Flask(__name__, template_folder="./webserver")
camera = CameraUSB()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(camera.get_web_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run():
    app.run(debug=True, port=9900, host="0.0.0.0")