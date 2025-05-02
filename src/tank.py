import OPi.GPIO as GPIO
from time import sleep
from threading import Lock
import warnings
import time

# === MOTOR CONTROL ===
class Motor:
    def __init__(self):
        self.left_motor_pwm_pin1 = 115  # Físico 27
        self.left_motor_pwm_pin2 = 73   # Físico 28
        self.right_motor_pwm_pin1 = 69  # Físico 29
        self.right_motor_pwm_pin2 = 70  # Físico 31
        self.lock = Lock()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.left_motor_pwm_pin1, GPIO.OUT)
        GPIO.setup(self.left_motor_pwm_pin2, GPIO.OUT)
        GPIO.setup(self.right_motor_pwm_pin1, GPIO.OUT)
        GPIO.setup(self.right_motor_pwm_pin2, GPIO.OUT)

        GPIO.output(self.left_motor_pwm_pin1, GPIO.LOW)
        GPIO.output(self.left_motor_pwm_pin2, GPIO.LOW)
        GPIO.output(self.right_motor_pwm_pin1, GPIO.LOW)
        GPIO.output(self.right_motor_pwm_pin2, GPIO.LOW)

    def duty_range(self, duty1, duty2):
        duty1 = max(0, min(100, duty1))
        duty2 = max(0, min(100, duty2))
        return duty1, duty2

    def left_wheel(self, duty):
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
        with self.lock:
            duty1, duty2 = self.duty_range(duty1, duty2)
            self.left_wheel(duty1)
            self.right_wheel(duty2)

    def drive_backward(self, speed_level=1):
        pwm = {1: 50, 2: 70, 3: 85, 4: 100}.get(speed_level, 50)
        self.set_motor_model(-pwm, -pwm)

    def drive_forward(self, speed_level=1):
        pwm = {1: 50, 2: 70, 3: 85, 4: 100}.get(speed_level, 50)
        self.set_motor_model(pwm, pwm)

    def drive_left(self, turn_level=1):
        pwm = {1: 50, 2: 70, 3: 85, 4: 100}.get(turn_level, 50)
        self.set_motor_model(-pwm, pwm)

    def drive_right(self, turn_level=1):
        pwm = {1: 50, 2: 70, 3: 85, 4: 100}.get(turn_level, 50)
        self.set_motor_model(pwm, -pwm)

    def stop(self):
        with self.lock:
            self.set_motor_model(0, 0)

    def close(self):
        GPIO.cleanup()


# === ULTRASONIC SENSOR ===
class Ultrasonic:
    def __init__(self):
        self.trigger_pin = 74  # Físico 35
        self.echo_pin = 75     # Físico 36
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        sleep(0.00001)
        GPIO.output(self.trigger_pin, GPIO.LOW)

        pulse_start = time.time()
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()

        pulse_end = time.time()
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        return round(distance, 2)

    def close(self):
        GPIO.cleanup(self.trigger_pin)
        GPIO.cleanup(self.echo_pin)


# === CLAMP (SERVO CONTROL) ===
class Clamp:
    def __init__(self):
        self.servo_pin1 = 71  # Físico 32
        self.servo_pin2 = 72  # Físico 33
        GPIO.setup(self.servo_pin1, GPIO.OUT)
        GPIO.setup(self.servo_pin2, GPIO.OUT)
        self.servo1 = GPIO.PWM(self.servo_pin1, 50)
        self.servo2 = GPIO.PWM(self.servo_pin2, 50)
        self.servo1.start(0)
        self.servo2.start(0)

    def up(self):
        self.servo1.ChangeDutyCycle(12)
        self.servo2.ChangeDutyCycle(8)
        sleep(1)

    def down(self):
        self.servo1.ChangeDutyCycle(8)
        self.servo2.ChangeDutyCycle(12)
        sleep(1)

    def close(self):
        self.servo1.stop()
        self.servo2.stop()
        GPIO.cleanup(self.servo_pin1)
        GPIO.cleanup(self.servo_pin2)


# === MAIN PROGRAM ===
if __name__ == '__main__':
    print('MOTOR TESTING STARTED ... \n')
    motor = Motor()
    ultrasonic = Ultrasonic()
    clamp = Clamp()

    try:
        while True:
            distance = ultrasonic.get_distance()
            print(f"Distance: {distance} cm")

            if distance < 10:
                print("Moving clamp up...")
                clamp.up()
                motor.drive_backward(2)
            elif 10 <= distance <= 20:
                print("Moving clamp down...")
                clamp.down()
                motor.drive_forward(2)
            else:
                motor.stop()

            sleep(1)

    except KeyboardInterrupt:
        motor.stop()
        motor.close()
        ultrasonic.close()
        clamp.close()
        print('Program stopped safely.')
