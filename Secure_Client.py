try:
    import socket
    # Cryptography Libraries
    from secrets import choice
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
    challengep = [choice([chr(i) for i in range(32, 127)]) for i in range(64)]
    challengep = ''.join(challengep)
    challengep = challengep.encode()
    sessionkey = Fernet.generate_key()
    session = Fernet(sessionkey)
    pub_key = int(connection.recv(65537).decode())
    server_rsa = PKCS1_OAEP.new(RSA.RsaKey(n=pub_key, e=65537))
    challenge = server_rsa.encrypt(challengep)
    connection.send(server_rsa.encrypt(sessionkey))
    connection.send(challenge)
    server_challenge = connection.recv(1024)
    if server_challenge != challengep:
        raise OSError('Server failed to decrypt the challenge.')
        return None
    else:
        return SecureSession(connection=connection, session=session)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 7000))
    secure_conn = init_session(sock)
    print(secure_conn.recv(1024).decode())
    secure_conn.close()
