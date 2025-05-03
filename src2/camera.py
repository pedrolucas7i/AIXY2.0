# camera.py
# Author: Pedro Lucas
# Project: AIXY2.0

import threading
import cv2
import numpy as np
import time

class Camera:

    _instance = None

    def __new__(cls):
        from picamera2 import Picamera2
        if cls._instance is None:
            cls._instance = super(Camera, cls).__new__(cls)
            cls._instance._init_camera()
        return cls._instance

    def _init_camera(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration(main={'size': (224, 224)}))
        self.picam2.start()

        self.frame = None
        self.lock = threading.Lock()
        self.running = True

        thread = threading.Thread(target=self.update_frame, daemon=True)
        thread.start()

    def update_frame(self):
        while self.running:
            frame = self.picam2.capture_array()
            rotated = np.rot90(frame, 2)
            _, jpeg = cv2.imencode('.jpg', rotated)
            with self.lock:
                self.frame = jpeg.tobytes()
            time.sleep(0.1)

    def get_frame(self):
        with self.lock:
            return self.frame

    def get_web_stream(self):
        while True:
            frame = self.get_frame()
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)


class CameraUSB:
    _instance = None

    def __new__(cls, camera_index=0):
        if cls._instance is None:
            cls._instance = super(CameraUSB, cls).__new__(cls)
            cls._instance._init_camera(camera_index)
        return cls._instance

    def _init_camera(self, camera_index):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)

        if not self.cap.isOpened():
            raise RuntimeError(f"Error opening USB camera at index {camera_index}")

        self.frame = None
        self.lock = threading.Lock()
        self.running = True

        thread = threading.Thread(target=self.update_frame, daemon=True)
        thread.start()

    def update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            frame_resized = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
            _, jpeg = cv2.imencode('.jpg', frame_resized)

            with self.lock:
                self.frame = jpeg.tobytes()

            time.sleep(0.1)

    def get_frame(self):
        with self.lock:
            return self.frame

    def get_web_stream(self):
        while True:
            frame = self.get_frame()
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)

    def __del__(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.running = False
            self.cap.release()