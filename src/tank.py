import subprocess
from time import sleep, time
from threading import Lock

# === GPIO NUMERAÇÃO (Linux GPIO) PARA LE POTATO ===
# Baseado nos pinos físicos a partir do 26

LEFT_FORWARD = 27     # Físico 27 - GPIOA_11
LEFT_BACKWARD = 28    # Físico 28 - GPIOX_11
RIGHT_FORWARD = 29    # Físico 29 - GPIOX_7
RIGHT_BACKWARD = 31   # Físico 31 - GPIOX_8

SERVO1 = 32           # Físico 32 - GPIOX_9
SERVO2 = 33           # Físico 33 - GPIOX_10

TRIG = 35             # Físico 35 - GPIOX_12
ECHO = 36             # Físico 36 - GPIOX_13


# === FUNÇÃO AUXILIAR PARA EXECUTAR COMANDOS COM subprocess ===
def run_command(command):
    """Executa um comando no shell e retorna a saída."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stdout.decode('utf-8'), e.stderr.decode('utf-8')


# === MOTOR CONTROL ===

class Motor:
    def __init__(self):
        self.lock = Lock()
        
        # Inicializando os pinos
        self.left_forward = LEFT_FORWARD
        self.left_backward = LEFT_BACKWARD
        self.right_forward = RIGHT_FORWARD
        self.right_backward = RIGHT_BACKWARD

        # Inicializa os pinos de saída
        for pin in [self.left_forward, self.left_backward, self.right_forward, self.right_backward]:
            run_command(f"sudo lgpio set {pin}=0")  # Set initial state to LOW

    def duty_range(self, duty1, duty2):
        return max(-100, min(100, duty1)), max(-100, min(100, duty2))

    def left_wheel(self, duty):
        run_command(f"sudo lgpio set {self.left_forward}=0")
        run_command(f"sudo lgpio set {self.left_backward}=0")
        if duty > 0:
            run_command(f"sudo lgpio set {self.left_forward}=1")
        elif duty < 0:
            run_command(f"sudo lgpio set {self.left_backward}=1")

    def right_wheel(self, duty):
        run_command(f"sudo lgpio set {self.right_forward}=0")
        run_command(f"sudo lgpio set {self.right_backward}=0")
        if duty > 0:
            run_command(f"sudo lgpio set {self.right_forward}=1")
        elif duty < 0:
            run_command(f"sudo lgpio set {self.right_backward}=1")

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


# === ULTRASONIC SENSOR ===

class Ultrasonic:
    def __init__(self):
        self.trigger = TRIG
        self.echo = ECHO

        # Inicializa o pino de trigger e echo
        run_command(f"sudo lgpio set {self.trigger}=0")
        run_command(f"sudo lgpio set {self.echo}=0")

    def get_distance(self):
        # Envia um pulso para o trigger
        run_command(f"sudo lgpio set {self.trigger}=1")
        sleep(0.00001)
        run_command(f"sudo lgpio set {self.trigger}=0")

        start = time()
        while True:
            echo_status = run_command(f"sudo lgpio get {self.echo}")[0].strip()
            if echo_status == '1':
                start = time()
                break

        while True:
            echo_status = run_command(f"sudo lgpio get {self.echo}")[0].strip()
            if echo_status == '0':
                stop = time()
                break

        # Calcula o tempo de viagem do sinal
        elapsed = stop - start
        distance = (elapsed * 34300) / 2
        return round(distance, 1)


# === SERVO CONTROL ===

class Clamp:
    def __init__(self):
        self.servo1 = SERVO1
        self.servo2 = SERVO2

        # Inicializa os servos
        run_command(f"sudo lgpio set {self.servo1}=0")
        run_command(f"sudo lgpio set {self.servo2}=0")

    def write_servo(self, gpio, angle):
        # Converte o ângulo (0–180) para um valor de PWM
        pulse = int((angle / 180.0) * 2000 + 500)
        run_command(f"sudo lgpio tx_pwm {gpio} 50 {pulse}")  # 50 Hz PWM

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
        ultrasonic.close()
        clamp.close()
