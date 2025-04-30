import OPi.GPIO as GPIO
from time import sleep
from threading import Lock
import warnings
import time

class Motor:
    def __init__(self):
        """Initialize the Motor class with GPIO pins for the left and right motors."""
        self.left_motor_pwm_pin1 = 23  # GPIO pin 23 (PWM)
        self.left_motor_pwm_pin2 = 24  # GPIO pin 24 (PWM)
        self.right_motor_pwm_pin1 = 6  # GPIO pin 6 (PWM)
        self.right_motor_pwm_pin2 = 5  # GPIO pin 5 (PWM)
        self.lock = Lock()
        GPIO.setmode(GPIO.BOARD)  # Use BOARD numbering for GPIO pins
        GPIO.setup(self.left_motor_pwm_pin1, GPIO.OUT)
        GPIO.setup(self.left_motor_pwm_pin2, GPIO.OUT)
        GPIO.setup(self.right_motor_pwm_pin1, GPIO.OUT)
        GPIO.setup(self.right_motor_pwm_pin2, GPIO.OUT)

        # Initialize the motor pins
        GPIO.output(self.left_motor_pwm_pin1, GPIO.LOW)
        GPIO.output(self.left_motor_pwm_pin2, GPIO.LOW)
        GPIO.output(self.right_motor_pwm_pin1, GPIO.LOW)
        GPIO.output(self.right_motor_pwm_pin2, GPIO.LOW)

    def duty_range(self, duty1, duty2):
        """Ensure the duty cycle values are within the valid range (0 to 100)."""
        if duty1 > 100:
            duty1 = 100
        elif duty1 < 0:
            duty1 = 0
        if duty2 > 100:
            duty2 = 100
        elif duty2 < 0:
            duty2 = 0
        return duty1, duty2

    def left_wheel(self, duty):
        """Control the left wheel based on the duty cycle value."""
        if duty > 0:
            GPIO.output(self.left_motor_pwm_pin1, GPIO.HIGH)
            GPIO.output(self.left_motor_pwm_pin2, GPIO.LOW)
            sleep(duty / 100.0)
            GPIO.output(self.left_motor_pwm_pin1, GPIO.LOW)
        elif duty < 0:
            GPIO.output(self.left_motor_pwm_pin1, GPIO.LOW)
            GPIO.output(self.left_motor_pwm_pin2, GPIO.HIGH)
            sleep(-duty / 100.0)
            GPIO.output(self.left_motor_pwm_pin2, GPIO.LOW)
        else:
            GPIO.output(self.left_motor_pwm_pin1, GPIO.LOW)
            GPIO.output(self.left_motor_pwm_pin2, GPIO.LOW)

    def right_wheel(self, duty):
        """Control the right wheel based on the duty cycle value."""
        if duty > 0:
            GPIO.output(self.right_motor_pwm_pin1, GPIO.HIGH)
            GPIO.output(self.right_motor_pwm_pin2, GPIO.LOW)
            sleep(duty / 100.0)
            GPIO.output(self.right_motor_pwm_pin1, GPIO.LOW)
        elif duty < 0:
            GPIO.output(self.right_motor_pwm_pin1, GPIO.LOW)
            GPIO.output(self.right_motor_pwm_pin2, GPIO.HIGH)
            sleep(-duty / 100.0)
            GPIO.output(self.right_motor_pwm_pin2, GPIO.LOW)
        else:
            GPIO.output(self.right_motor_pwm_pin1, GPIO.LOW)
            GPIO.output(self.right_motor_pwm_pin2, GPIO.LOW)

    def set_motor_model(self, duty1, duty2):
        """Set the duty cycle for both motors and ensure they are within the valid range."""
        with self.lock:
            duty1, duty2 = self.duty_range(duty1, duty2)
            self.left_wheel(duty1)
            self.right_wheel(duty2)

    def drive_backward(self, speed_level=1):
        """Drive backward with different speed levels."""
        pwm_value = 50  # 50% duty cycle, this increases power to the motors
        if speed_level == 2:
            pwm_value = 70  # 70% duty cycle
        elif speed_level == 3:
            pwm_value = 85  # 85% duty cycle
        elif speed_level == 4:
            pwm_value = 100  # 100% duty cycle for max power
        self.set_motor_model(pwm_value, pwm_value)

    def drive_right(self, turn_level=1):
        """Drive right with different turn levels."""
        left_pwm = 50
        right_pwm = 50
        if turn_level == 2:
            left_pwm = 70
            right_pwm = 70
        elif turn_level == 3:
            left_pwm = 85
            right_pwm = 85
        elif turn_level == 4:
            left_pwm = 100
            right_pwm = 100
        self.set_motor_model(left_pwm, right_pwm)

    def drive_left(self, turn_level=1):
        """Drive left with different turn levels."""
        left_pwm = 50
        right_pwm = 50
        if turn_level == 2:
            left_pwm = 70
            right_pwm = 70
        elif turn_level == 3:
            left_pwm = 85
            right_pwm = 85
        elif turn_level == 4:
            left_pwm = 100
            right_pwm = 100
        self.set_motor_model(left_pwm, right_pwm)

    def drive_forward(self, speed_level=1):
        """Drive forward with different speed levels."""
        pwm_value = 50
        if speed_level == 2:
            pwm_value = 70
        elif speed_level == 3:
            pwm_value = 85
        elif speed_level == 4:
            pwm_value = 100  # Max power (100% duty cycle)
        self.set_motor_model(pwm_value, pwm_value)

    def stop(self):
        """Stop the motors."""
        with self.lock:
            self.set_motor_model(0, 0)

    def close(self):
        """Close the motors to release resources."""
        GPIO.cleanup()

