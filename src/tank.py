# Import the Motor class from the gpiozero library
from gpiozero import Motor as Motors, DistanceSensor, PWMSoftwareFallback, Servo
from threading import Lock
from time import sleep
import warnings
import env

# Define the tankMotor class to control the motors of a tank-like robot
class Motor:
    
    def __init__(self):
        """Initialize the tankMotor class with GPIO pins for the left and right motors."""
        self.left_motor = Motors(23, 24)  # Initialize the left motor with GPIO pins 23 and 24
        self.right_motor = Motors(6, 5)   # Initialize the right motor with GPIO pins 6 and 5
        self.lock = Lock()

    def duty_range(self, duty1, duty2):
        """Ensure the duty cycle values are within the valid range (-4095 to 4095)."""
        if duty1 > 4095:
            duty1 = 4095     # Cap the value at 4095 if it exceeds the maximum
        elif duty1 < -4095:
            duty1 = -4095    # Cap the value at -4095 if it falls below the minimum
        
        if duty2 > 4095:
            duty2 = 4095     # Cap the value at 4095 if it exceeds the maximum
        elif duty2 < -4095:
            duty2 = -4095    # Cap the value at -4095 if it falls below the minimum
        
        return duty1, duty2  # Return the clamped duty cycle values

    def left_Wheel(self, duty):
        """Control the left wheel based on the duty cycle value."""
        if duty > 0:
            self.left_motor.forward(duty / 4096)    # Move the left motor forward
        elif duty < 0:
            self.left_motor.backward(-duty / 4096)  # Move the left motor backward
        else:
            self.left_motor.stop()                  # Stop the left motor

    def right_Wheel(self, duty):
        """Control the right wheel based on the duty cycle value."""
        if duty > 0:
            self.right_motor.forward(duty / 4096)    # Move the right motor forward
        elif duty < 0:
            self.right_motor.backward(-duty / 4096)  # Move the right motor backward
        else:
            self.right_motor.stop()                  # Stop the right motor

    def setMotorModel(self, duty1, duty2):
        """Set the duty cycle for both motors and ensure they are within the valid range."""
        with self.lock:
            duty1, duty2 = self.duty_range(duty1, duty2)
            self.left_Wheel(-duty1)
            self.right_Wheel(-duty2)

        
    def driveBackward(self, speedLevel=1):
        """Drive Backward with diferent speed levels"""
        pwm_value = -800
        
        if speedLevel == 2:
            pwm_value = -1200
        elif speedLevel == 3:
            pwm_value = -2640
        elif speedLevel == 4:
            pwm_value = -4000
        
        self.setMotorModel(pwm_value + int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE), pwm_value + int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE))
        
    def driveRight(self, turnLevel=1):
        """Drive Right with diferent turn levels"""
        left_pwm = -800
        right_pwm = 800
        
        if turnLevel == 2:
            left_pwm = -1200
            right_pwm = 1200
        elif turnLevel == 3:
            left_pwm = -2640
            right_pwm = 2640
        elif turnLevel == 4:
            left_pwm = -4000
            right_pwm = 4000
        
        self.setMotorModel(-left_pwm + int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE), -right_pwm + int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE))
        
    def driveLeft(self, turnLevel=1):
        """Drive Left with diferent turn levels"""
        left_pwm = 800
        right_pwm = -800
        
        if turnLevel == 2:
            left_pwm = 1200
            right_pwm = -1200
        elif turnLevel == 3:
            left_pwm = 2640
            right_pwm = -2640
        elif turnLevel == 4:
            left_pwm = 4000
            right_pwm = -4000
        
        self.setMotorModel(-left_pwm + int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE), -right_pwm + int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE))
        
    def driveForward(self, speedLevel=1):
        """Drive Backward with diferent speed levels"""
        pwm_value = 800
        
        if speedLevel == 2:
            pwm_value = 1200
        elif speedLevel == 3:
            pwm_value = 2640
        elif speedLevel == 4:
            pwm_value = 4000
        
        self.setMotorModel(pwm_value - int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE), pwm_value - int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE))
    
    def stop(self):
        with self.lock:
            self.setMotorModel(0, 0) 
    
    def close(self):
        """Close the motors to release resources."""
        self.left_motor.close()   # Close the left motor
        self.right_motor.close()  # Close the right motor
        
class Ultrasonic:
    def __init__(self):
        # Initialize the Ultrasonic class and set up the distance sensor.
        warnings.filterwarnings("ignore", category=PWMSoftwareFallback)  # Ignore PWM software fallback warnings
        self.trigger_pin = 27  # Set the trigger pin number
        self.echo_pin = 22     # Set the echo pin number
        self.sensor = DistanceSensor(echo=self.echo_pin, trigger=self.trigger_pin, max_distance=3)  # Initialize the distance sensor

    def get_distance(self):
        # Get the distance measurement from the ultrasonic sensor in centimeters.
        distance_cm = self.sensor.distance * 100  # Convert distance from meters to centimeters
        return round(float(distance_cm), 1)       # Return the distance rounded to one decimal place

    def close(self):
        # Close the distance sensor.
        self.sensor.close()        # Close the sensor to release resources
        
class Clamp:
    def __init__(self):
        self.servo = None
        if self.servo is None:
            self.servo0 = Servo(12)
            self.servo1 = Servo(13)
        
    def up(self):
        """Perform clamp up operation"""
        # Get distance from ultrasonic sensor
#        distance = self.sonic.get_distance()
#        motor = Motor()
#        # Control motor based on distance
#        if distance <= 5:
#            motor.driveBackward(2)
#        elif distance > 5 and distance < 7.5:
#            motor.driveBackward(1)
#        elif distance >= 7.5 and distance <= 7.7:
#            motor.stop()
            # Adjust servos to clamp up
        for i in range(180, 90, -1):
            self.servo1.value = (i - 90) / 90
            sleep(0.01)
        for i in range(170, 90, -1):
            self.servo0.value = (i - 90) / 90
            sleep(0.01)  
        for i in range(90, 180, 1):
            self.servo1.value = (i - 90) / 90
            sleep(0.01)
#        elif distance > 7.7 and distance < 11:
#            motor.driveForward(1)
#        elif distance >= 11:
#            motor.driveForward(2)
        # Sleep for a short duration
#        sleep(0.05) 

    def down(self):
        """Perform clamp down operation"""
#        motor = Motor()
#        motor.stop()
        # Adjust servos to clamp down
        for i in range(180, 90, -1):
            self.servo1.value = (i - 90) / 90
            sleep(0.01)
        for i in range(90, 170, 1):
            self.servo0.value = (i - 90) / 90
            sleep(0.01)  
        for i in range(90, 180, 1):
            self.servo1.value = (i - 90) / 90
            sleep(0.01)

# Main program logic follows:
if __name__ == '__main__':
    print('MOTOR TESTING STARTED ... \n')  # Print a start message
    motor = Motor()                        # Create an instance of the tankMotor class
    while True:
        try:
            motor.driveLeft(4)
            sleep(0.35)
            motor.driveForward(1)
            sleep(0.5)
            motor.driveLeft(4)
            sleep(0.35)
            motor.driveForward(1)
            sleep(0.5)
            motor.driveLeft(4)
            sleep(0.35)
            motor.driveForward(1)
            sleep(0.5)
            motor.driveLeft(4)
            sleep(0.35)
            motor.driveForward(1)
            sleep(0.5)
        except KeyboardInterrupt:              # Handle a keyboard interrupt (Ctrl+C)
            motor.setMotorModel(0, 0)          # Stop both motors
            motor.close()                      # Close the motors to release resources