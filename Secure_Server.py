try:
    import socket
    # Cryptography Libraries
    from Crypto.PublicKey import RSA
    from cryptography.fernet import Fernet
    from Crypto.Cipher import PKCS1_OAEP

except ImportError:
    raise OSError('The neccasary libraries are not found. Make sure that socket, pycryptodome and cryptography are installed.')

# Define SecureSession Class
class SecureSession:
    def __init__(this, connection, session):
        this.connection = connection
        this.session = session
        this.closed = False
    
    def send(this, data):
        if this.closed:
            # Reference to the socket library socket closed error, "An operation was attempted on something that is not a socket."
            raise OSError('An operation was attempted on something that is not a connection.')
        this.connection.send(this.session.encrypt(data))
        return len(this.session.encrypt(data))
    def recv(this, bytes):
        if this.closed:
            # Reference to the socket library socket closed error, "An operation was attempted on something that is not a socket."
            raise OSError('An operation was attempted on something that is not a connection.')
        return this.session.decrypt(this.connection.recv(bytes))
    
    def close(this):
        this.closed = True
        return None
# Define Session Generator
def init_session(connection):
    connection.send(str(public_key.n).encode())
    sessionkey = secret.decrypt(connection.recv(1048576))
    connection.send(secret.decrypt(connection.recv(1024)))
    session = Fernet(sessionkey)
    return SecureSession(connection=connection, session=session)
# RSA Key Generation
private_key = RSA.generate(2048)
public_key = private_key.publickey()
cipher = PKCS1_OAEP.new(public_key)
secret = PKCS1_OAEP.new(private_key)
# Demonstration of library, does not run when imported.
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 7000))
    sock.listen(1)
    conn, _ = sock.accept()
    secure_conn = init_session(conn)
    secure_conn.send(b'The session was initialized successfully. All required libraries are installed.')
    secure_conn.close()