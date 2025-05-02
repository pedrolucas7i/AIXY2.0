import lgpio
from threading import Lock
from time import sleep
import env


CHIP = 1  # gpiochip1
CHIP_HANDLE = lgpio.gpiochip_open(CHIP)


# === GPIO CONTROL FUNCTIONS ===

def gpio_set(chip_line, value):
    _, line = chip_line.split('_')
    line = int(line)
    lgpio.gpio_claim_output(CHIP_HANDLE, line, value)

def gpio_pwm(chip_line, duty_percent):
    _, line = chip_line.split('_')
    line = int(line)
    frequency = 50  # Typical for servos
    duty_microseconds = int(duty_percent * 1_000_000)
    lgpio.tx_pwm(CHIP_HANDLE, line, frequency, duty_microseconds)


# === MOTOR CONTROL ===

class Motor:
    def __init__(self):
        self.left_forward = '1_96'
        self.left_backward = '1_97'
        self.right_forward = '1_84'
        self.right_backward = '1_85'
        self.lock = Lock()

        for pin in [self.left_forward, self.left_backward, self.right_forward, self.right_backward]:
            gpio_set(pin, 0)

    def duty_range(self, duty1, duty2):
        return max(-4095, min(4095, duty1)), max(-4095, min(4095, duty2))

    def left_Wheel(self, duty):
        gpio_set(self.left_forward, 0)
        gpio_set(self.left_backward, 0)
        if duty > 0:
            gpio_set(self.left_forward, 1)
        elif duty < 0:
            gpio_set(self.left_backward, 1)

    def right_Wheel(self, duty):
        gpio_set(self.right_forward, 0)
        gpio_set(self.right_backward, 0)
        if duty > 0:
            gpio_set(self.right_forward, 1)
        elif duty < 0:
            gpio_set(self.right_backward, 1)

    def setMotorModel(self, duty1, duty2):
        with self.lock:
            duty1, duty2 = self.duty_range(duty1, duty2)
            self.left_Wheel(-duty1)
            self.right_Wheel(-duty2)

    def driveBackward(self, speedLevel=1):
        pwm_value = -800 * speedLevel
        self.setMotorModel(
            pwm_value + int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE),
            pwm_value + int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE)
        )

    def driveForward(self, speedLevel=1):
        pwm_value = 800 * speedLevel
        self.setMotorModel(
            pwm_value - int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE),
            pwm_value - int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE)
        )

    def driveLeft(self, turnLevel=1):
        pwm = 800 * turnLevel
        self.setMotorModel(
            -pwm + int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE),
            pwm - int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE)
        )

    def driveRight(self, turnLevel=1):
        pwm = 800 * turnLevel
        self.setMotorModel(
            pwm - int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE),
            -pwm + int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE)
        )

    def stop(self):
        self.setMotorModel(0, 0)

    def close(self):
        self.stop()


# === ULTRASONIC SENSOR ===

class Ultrasonic:
    def __init__(self):
        self.trigger = '1_86'  # Pin 35
        self.echo = '1_95'     # Pin 32
        gpio_set(self.trigger, 0)

    def get_distance(self):
        import time
        TRIG = 86
        ECHO = 95
        lgpio.gpio_claim_output(CHIP_HANDLE, TRIG, 0)
        lgpio.gpio_claim_input(CHIP_HANDLE, ECHO)

        lgpio.gpio_write(CHIP_HANDLE, TRIG, 1)
        time.sleep(0.00001)
        lgpio.gpio_write(CHIP_HANDLE, TRIG, 0)

        start = time.time()
        while lgpio.gpio_read(CHIP_HANDLE, ECHO) == 0:
            start = time.time()
        while lgpio.gpio_read(CHIP_HANDLE, ECHO) == 1:
            stop = time.time()

        elapsed = stop - start
        distance = (elapsed * 34300) / 2  # cm
        return round(distance, 1)

    def close(self):
        pass


# === SERVO CONTROL ===

class Clamp:
    def __init__(self):
        self.servo0 = '1_81'  # Pin 36
        self.servo1 = '1_82'  # Pin 38

    def angle_to_duty(self, angle):
        # Converts angle (0–180) to 0.05–0.10 (5% to 10% duty)
        return (angle / 180.0) * 0.05 + 0.05

    def up(self):
        for i in range(180, 90, -1):
            gpio_pwm(self.servo1, self.angle_to_duty(i))
            sleep(0.01)
        for i in range(170, 90, -1):
            gpio_pwm(self.servo0, self.angle_to_duty(i))
            sleep(0.01)
        for i in range(90, 180, 1):
            gpio_pwm(self.servo1, self.angle_to_duty(i))
            sleep(0.01)

    def down(self):
        for i in range(180, 90, -1):
            gpio_pwm(self.servo1, self.angle_to_duty(i))
            sleep(0.01)
        for i in range(90, 170, 1):
            gpio_pwm(self.servo0, self.angle_to_duty(i))
            sleep(0.01)
        for i in range(90, 180, 1):
            gpio_pwm(self.servo1, self.angle_to_duty(i))
            sleep(0.01)


# === MAIN LOOP ===

if __name__ == '__main__':
    print('MOTOR TESTING STARTED ... \n')
    motor = Motor()
    try:
        while True:
            motor.driveLeft(4)
            sleep(0.35)
            motor.driveForward(1)
            sleep(0.5)
    except KeyboardInterrupt:
        motor.stop()
        motor.close()
        lgpio.gpiochip_close(CHIP_HANDLE)
