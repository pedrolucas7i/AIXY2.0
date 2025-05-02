import time
from threading import Lock
import env
from libregpio import OUT, IN

# === MOTOR CONTROL ===

class Motor:
    def __init__(self):
        self.left_forward = OUT("GPIOX_17")   # Pin 29
        self.left_backward = OUT("GPIOX_18")  # Pin 31
        self.right_forward = OUT("GPIOX_2")   # Pin 37
        self.right_backward = OUT("GPIOX_3")  # Pin 33
        self.lock = Lock()

        for pin in [self.left_forward, self.left_backward, self.right_forward, self.right_backward]:
            pin.write(0)

    def duty_range(self, duty1, duty2):
        return max(-4095, min(4095, duty1)), max(-4095, min(4095, duty2))

    def left_Wheel(self, duty):
        self.left_forward.write(0)
        self.left_backward.write(0)
        if duty > 0:
            self.left_forward.write(1)
        elif duty < 0:
            self.left_backward.write(1)

    def right_Wheel(self, duty):
        self.right_forward.write(0)
        self.right_backward.write(0)
        if duty > 0:
            self.right_forward.write(1)
        elif duty < 0:
            self.right_backward.write(1)

    def setMotorModel(self, duty1, duty2):
        with self.lock:
            duty1, duty2 = self.duty_range(duty1, duty2)
            self.left_Wheel(-duty1)
            self.right_Wheel(-duty2)

    def driveBackward(self, speedLevel=1):
        pwm_value = -800 * speedLevel
        self.setMotorModel(pwm_value + int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE),
                           pwm_value + int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE))

    def driveForward(self, speedLevel=1):
        pwm_value = 800 * speedLevel
        self.setMotorModel(pwm_value - int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE),
                           pwm_value - int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE))

    def driveLeft(self, turnLevel=1):
        pwm = 800 * turnLevel
        self.setMotorModel(-pwm + int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE),
                           pwm - int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE))

    def driveRight(self, turnLevel=1):
        pwm = 800 * turnLevel
        self.setMotorModel(pwm - int(env.LEFT_MOTOR_CORRECTION_PWM_VALUE),
                           -pwm + int(env.RIGHT_MOTOR_CORRECTION_PWM_VALUE))

    def stop(self):
        self.setMotorModel(0, 0)

    def close(self):
        self.stop()

# === ULTRASONIC SENSOR ===

class Ultrasonic:
    def __init__(self):
        self.trigger = OUT("GPIOX_19")  # Pin 35
        self.echo = IN("GPIOX_16")      # Pin 32
        self.trigger.write(0)

    def get_distance(self):
        import time
        self.trigger.write(1)
        time.sleep(0.00001)
        self.trigger.write(0)

        start = time.time()
        while self.echo.read() == 0:
            start = time.time()
        while self.echo.read() == 1:
            stop = time.time()

        elapsed = stop - start
        distance = (elapsed * 34300) / 2  # cm
        return round(distance, 1)

    def close(self):
        pass

# === SERVO CONTROL ===

class Clamp:
    def __init__(self):
        self.servo0 = OUT("GPIOX_13")  # Pin 36
        self.servo1 = OUT("GPIOX_14")  # Pin 38

    def up(self):
        for i in range(180, 90, -1):
            val = (i - 90) / 90
            self.servo1.write(val)
            time.sleep(0.01)
        for i in range(170, 90, -1):
            val = (i - 90) / 90
            self.servo0.write(val)
            time.sleep(0.01)
        for i in range(90, 180, 1):
            val = (i - 90) / 90
            self.servo1.write(val)
            time.sleep(0.01)

    def down(self):
        for i in range(180, 90, -1):
            val = (i - 90) / 90
            self.servo1.write(val)
            time.sleep(0.01)
        for i in range(90, 170, 1):
            val = (i - 90) / 90
            self.servo0.write(val)
            time.sleep(0.01)
        for i in range(90, 180, 1):
            val = (i - 90) / 90
            self.servo1.write(val)
            time.sleep(0.01)

# === MAIN ===

if __name__ == '__main__':
    print('MOTOR TESTING STARTED ... \n')
    motor = Motor()
    try:
        while True:
            motor.driveLeft(4)
            time.sleep(0.35)
            motor.driveForward(1)
            time.sleep(0.5)
    except KeyboardInterrupt:
        motor.stop()
        motor.close()
