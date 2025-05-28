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
import subprocess

# Serial object
ser = None

# === Serial Connection Initialization ===
try:
    ser = serial.Serial('/dev/ttyAML0', 9600, timeout=2)  # Increased timeout for more reliable reads
    time.sleep(2)  # Wait for Arduino boot after serial open
    print("Serial open with Success!")
except serial.SerialException as e:
    print(f"Error in serial port: {e}")
except Exception as e:
    print(f"General error: {e}")


# === Internal Helper to Send a Command and Wait for Valid Response ===
def send_command(cmd):
    """
    Sends a command string to the serial port, waits for an 'OK:' or 'DIST:' response.
    
    Args:
        cmd (str): Command string to send to microcontroller.

    Returns:
        str: The valid response from microcontroller or None if unexpected.
    """
    if ser and ser.is_open:
        try:
            full_cmd = f"{cmd}\n"
            ser.write(full_cmd.encode('utf-8'))  # Encode properly to bytes
            ser.flush()  # Force immediate transmission

            while True:
                response = ser.readline().decode('utf-8', errors='replace').strip()
                if response == "":
                    continue  # No data received, keep waiting (timeout handles escape)
                if response.startswith("OK:") or response.startswith("DIST:"):
                    return response
                else:
                    print(f"Unexpected response: {response}")
                    return None
        except Exception as e:
            print(f"Error during serial communication: {e}")
            return None


# === MOTOR CONTROL ===
def drive_forward():
    response = send_command("drive_forward")
    print(response)

def drive_backward():
    response = send_command("drive_backward")
    print(response)

def drive_left():
    response = send_command("drive_left")
    print(response)

def drive_right():
    response = send_command("drive_right")
    print(response)

def drive_release():
    response = send_command("drive_release")
    print(response)

def drive_stop():
    response = send_command("drive_stop")
    print(response)

# === SERVO CONTROL ===
def system_catch():
    if send_command("arm_up"):
        time.sleep(0.1)
        if send_command("clamp_catch"):
            time.sleep(0.1)
            send_command("arm_down")

def system_release():
    if send_command("arm_up"):
        time.sleep(0.1)
        if send_command("clamp_release"):
            time.sleep(0.1)
            send_command("arm_down")

def arm_down():
    response = send_command("arm_down")
    print(response)
    if response:
        time.sleep(0.1)

def arm_up():
    response = send_command("arm_up")
    print(response)
    if response:
        time.sleep(0.1)

def clamp_catch():
    response = send_command("clamp_catch")
    print(response)
    if response:
        time.sleep(0.1)

def clamp_release():
    response = send_command("clamp_release")
    print(response)
    if response:
        time.sleep(0.1)

# === ULTRASONIC SENSOR ===
def get_distance():
    response = send_command("ultrassonic_data")
    if response and response.startswith("DIST:"):
        try:
            return float(response.split(":")[1].strip())
        except ValueError:
            print(f"Invalid distance response: {response}")
            return None
    else:
        print("No valid distance received.")
        return None

# === LIGHT CONTROL ===
def lightON():
    response = send_command("light_on")
    print(response)

def lightOFF():
    response = send_command("light_off")
    print(response)

def flash_light():
    response = send_command("flash_light")
    print(response)
