"""
===============================================================================================================================================================
===============================================================================================================================================================

                                                                   _      ___  __  __ __   __  ____         ___  
                                                                  / \    |_ _| \ \/ / \ \ / / |___ \       / _ \ 
                                                                 / _ \    | |   \  /   \ V /    __) |     | | | |
                                                                / ___ \   | |   /  \    | |    / __/   _  | |_| |
                                                               /_/   \_\ |___| /_/\_\   |_|   |_____| (_)  \___/ 

                                                               
                                                                            COMPUTER HARDWARE CODE
                                                                            by Pedro Ribeiro Lucas
                                                                                                                  
===============================================================================================================================================================
===============================================================================================================================================================
"""

import serial

# === Serial Connection ===
ser = None
try:
    ser = serial.Serial('/dev/ttyAML6', 9600, timeout=1)
    if ser.is_open:
        print("✅ Serial port opened successfully!")
    else:
        print("⚠️ Serial port not open.")
except serial.SerialException as e:
    print(f"❌ SerialException: {e}")
except Exception as e:
    print(f"❌ General error: {e}")


# === MOTOR CONTROL ===
def drive_forward():
    if ser and ser.is_open:
        ser.write(b"drive_forward\n")

def drive_backward():
    if ser and ser.is_open:
        ser.write(b"drive_backward\n")

def drive_left():
    if ser and ser.is_open:
        ser.write(b"drive_left\n")

def drive_right():
    if ser and ser.is_open:
        ser.write(b"drive_right\n")

def drive_release():
    if ser and ser.is_open:
        ser.write(b"drive_release\n")

def drive_stop():
    if ser and ser.is_open:
        ser.write(b"drive_stop\n")


# === ULTRASONIC SENSOR ===
def get_distance():
    if ser and ser.is_open:
        ser.write(b"ultrassonic_data\n")
        response = ser.readline().decode('utf-8').strip()
        try:
            return float(response)
        except ValueError:
            print(f"⚠️ Invalid distance response: {response}")
            return None
    else:
        print("❌ Serial not available.")
        return None


# === SERVO CONTROL ===
def clamp_catch():
    if ser and ser.is_open:
        ser.write(b"arm_down\n")
        ser.write(b"clamp_catch\n")
        ser.write(b"arm_up\n")

def clamp_release():
    if ser and ser.is_open:
        ser.write(b"arm_down\n")
        ser.write(b"clamp_release\n")
        ser.write(b"arm_up\n")
