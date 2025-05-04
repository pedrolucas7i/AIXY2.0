/*
===========================================================================================================================================
===========================================================================================================================================
                                                                  HARDWARE CONTROLER CODE
===========================================================================================================================================
===========================================================================================================================================
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

#define PIN_MOTOR1_IN1 3                      // Pin responsible for motor1 clockwise control
#define PIN_MOTOR2_IN1 4                      // Pin responsible for motor2 clockwise control
#define PIN_MOTOR1_IN2 5                      // Pin responsible for counterclockwise control
#define PIN_MOTOR2_IN2 6                      // Pin responsible for counterclockwise control

int backward_pwm = 175;

void setup() {
  pinMode(PIN_MOTOR1_IN1, OUTPUT);            // Defining PIN's as ouptuts
  pinMode(PIN_MOTOR1_IN2, OUTPUT);            // Defining PIN's as ouptuts
  pinMode(PIN_MOTOR2_IN1, OUTPUT);            // Defining PIN's as ouptuts
  pinMode(PIN_MOTOR2_IN2, OUTPUT);            // Defining PIN's as ouptuts
  Serial.begin(9600);                         // Start Serial comunication in 9600 bauds
  
}

void loop() {
  

}


void drive_forward() {
  digitalWrite(PIN_MOTOR1_IN2, LOW);          // Send to PIN 0V
  digitalWrite(PIN_MOTOR2_IN2, LOW);          // Send to PIN 0V
  digitalWrite(PIN_MOTOR1_IN1, HIGH);         // Send to PIN ~5V
  digitalWrite(PIN_MOTOR2_IN1, HIGH);         // Send to PIN ~5V
  delay(1000);                                // Execute the action for 1000ms
}


void drive_backward() {
  digitalWrite(PIN_MOTOR1_IN1, LOW);          // Send to PIN ~5V
  digitalWrite(PIN_MOTOR2_IN1, LOW);          // Send to PIN ~5V
  analogWrite(PIN_MOTOR1_IN2, backward_pwm);  // Send to PIN backward_pwm PWM VALUE
  analogWrite(PIN_MOTOR2_IN2, backward_pwm);  // Send to PIN backward_pwm PWM VALUE
  delay(1000);                                // Execute the action for 1000ms
}


void drive_left() {
  digitalWrite(PIN_MOTOR1_IN1, LOW);          // Send to PIN 0V
  digitalWrite(PIN_MOTOR2_IN1, HIGH);         // Send to PIN ~5V
  digitalWrite(PIN_MOTOR1_IN2, HIGH);         // Send to PIN ~5V
  digitalWrite(PIN_MOTOR2_IN2, LOW);          // Send to PIN 0V
  delay(700);                                 // Execute the action for 700ms
}

void drive_right() {
  digitalWrite(PIN_MOTOR1_IN1, HIGH);         // Send to PIN ~5V
  digitalWrite(PIN_MOTOR2_IN1, LOW);          // Send to PIN 0V
  digitalWrite(PIN_MOTOR1_IN2, LOW);          // Send to PIN 0V
  digitalWrite(PIN_MOTOR2_IN2, HIGH);         // Send to PIN ~5V
  delay(700);                                 // Execute the action for 700ms
}
