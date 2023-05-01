import socket, ssl, os
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import subprocess

# generate a new RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# create a self-signed certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, "www.example.com")
])
certificate = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName("www.example.com")]),
    critical=False,
).sign(private_key, hashes.SHA256(), default_backend())

# save the certificate and private key to files
with open("server.crt", "wb") as f:
    f.write(certificate.public_bytes(encoding=serialization.Encoding.PEM))
with open("server.key", "wb") as f:
    f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()))

# load the certificate and key files
certfile = "server.crt"
keyfile = "server.key"

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host and port
host = "10.128.0.7"
port = 12345
server_socket.bind((host, port))

# configure the server to listen for incoming connections
server_socket.listen(1)

# create an SSL context with TLS 1.3
context = ssl.SSLContext(ssl.PROTOCOL_TLS)

# load a self-signed certificate
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# accept connections from clients
while True:
    print("Waiting for client connection...")
    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")

    # wrap the socket in an SSL context
    ssl_socket = context.wrap_socket(client_socket, server_side=True)


    # receive data from the client and add the token to the tokens file
    data = ssl_socket.recv(1024)
    if data:
        message = data.decode("utf-8")
        if message != "Hello, server!":  # check if the message is not "hello server"
            print(f"Received token: {message}")
                    # Open the HTML file in read mode
            with open("/home/esrom/Desktop/web/index.html", "r") as f:
                content = f.read()

# Insert a new paragraph containing the word "Hello"
            new_content = content.replace("</body>", "<p>"+message+"</p>\n</body>")

# Open the HTML file in write mode and overwrite the old content
            with open("/home/esrom/Desktop/web/index.html", "w") as f:
                 f.write(new_content)
                 subprocess.run(["git", "add", "."])
                 subprocess.run(["git", "commit", "-m", "changes"])
                 subprocess.run(["git", "push"])
                           

    # close the SSL connection and the client socket
    ssl_socket.close()
    client_socket.close()
