"""
===============================================================================================================================================================
===============================================================================================================================================================

                                                                   _      ___  __  __ __   __  ____         ___  
                                                                  / \    |_ _| \ \/ / \ \ / / |___ \       / _ \ 
                                                                 / _ \    | |   \  /   \ V /    __) |     | | | |
                                                                / ___ \   | |   /  \    | |    / __/   _  | |_| |
                                                               /_/   \_\ |___| /_/\_\   |_|   |_____| (_)  \___/ 

                                                               
                                                                            COMPUTER WCS CORE CODE
                                                                            by Pedro Ribeiro Lucas
                                                                                                                  
===============================================================================================================================================================
===============================================================================================================================================================
"""

from flask import Flask, render_template, Response
import env

if env.CAMERA:
    from camera import CameraUSB
    camera = CameraUSB()

if env.MOTORS:
    import hardware


#Initialize the Flask app
app = Flask(__name__, template_folder="./WCS_thread/webserver", static_folder="./WCS_thread/static")

@app.route('/')
def index():
    return render_template('index.html')

if env.MOTORS:
    @app.route('/forward')
    def forward():
        hardware.drive_forward()

    @app.route('/left')
    def left():
        hardware.drive_left()

    @app.route('/right')
    def right():
        hardware.drive_right()

    @app.route('/backward')
    def backward():
        hardware.drive_backward()

    @app.route('/release')
    def release():
        hardware.drive_release()

if env.CAMERA:
    @app.route('/stream')
    def stream():
        return Response(camera.get_web_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run():
    app.run(debug=True, port=9900, host="0.0.0.0")

if __name__ == '__main__':
    run()