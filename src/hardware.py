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
try:
    ser = serial.Serial('/dev/ttyAML6', 9600, timeout=1)
    print("Serial open with Success!")
except serial.SerialException as e:
    print(f"Error in serial port: {e}")
except Exception as e:
    print(f"General error: {e}")


# === MOTOR CONTROL ===
def drive_forward():
    ser.write("drive_forward\n")

def drive_backward():
    ser.write("drive_backward\n")

def drive_left():
    ser.write("drive_left\n")

def drive_right():
    ser.write("drive_right\n")

def drive_release():
    ser.write("drive_release\n")

def drive_stop():
    ser.write("drive_stop\n")


# === ULTRASONIC SENSOR ===
def get_distance():
    ser.write("ultrassonic_data\n")
    response = ser.readline().decode('utf-8').strip()
    try:
        return float(response)
    except ValueError:
        print(f"Invalid Response: {response}")
        return None


# === SERVO CONTROL ===
def clamp_catch():
    ser.write("arm_down\n")
    ser.write("clamp_catch\n")
    ser.write("arm_up\n")

def clamp_release():
    ser.write("arm_down\n")
    ser.write("clamp_release\n")
    ser.write("arm_up\n")
