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

# === STOP SERIAL-GETTY SERVICE ONLY ONCE ===
def stop_serial_getty_once():
    """Execute the command only once when the program starts."""
    try:
        # Stop the conflicting serial-getty service (Linux TTY login shell)
        subprocess.run(["sudo", "systemctl", "stop", "serial-getty@ttyAML0.service"],
                       check=True)
        print("serial-getty service stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping serial-getty: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# === Execute the stop command only once when the program starts ===
stop_serial_getty_once()

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
            time.sleep(0.05)  # Give microcontroller time to process

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
    """
    Requests distance from ultrasonic sensor and parses numeric value.

    Returns:
        float or None: Distance in cm if valid, None if response malformed.
    """
    response = send_command("ultrassonic_data")
    if response and response.startswith("DIST:"):
        try:
            return float(response.split(":")[1].strip())
        except ValueError:
            print(f"Invalid distance response: {response}")
    return None


# === SERVO CONTROL ===
def system_catch():
    """
    Lowers arm, closes clamp, raises arm — with command acknowledgment.
    """
    send_command("arm_up")
    time.sleep(0.1)
    send_command("clamp_catch")
    time.sleep(0.1)
    send_command("arm_down")

def system_release():
    """
    Lowers arm, opens clamp, raises arm — with command acknowledgment.
    """
    send_command("arm_up")
    time.sleep(0.1)
    send_command("clamp_release")
    time.sleep(0.1)
    send_command("arm_down")

def arm_down():
    send_command("arm_down")

def arm_up():
    send_command("arm_up")

def clamp_catch():
    send_command("clamp_catch")

def clamp_release():
    send_command("clamp_release")