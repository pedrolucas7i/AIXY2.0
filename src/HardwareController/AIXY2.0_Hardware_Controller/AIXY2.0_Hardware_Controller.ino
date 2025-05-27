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

#define PIN_ARM 7                                     // Pin responsible for ARM SERVO
#define PIN_CLAMP 2                                   // Pin responsible for CLAMP SERVO

#define TRIGGER_PIN  11                               // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     10                               // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 500                              // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

Servo arm;
Servo clamp;

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);   // NewPing setup of pins and maximum distance.

int backward_pwm = 175;                               // PWM used to drive backward
int armPos = 90;                                      // Variable that saves the actual arm servo position
int clampPos = 90;                                    // Variable that saves the actual clamp servo position

void setup() {
  pinMode(PIN_MOTOR1_IN1, OUTPUT);                    // Defining PIN's as ouptuts
  pinMode(PIN_MOTOR1_IN2, OUTPUT);
  pinMode(PIN_MOTOR2_IN1, OUTPUT);
  pinMode(PIN_MOTOR2_IN2, OUTPUT);
  pinMode(13, OUTPUT);
  arm.attach(PIN_ARM);                                // Defining the PIN of ARM SERVO
  clamp.attach(PIN_CLAMP);                            // Defining the PIN of CLAMP SERVO
  Serial.begin(9600);                                 // Start Serial comunication in 9600 bauds
  arm_up();
  
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
    } else if (command == "flash_light") {
      flash();
      Serial.println("OK: flashed_light");
    } else if (command == "light_on") {
      light_on();
      Serial.println("OK: light_on");
    } else if (command == "light_off") {
      light_off();
      Serial.println("OK: light_off");
    } else {
      Serial.println("COMMAND NOT FOUND!");
    }
  }
  avoid_obstacle();
}


// === MOTOR COMMANDS ===

void drive_forward() {
  digitalWrite(PIN_MOTOR1_IN2, LOW);
  digitalWrite(PIN_MOTOR2_IN2, LOW);
  digitalWrite(PIN_MOTOR1_IN1, HIGH);
  digitalWrite(PIN_MOTOR2_IN1, HIGH);
  delay(300);
  drive_release();  // Release motors after driving forward
}

void drive_backward() {
  digitalWrite(PIN_MOTOR1_IN1, LOW);
  digitalWrite(PIN_MOTOR2_IN1, LOW);
  analogWrite(PIN_MOTOR1_IN2, backward_pwm);
  analogWrite(PIN_MOTOR2_IN2, backward_pwm);
  delay(300);
  drive_release();  // Release motors after driving backward
}

void drive_right() {
  digitalWrite(PIN_MOTOR1_IN1, LOW);
  digitalWrite(PIN_MOTOR2_IN1, HIGH);
  digitalWrite(PIN_MOTOR1_IN2, HIGH);
  digitalWrite(PIN_MOTOR2_IN2, LOW);
  delay(300);
  drive_release();  // Release motors after driving right
}

void drive_left() {
  digitalWrite(PIN_MOTOR1_IN1, HIGH);
  digitalWrite(PIN_MOTOR2_IN1, LOW);
  digitalWrite(PIN_MOTOR1_IN2, LOW);
  digitalWrite(PIN_MOTOR2_IN2, HIGH);
  delay(300);
  drive_release();  // Release motors after driving left
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
  for (int pos = armPos; pos > 110; pos--) {
    arm.write(pos);
    delay(16);
  }
  armPos = 110;
}

void arm_up() {
  for (int pos = armPos; pos < 180; pos++) {
    arm.write(pos);
    delay(17);
  }
  armPos = 180;
}

void clamp_release() {
  for (int pos = clampPos; pos > 90; pos--) {
    clamp.write(pos);
    delay(15);
  }
  clampPos = 90;
}

void clamp_catch() {
  for (int pos = clampPos; pos < 170; pos++) {
    clamp.write(pos);
    delay(15);
  }
  clampPos = 170;
}

float ultrassonic_data() {
  return sonar.ping_cm();                             // Return ping distance in cm
}
  

// === LIGHT COMMANDS ===

void flash() {
  digitalWrite(13, HIGH);
  delay(600);
  digitalWrite(13, LOW);
}

void light_on() {
  digitalWrite(13, HIGH);
}

void light_off() {
  digitalWrite(13, LOW);
}


// Obstacule Avoidance Function

void avoid_obstacle() {
  float distance = ultrassonic_data();               // Get the distance from the ultrasonic sensor
  if ((distance < 10) && (distance != 0)) {                               // If an obstacle is detected within 10 cm
    drive_backward();                                // Move backward
    delay(500);                                      // Wait for half a second
    drive_left();                                    // Turn left to avoid the obstacle
    delay(500);                                      // Wait for half a second
  }
}
