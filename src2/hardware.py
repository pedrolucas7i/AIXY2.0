# hardware.py
# Author: Pedro Lucas
# Project: AIXY2.0


import serial

# === Serial Connection ===
try:
    ser = serial.Serial('/dev/ttyAML6', 9600, timeout=1)
    print("Serial open with Success!")
except serial.SerialException as e:
    print(f"Error in serial port: {e}")
except Exception as e:
    print(f"General error: {e}")


# === MOTOR CONTROL ===
def drive_forward():
    ser.write("drive_forward\n".encode('utf-8'))

def drive_backward():
    ser.write("drive_backward\n".encode('utf-8'))

def drive_left():
    ser.write("drive_left\n".encode('utf-8'))

def drive_right():
    ser.write("drive_right\n".encode('utf-8'))

def drive_release():
    ser.write("drive_release\n".encode('utf-8'))

def drive_stop():
    ser.write("drive_stop\n".encode('utf-8'))


# === ULTRASONIC SENSOR ===
def get_distance():
    ser.write("ultrassonic_data\n".encode('utf-8'))
    response = ser.readline().decode('utf-8').strip()
    try:
        return float(response)
    except ValueError:
        print(f"Invalid Response: {response}")
        return None


# === SERVO CONTROL ===
def clamp_catch():
    ser.write("arm_down\n".encode('utf-8'))
    ser.write("clamp_catch\n".encode('utf-8'))
    ser.write("arm_up\n".encode('utf-8'))

def clamp_release():
    ser.write("arm_down\n".encode('utf-8'))
    ser.write("clamp_release\n".encode('utf-8'))
    ser.write("arm_up\n".encode('utf-8'))