class Ultrasonic:
    def __init__(self):
        """Initialize the Ultrasonic sensor class."""
        warnings.filterwarnings("ignore", category=PWMSoftwareFallback)  # Ignore PWM warnings
        self.trigger_pin = 27  # GPIO trigger pin
        self.echo_pin = 22     # GPIO echo pin
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        """Measure the distance using the ultrasonic sensor."""
        # Send a pulse to trigger the ultrasonic sensor
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        sleep(0.00001)
        GPIO.output(self.trigger_pin, GPIO.LOW)
        
        # Measure the time it takes for the echo to return
        pulse_start = time.time()
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
        
        pulse_end = time.time()
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Calculate distance in cm
        return round(distance, 2)

    def close(self):
        """Cleanup the ultrasonic sensor."""
        GPIO.cleanup(self.trigger_pin)
        GPIO.cleanup(self.echo_pin)

class Clamp:
    def __init__(self):
        """Initialize the Clamp class and set up servo control."""
        self.servo_pin1 = 12  # GPIO pin for the first servo
        self.servo_pin2 = 13  # GPIO pin for the second servo
        GPIO.setup(self.servo_pin1, GPIO.OUT)
        GPIO.setup(self.servo_pin2, GPIO.OUT)
        
        # Set up PWM for both servos
        self.servo1 = GPIO.PWM(self.servo_pin1, 50)  # 50Hz for servos
        self.servo2 = GPIO.PWM(self.servo_pin2, 50)
        self.servo1.start(0)  # Start with 0% duty cycle (servo off)
        self.servo2.start(0)

    def up(self):
        """Move the clamp up (open the clamp)."""
        # Move the servos to the "up" position
        self.servo1.ChangeDutyCycle(12)  # Adjust this value as needed for servo calibration
        self.servo2.ChangeDutyCycle(8)   # Adjust this value as needed for servo calibration
        sleep(1)  # Wait for the servo to reach the position

    def down(self):
        """Move the clamp down (close the clamp)."""
        # Move the servos to the "down" position
        self.servo1.ChangeDutyCycle(8)
        self.servo2.ChangeDutyCycle(12)
        sleep(1)  # Wait for the servo to reach the position

    def close(self):
        """Stop PWM and clean up the servos."""
        self.servo1.stop()
        self.servo2.stop()
        GPIO.cleanup(self.servo_pin1)
        GPIO.cleanup(self.servo_pin2)

# Main program logic follows:
if __name__ == '__main__':
    print('MOTOR TESTING STARTED ... \n')
    motor = Motor()  # Create an instance of the Motor class
    ultrasonic = Ultrasonic()  # Create an instance of the Ultrasonic class
    clamp = Clamp()  # Create an instance of the Clamp class

    try:
        while True:
            distance = ultrasonic.get_distance()  # Get distance from the ultrasonic sensor
            print(f"Distance: {distance} cm")

            # Use the clamp based on the distance
            if distance < 10:  # If an object is closer than 10cm
                print("Moving clamp up...")
                clamp.up()
                motor.drive_backward(2)
            elif distance >= 10 and distance <= 20:  # If the object is between 10 and 20 cm
                print("Moving clamp down...")
                clamp.down()
                motor.drive_forward(2)
            else:  # If the object is farther than 20cm
                motor.stop()

            sleep(1)  # Pause between actions

    except KeyboardInterrupt:
        motor.stop()  # Stop both motors
        motor.close()  # Close the motors to release resources
        ultrasonic.close()  # Cleanup ultrasonic sensor
        clamp.close()  # Cleanup clamp servos
        print('Program stopped safely.')
