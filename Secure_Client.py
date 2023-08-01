# Try to import the necessary libraries
try:
    import socket
    # Cryptography Libraries
    from secrets import choice
    from Crypto.PublicKey import RSA
    from cryptography.fernet import Fernet
    from Crypto.Cipher import PKCS1_OAEP

except ImportError:
    # Inform the user of the missing libraries
    raise OSError('The neccasary libraries are not found. Make sure that socket, secrets, pycryptodome and cryptography are installed.')

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
        # Return the number of bytes sent.
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
    # The challengep variable refers to the plaintext of the challenge. These lines generate the challenge.
    challengep = [choice([chr(i) for i in range(32, 127)]) for i in range(64)]
    challengep = ''.join(challengep)
    challengep = challengep.encode()
    # Set a symmetric key for the current session.
    sessionkey = Fernet.generate_key()
    session = Fernet(sessionkey)
    # Read the server's public key.
    pub_key = int(connection.recv(65537).decode())
    server_rsa = PKCS1_OAEP.new(RSA.RsaKey(n=pub_key, e=65537))
    # Encrypt and send the challenge. If the server really has the public key they claim they have, they will be able to decrypt it and send it back.
    challenge = server_rsa.encrypt(challengep)
    # Also send the session key.
    connection.send(server_rsa.encrypt(sessionkey))
    connection.send(challenge)
    server_challenge = connection.recv(1024)
    # Check if the server decrypted the challenge successfully.
    if server_challenge != challengep:
        # If the server is impersonating another, inform the user.
        raise OSError('Server failed to decrypt the challenge.')
        return None
    else:
        # If the server passed all the tests, return a Session object, that performs encryption/decryption with the symmetric key.
        return SecureSession(connection=connection, session=session)

if __name__ == '__main__':
    # Demonstration of how to use this script. Here, the variable "secure_conn" is the SecureSession object, and provides an interface into the encrypted connection.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 7000))
    secure_conn = init_session(sock)
    print(secure_conn.recv(1024).decode())
    secure_conn.close()
