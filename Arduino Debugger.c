// Define the GPIO pins you want to control
const int gpio_pins[] = {2, 3, 4}; // Replace with the actual GPIO pins you want to use

void setup() {
  // Initialize GPIO pins as outputs
  for (int i = 0; i < sizeof(gpio_pins) / sizeof(gpio_pins[0]); i++) {
    pinMode(gpio_pins[i], OUTPUT);
    digitalWrite(gpio_pins[i], LOW);
  }
  
  // Initialize Serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();

    if (message.startsWith("ON ")) {
      int pin_number = message.substring(3).toInt();
      if (isValidPin(pin_number)) {
        digitalWrite(pin_number, HIGH);
        Serial.println("OK");
      } else {
        Serial.println("Invalid Command");
      }
    } else if (message.startsWith("OFF ")) {
      int pin_number = message.substring(4).toInt();
      if (isValidPin(pin_number)) {
        digitalWrite(pin_number, LOW);
        Serial.println("OK");
      } else {
        Serial.println("Invalid Command");
      }
    } else {
      Serial.println("Invalid Command");
    }
  }
}

bool isValidPin(int pin) {
  for (int i = 0; i < sizeof(gpio_pins) / sizeof(gpio_pins[0]); i++) {
    if (gpio_pins[i] == pin) {
      return true;
    }
  }
  return false;
}
