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

String COMMANDS[] = {
  "drive_forward",
  "drive_backward",
  "drive_left",
  "drive_right",
  "drive_release",
  "drive_stop",
  "ultrassonic_data",
  "arm_down",
  "arm_up",
  "clamp_catch",
  "clamp_release",
};

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
  pinMode(PIN_MOTOR1_IN2, OUTPUT);                    // Defining PIN's as ouptuts
  pinMode(PIN_MOTOR2_IN1, OUTPUT);                    // Defining PIN's as ouptuts
  pinMode(PIN_MOTOR2_IN2, OUTPUT);                    // Defining PIN's as ouptuts
  arm.attach(PIN_ARM);                                // Defining the PIN of ARM SERVO
  clamp.attach(PIN_CLAMP);                            // Defining the PIN of CLAMP SERVO
  Serial.begin(9600);                                 // Start Serial comunication in 9600 bauds
  
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command == COMMANDS[0]) {
      drive_forward();
    } 
    else if (command == COMMANDS[1]) {
      drive_backward();
    } 
    else if (command == COMMANDS[2]) {
      drive_left();
    } 
    else if (command == COMMANDS[3]) {
      drive_right();
    } 
    else if (command == COMMANDS[4]) {
      drive_release();
    } 
    else if (command == COMMANDS[5]) {
      drive_stop();
    } 
    else if (command == COMMANDS[6]) {
      ultrassonic_data();
    } 
    else if (command == COMMANDS[7]) {
      arm_down();
    } 
    else if (command == COMMANDS[8]) {
      arm_up();
    } 
    else if (command == COMMANDS[9]) {
      clamp_catch();
    } 
    else if (command == COMMANDS[10]) {
      clamp_release();
    } 
    else {
      Serial.println("COMMAND NOT FOUND!");
    }
    
  }
}


void drive_forward() {
  digitalWrite(PIN_MOTOR1_IN2, LOW);                  // Send to PIN 0V
  digitalWrite(PIN_MOTOR2_IN2, LOW);                  // Send to PIN 0V
  digitalWrite(PIN_MOTOR1_IN1, HIGH);                 // Send to PIN ~5V
  digitalWrite(PIN_MOTOR2_IN1, HIGH);                 // Send to PIN ~5V
  delay(1000);                                        // Execute the action for 1000ms
}


void drive_backward() {
  digitalWrite(PIN_MOTOR1_IN1, LOW);                  // Send to PIN ~5V
  digitalWrite(PIN_MOTOR2_IN1, LOW);                  // Send to PIN ~5V
  analogWrite(PIN_MOTOR1_IN2, backward_pwm);          // Send to PIN backward_pwm PWM VALUE
  analogWrite(PIN_MOTOR2_IN2, backward_pwm);          // Send to PIN backward_pwm PWM VALUE
  delay(1000);                                        // Execute the action for 1000ms
}


void drive_left() {
  digitalWrite(PIN_MOTOR1_IN1, LOW);                  // Send to PIN 0V
  digitalWrite(PIN_MOTOR2_IN1, HIGH);                 // Send to PIN ~5V
  digitalWrite(PIN_MOTOR1_IN2, HIGH);                 // Send to PIN ~5V
  digitalWrite(PIN_MOTOR2_IN2, LOW);                  // Send to PIN 0V
  delay(700);                                         // Execute the action for 700ms
}

void drive_right() {
  digitalWrite(PIN_MOTOR1_IN1, HIGH);                 // Send to PIN ~5V
  digitalWrite(PIN_MOTOR2_IN1, LOW);                  // Send to PIN 0V
  digitalWrite(PIN_MOTOR1_IN2, LOW);                  // Send to PIN 0V
  digitalWrite(PIN_MOTOR2_IN2, HIGH);                 // Send to PIN ~5V
  delay(700);                                         // Execute the action for 700ms
}

void drive_release() {
  digitalWrite(PIN_MOTOR1_IN1, LOW);                  // Send to PIN 0V
  digitalWrite(PIN_MOTOR2_IN1, LOW);                  // Send to PIN 0V
  digitalWrite(PIN_MOTOR1_IN2, LOW);                  // Send to PIN 0V
  digitalWrite(PIN_MOTOR2_IN2, LOW);                  // Send to PIN 0V
}

void drive_stop() {
  digitalWrite(PIN_MOTOR1_IN1, HIGH);                 // Send to PIN ~5V
  digitalWrite(PIN_MOTOR2_IN1, HIGH);                 // Send to PIN ~5V
  digitalWrite(PIN_MOTOR1_IN2, HIGH);                 // Send to PIN ~5V
  digitalWrite(PIN_MOTOR2_IN2, HIGH);                 // Send to PIN ~5V
}


void arm_down() {
  for (int pos = 180; pos > 90; pos--) {
    arm.write(pos);
    delay(17);
  }
}

void arm_up() {
  for (int pos = 90;pos < 180; pos++) {
    arm.write(pos);
    delay(17);
  }
}


void clamp_catch() {
  for (int pos = 170; pos > 90; pos--) {
    clamp.write(pos);
    delay(15);
  }
}


void clamp_release() {
  for (int pos = 90; pos < 170; pos++) {
    arm.write(pos);
    delay(15);
  }
}


float ultrassonic_data() {
  Serial.println(sonar.ping_cm());
}
