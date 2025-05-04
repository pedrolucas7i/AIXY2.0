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
import time

ser = None

# === Serial Connection ===
try:
    ser = serial.Serial('/dev/ttyAML0', 9600, timeout=2)  # Increased timeout to improve reliability
    print("Serial open with Success!")
except serial.SerialException as e:
    print(f"Error in serial port: {e}")
except Exception as e:
    print(f"General error: {e}")

# === Internal helper to send command and wait for confirmation ===
def send_command(cmd):
    if ser and ser.is_open:
        ser.write((cmd + "\n").encode())
        time.sleep(0.05)
        while True:
            response = ser.readline().decode().strip()
            if response.startswith("OK:") or response.startswith("DIST:"):
                return response
            elif response == "":
                continue
            else:
                print(f"Unexpected response: {response}")
                break

# === MOTOR CONTROL ===
def drive_forward():
    print(send_command("drive_forward"))

def drive_backward():
    print(send_command("drive_backward"))

def drive_left():
    print(send_command("drive_left"))

def drive_right():
    print(send_command("drive_right"))

def drive_release():
    print(send_command("drive_release"))

def drive_stop():
    print(send_command("drive_stop"))

# === ULTRASONIC SENSOR ===
def get_distance():
    response = send_command("ultrassonic_data")
    if response and response.startswith("DIST:"):
        try:
            return float(response.split(":")[1].strip())
        except ValueError:
            print(f"Invalid distance response: {response}")
            return None

# === SERVO CONTROL ===
def clamp_catch():
    send_command("arm_down")
    send_command("clamp_catch")
    send_command("arm_up")

def clamp_release():
    send_command("arm_down")
    send_command("clamp_release")
    send_command("arm_up")
