// Define the GPIO pins you want to control
const int gpio_pins[] = {2, 3, 4}; // Replace with the actual GPIO pins you want to use

void setup() {
  // Initialize GPIO pins as outputs
  for (int i = 0; i < sizeof(gpio_pins) / sizeof(gpio_pins[0]); i++) {
    pinMode(gpio_pins[i], OUTPUT);
    digitalWrite(gpio_pins[i], LOW); // Set pins to LOW (OFF) initially
  }
  
  // Initialize Serial communication at 9600 baud rate
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming message until a newline character is received
    String message = Serial.readStringUntil('\n');
    message.trim(); // Remove leading/trailing whitespace

    // Check if the message starts with "ON "
    if (message.startsWith("ON ")) {
      // Extract the pin number from the message and convert it to an integer
      int pin_number = message.substring(3).toInt();
      
      // Check if the pin number is valid
      if (isValidPin(pin_number)) {
        // Turn on the specified GPIO pin
        digitalWrite(pin_number, HIGH);
        // Send "OK" back to the sender
        Serial.println("OK");
      } else {
        // Send "Invalid Command" if the pin is not in the list
        Serial.println("Invalid Command");
      }
    }
    // Check if the message starts with "OFF "
    else if (message.startsWith("OFF ")) {
      // Extract the pin number from the message and convert it to an integer
      int pin_number = message.substring(4).toInt();
      
      // Check if the pin number is valid
      if (isValidPin(pin_number)) {
        // Turn off the specified GPIO pin
        digitalWrite(pin_number, LOW);
        // Send "OK" back to the sender
        Serial.println("OK");
      } else {
        // Send "Invalid Command" if the pin is not in the list
        Serial.println("Invalid Command");
      }
    }
    // If the message format is not recognized
    else {
      Serial.println("Invalid Command");
    }
  }
}

// Function to check if a pin number is valid
bool isValidPin(int pin) {
  for (int i = 0; i < sizeof(gpio_pins) / sizeof(gpio_pins[0]); i++) {
    // Compare the pin number with the elements in the gpio_pins array
    if (gpio_pins[i] == pin) {
      return true; // The pin is valid
    }
  }
  return false; // The pin is not valid
}
