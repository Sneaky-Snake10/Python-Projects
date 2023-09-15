# This code is by Krishna Ganta, student of Northshore School District, student ID 2032673.

# Try to import the necessary libraries
try:
    import socket
    # Cryptography Libraries
    from Crypto.PublicKey import RSA
    from cryptography.fernet import Fernet
    from Crypto.Cipher import PKCS1_OAEP

except ImportError:
    # Inform the user of the missing libraries
    raise OSError('The neccasary libraries are not found. Make sure that socket, pycryptodome and cryptography are installed.')

# Define SecureSession Class
class SecureSession:
    # This class is an interface to the encrypted connection, that acts like the "socket" object, but also performs the encryption.
    def __init__(this, connection, session):
        this.connection = connection
        this.session = session
        this.closed = False
    
    def send(this, data):
        if this.closed:
            # Reference to the socket library socket closed error, "An operation was attempted on something that is not a socket."
            raise OSError('An operation was attempted on something that is not a connection.')
         # If it is not closed, encrypt and send the data. Similar to the socket library, it accepts a bytes-like object.
        this.connection.send(this.session.encrypt(data))
        return len(this.session.encrypt(data))
    def recv(this, bytes):
        if this.closed:
            # Reference to the socket library socket closed error, "An operation was attempted on something that is not a socket."
            raise OSError('An operation was attempted on something that is not a connection.')
         # If it is not closed, then return the decrypted bytes. Similar to the socket library, it returns a bytes-like object.
        return this.session.decrypt(this.connection.recv(bytes))
    
    def close(this):
        # Set the closed flag, and close the TCP connection.
        this.closed = True
        this.connection.close()
        return None
# Define Session Generator
def init_session(connection):
    # Give the client the server's public key.
    connection.send(str(public_key.n).encode())
    # Decrypt the session key for this connection.
    sessionkey = secret.decrypt(connection.recv(1048576))
    # Decrypt the client's challenge, and send back the bytes.
    connection.send(secret.decrypt(connection.recv(1024)))
    # Generate a Fernet object to pass to the SecureSession.
    session = Fernet(sessionkey)
    # Return a Session object, that performs encryption/decryption with the newly established symmetric session key.
    return SecureSession(connection=connection, session=session)
# RSA Key Generation
private_key = RSA.generate(2048)
public_key = private_key.publickey()
# Set up the two keys with objects that will perform encryption/decryption with them.
cipher = PKCS1_OAEP.new(public_key)
secret = PKCS1_OAEP.new(private_key)

if __name__ == '__main__':
    # Demonstration of how to use this script. Here, the variable "secure_conn" is the SecureSession object, and provides an interface into the encrypted connection.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 7000))
    sock.listen(1)
    conn, _ = sock.accept()
    secure_conn = init_session(conn)
    secure_conn.send(b'The session was initialized successfully. All required libraries are installed.')
    secure_conn.close()
