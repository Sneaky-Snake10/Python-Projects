# Import necessary libraries 
import socket
import RPi.GPIO as GPIO

# Define the GPIO pins you want to control
GPIO.setmode(GPIO.BCM)
gpio_pins = [17, 18, 19]  # Replace with the actual GPIO pins you want to use

# Setup GPIO pins as outputs
for pin in gpio_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Define the IP and port for the socket server
host = 'your_server_ip_here'
port = 12345  # Replace with the desired port number

# Function to handle incoming messages
def handle_message(message, client_socket):
    try:
        command, pin_number = message.split()
        pin_number = int(pin_number)

        # Check if the command is 'ON'
        if command == 'ON':
            # Check if the pin_number is valid
            if pin_number in gpio_pins:
                # Turn on the GPIO pin
                GPIO.output(pin_number, GPIO.HIGH)
                # Send 'OK' back to the client
                client_socket.send(b'OK')
            else:
                # Send 'Invalid Command' if the pin is not in the list
                client_socket.send(b'Invalid Command')
        # Check if the command is 'OFF'
        elif command == 'OFF':
            # Check if the pin_number is valid
            if pin_number in gpio_pins:
                # Turn off the GPIO pin
                GPIO.output(pin_number, GPIO.LOW)
                # Send 'OK' back to the client
                client_socket.send(b'OK')
            else:
                # Send 'Invalid Command' if the pin is not in the list
                client_socket.send(b'Invalid Command')
        else:
            # Send 'Invalid Command' for any other command
            client_socket.send(b'Invalid Command')
    except ValueError:
        # Send 'Invalid Command' if the message format is incorrect
        client_socket.send(b'Invalid Command')

# Main function to run the script
def main():
    while True:
        try:
            # Create a socket and attempt to connect
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                # Handle incoming messages
                handle_message(data.strip(), client_socket)

        except (socket.error, ConnectionResetError):
            print("Socket error. Attempting to reconnect...")
            continue
        except KeyboardInterrupt:
            break
        finally:
            # Close the socket and clean up GPIO pins
            client_socket.close()
            GPIO.cleanup()

if __name__ == "__main__":
    main()
