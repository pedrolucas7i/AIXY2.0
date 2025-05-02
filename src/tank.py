import lgpio
from time import sleep, time
from threading import Lock

# === GPIO NUMERAÇÃO (Linux GPIO) PARA LE POTATO ===
# Baseado nos pinos físicos a partir do 26

LEFT_FORWARD = 115    # Físico 27 - GPIOA_11
LEFT_BACKWARD = 73    # Físico 28 - GPIOX_11
RIGHT_FORWARD = 69    # Físico 29 - GPIOX_7
RIGHT_BACKWARD = 70   # Físico 31 - GPIOX_8

SERVO1 = 71           # Físico 32 - GPIOX_9
SERVO2 = 72           # Físico 33 - GPIOX_10

TRIG = 74             # Físico 35 - GPIOX_12
ECHO = 75             # Físico 36 - GPIOX_13


# === MOTOR CONTROL ===

class Motor:
    def __init__(self):
        self.h = lgpio.gpiochip_open(1)
        self.left_forward = LEFT_FORWARD
        self.left_backward = LEFT_BACKWARD
        self.right_forward = RIGHT_FORWARD
        self.right_backward = RIGHT_BACKWARD
        self.lock = Lock()

        for pin in [self.left_forward, self.left_backward, self.right_forward, self.right_backward]:
            lgpio.gpio_claim_output(self.h, pin, 1)

    def duty_range(self, duty1, duty2):
        return max(-100, min(100, duty1)), max(-100, min(100, duty2))

    def left_wheel(self, duty):
        lgpio.gpio_write(self.h, self.left_forward, 0)
        lgpio.gpio_write(self.h, self.left_backward, 0)
        if duty > 0:
            lgpio.gpio_write(self.h, self.left_forward, 1)
        elif duty < 0:
            lgpio.gpio_write(self.h, self.left_backward, 1)

    def right_wheel(self, duty):
        lgpio.gpio_write(self.h, self.right_forward, 0)
        lgpio.gpio_write(self.h, self.right_backward, 0)
        if duty > 0:
            lgpio.gpio_write(self.h, self.right_forward, 1)
        elif duty < 0:
            lgpio.gpio_write(self.h, self.right_backward, 1)

    def set_motor_model(self, duty1, duty2):
        with self.lock:
            duty1, duty2 = self.duty_range(duty1, duty2)
            self.left_wheel(duty1)
            self.right_wheel(duty2)

    def drive_forward(self, level=1):
        pwm_value = 80 * level
        self.set_motor_model(pwm_value, pwm_value)

    def drive_backward(self, level=1):
        pwm_value = -80 * level
        self.set_motor_model(pwm_value, pwm_value)

    def drive_left(self, level=1):
        pwm = 80 * level
        self.set_motor_model(-pwm, pwm)

    def drive_right(self, level=1):
        pwm = 80 * level
        self.set_motor_model(pwm, -pwm)

    def stop(self):
        self.set_motor_model(0, 0)

    def close(self):
        self.stop()
        lgpio.gpiochip_close(self.h)


# === ULTRASONIC SENSOR ===

class Ultrasonic:
    def __init__(self):
        self.h = lgpio.gpiochip_open(0)
        self.trigger = TRIG
        self.echo = ECHO
        lgpio.gpio_claim_output(self.h, self.trigger, 0)
        lgpio.gpio_claim_input(self.h, self.echo)

    def get_distance(self):
        lgpio.gpio_write(self.h, self.trigger, 1)
        sleep(0.00001)
        lgpio.gpio_write(self.h, self.trigger, 0)

        start = time()
        while lgpio.gpio_read(self.h, self.echo) == 0:
            start = time()
        while lgpio.gpio_read(self.h, self.echo) == 1:
            stop = time()

        elapsed = stop - start
        distance = (elapsed * 34300) / 2
        return round(distance, 1)

    def close(self):
        lgpio.gpiochip_close(self.h)


# === SERVO CONTROL ===

class Clamp:
    def __init__(self):
        self.h = lgpio.gpiochip_open(0)
        self.servo1 = SERVO1
        self.servo2 = SERVO2
        lgpio.gpio_claim_output(self.h, self.servo1, 0)
        lgpio.gpio_claim_output(self.h, self.servo2, 0)

    def write_servo(self, gpio, angle):
        # Convert angle (0–180) to pulse width in microseconds (500–2500)
        pulse = int((angle / 180.0) * 2000 + 500)
        lgpio.tx_pwm(self.h, gpio, 50, pulse)  # 50 Hz PWM

    def up(self):
        for i in range(180, 90, -5):
            self.write_servo(self.servo2, i)
            sleep(0.02)
        for i in range(170, 90, -5):
            self.write_servo(self.servo1, i)
            sleep(0.02)
        for i in range(90, 180, 5):
            self.write_servo(self.servo2, i)
            sleep(0.02)

    def down(self):
        for i in range(180, 90, -5):
            self.write_servo(self.servo2, i)
            sleep(0.02)
        for i in range(90, 170, 5):
            self.write_servo(self.servo1, i)
            sleep(0.02)
        for i in range(90, 180, 5):
            self.write_servo(self.servo2, i)
            sleep(0.02)

    def close(self):
        lgpio.tx_pwm(self.h, self.servo1, 0, 0)
        lgpio.tx_pwm(self.h, self.servo2, 0, 0)
        lgpio.gpiochip_close(self.h)


# === MAIN LOOP ===

if __name__ == '__main__':
    print("MOTOR TESTING STARTED...\n")
    motor = Motor()
    ultrasonic = Ultrasonic()
    clamp = Clamp()

    try:
        while True:
            dist = ultrasonic.get_distance()
            print(f"Distance: {dist} cm")

            if dist < 10:
                print("Object close — moving clamp up and reversing...")
                clamp.up()
                motor.drive_backward(1)
            elif 10 <= dist <= 20:
                print("Medium range — moving clamp down and advancing...")
                clamp.down()
                motor.drive_forward(1)
            else:
                print("Nothing nearby — stopping.")
                motor.stop()

            sleep(1)

    except KeyboardInterrupt:
        print("\nStopping safely...")
        motor.stop()
        motor.close()
        ultrasonic.close()
        clamp.close()
