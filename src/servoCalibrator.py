from gpiozero import Servo
from time import sleep

# Define servos on GPIO pins
servo1 = Servo(13)  # Assuming GPIO 13
servo2 = Servo(12)  # Assuming GPIO 12

# Convert angle to servo value (-1 to 1)
def angle_to_value(angle):
    return (angle / 180) * 2 - 1

# Set servo angles
while True:
    servo2.value = angle_to_value(150)  # Move to 150 degrees
    servo1.value = angle_to_value(90)
    sleep(2)