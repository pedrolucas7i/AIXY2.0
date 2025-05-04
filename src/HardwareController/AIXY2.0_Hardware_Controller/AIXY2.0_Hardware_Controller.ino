/*
===============================================================================================================================================================
===============================================================================================================================================================

                                                                   _      ___  __  __ __   __  ____         ___  
                                                                  / \    |_ _| \ \/ / \ \ / / |___ \       / _ \ 
                                                                 / _ \    | |   \  /   \ V /    __) |     | | | |
                                                                / ___ \   | |   /  \    | |    / __/   _  | |_| |
                                                               /_/   \_\ |___| /_/\_\   |_|   |_____| (_)  \___/ 


                                                                            HARDWARE CONTROLER CODE
                                                                            by Pedro Ribeiro Lucas
                                                                                                                  
===============================================================================================================================================================
===============================================================================================================================================================
*/

#include <Servo.h>                                    // Includes the Servo Library
#include <NewPing.h>                                  // Includes the Ultrassonic Sensor Library

#define PIN_MOTOR1_IN1 3                              // Pin responsible for motor1 clockwise control
#define PIN_MOTOR2_IN1 4                              // Pin responsible for motor2 clockwise control
#define PIN_MOTOR1_IN2 5                              // Pin responsible for counterclockwise control
#define PIN_MOTOR2_IN2 6                              // Pin responsible for counterclockwise control

#define PIN_ARM 2                                     // Pin responsible for ARM SERVO
#define PIN_CLAMP 7                                   // Pin responsible for CLAMP SERVO

#define TRIGGER_PIN  11                               // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     10                               // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 350                              // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

Servo arm;
Servo clamp;

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);   // NewPing setup of pins and maximum distance.

int backward_pwm = 175;                               // PWM used to drive backward

void setup() {
  pinMode(PIN_MOTOR1_IN1, OUTPUT);                    // Defining PIN's as ouptuts
  pinMode(PIN_MOTOR1_IN2, OUTPUT);
  pinMode(PIN_MOTOR2_IN1, OUTPUT);
  pinMode(PIN_MOTOR2_IN2, OUTPUT);
  arm.attach(PIN_ARM);                                // Defining the PIN of ARM SERVO
  clamp.attach(PIN_CLAMP);                            // Defining the PIN of CLAMP SERVO
  Serial.begin(9600);                                 // Start Serial comunication in 9600 bauds
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');    // Read command until newline
    command.trim();                                   // Remove whitespaces or extra characters

    // Compare command strings directly and send back confirmation
    if (command == "drive_forward") {
      drive_forward();
      Serial.println("OK: drive_forward");
    } else if (command == "drive_backward") {
      drive_backward();
      Serial.println("OK: drive_backward");
    } else if (command == "drive_left") {
      drive_left();
      Serial.println("OK: drive_left");
    } else if (command == "drive_right") {
      drive_right();
      Serial.println("OK: drive_right");
    } else if (command == "drive_release") {
      drive_release();
      Serial.println("OK: drive_release");
    } else if (command == "drive_stop") {
      drive_stop();
      Serial.println("OK: drive_stop");
    } else if (command == "ultrassonic_data") {
      float dist = ultrassonic_data();
      Serial.print("DIST: ");
      Serial.println(dist);
    } else if (command == "arm_down") {
      arm_down();
      Serial.println("OK: arm_down");
    } else if (command == "arm_up") {
      arm_up();
      Serial.println("OK: arm_up");
    } else if (command == "clamp_catch") {
      clamp_catch();
      Serial.println("OK: clamp_catch");
    } else if (command == "clamp_release") {
      clamp_release();
      Serial.println("OK: clamp_release");
    } else {
      Serial.println("COMMAND NOT FOUND!");
    }
  }
}


// === MOTOR COMMANDS ===

void drive_forward() {
  digitalWrite(PIN_MOTOR1_IN2, LOW);
  digitalWrite(PIN_MOTOR2_IN2, LOW);
  digitalWrite(PIN_MOTOR1_IN1, HIGH);
  digitalWrite(PIN_MOTOR2_IN1, HIGH);
  delay(1000);
}

void drive_backward() {
  digitalWrite(PIN_MOTOR1_IN1, LOW);
  digitalWrite(PIN_MOTOR2_IN1, LOW);
  analogWrite(PIN_MOTOR1_IN2, backward_pwm);
  analogWrite(PIN_MOTOR2_IN2, backward_pwm);
  delay(1000);
}

void drive_left() {
  digitalWrite(PIN_MOTOR1_IN1, LOW);
  digitalWrite(PIN_MOTOR2_IN1, HIGH);
  digitalWrite(PIN_MOTOR1_IN2, HIGH);
  digitalWrite(PIN_MOTOR2_IN2, LOW);
  delay(700);
}

void drive_right() {
  digitalWrite(PIN_MOTOR1_IN1, HIGH);
  digitalWrite(PIN_MOTOR2_IN1, LOW);
  digitalWrite(PIN_MOTOR1_IN2, LOW);
  digitalWrite(PIN_MOTOR2_IN2, HIGH);
  delay(700);
}

void drive_release() {
  digitalWrite(PIN_MOTOR1_IN1, LOW);
  digitalWrite(PIN_MOTOR2_IN1, LOW);
  digitalWrite(PIN_MOTOR1_IN2, LOW);
  digitalWrite(PIN_MOTOR2_IN2, LOW);
}

void drive_stop() {
  digitalWrite(PIN_MOTOR1_IN1, HIGH);
  digitalWrite(PIN_MOTOR2_IN1, HIGH);
  digitalWrite(PIN_MOTOR1_IN2, HIGH);
  digitalWrite(PIN_MOTOR2_IN2, HIGH);
}


// === SERVO AND SENSOR COMMANDS ===

void arm_down() {
  for (int pos = 180; pos > 90; pos--) {
    arm.write(pos);
    delay(17);
  }
}

void arm_up() {
  for (int pos = 90; pos < 180; pos++) {
    arm.write(pos);
    delay(17);
  }
}

void clamp_release() {
  for (int pos = 170; pos > 90; pos--) {
    clamp.write(pos);
    delay(15);
  }
}

void clamp_catch() {
  for (int pos = 90; pos < 170; pos++) {
    clamp.write(pos);
    delay(15);
  }
}

float ultrassonic_data() {
  return sonar.ping_cm();                             // Return ping distance in cm
}
