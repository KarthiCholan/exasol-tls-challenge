import ssl
import socket
import hashlib
import random
import string

# === Configuration ===
HOST = "18.202.148.130"
PORT = 3336

CLIENT_CERT_FILE = "client.crt"
CLIENT_KEY_FILE = "client.key"
CA_CERT_FILE = "ca.crt"

# === Helper Functions ===

def sha1sum(data):
    return hashlib.sha1(data.encode('utf-8')).hexdigest()

def random_string(length=8):
    chars = ''.join(c for c in string.printable if c not in '\n\r\t ')
    return ''.join(random.choice(chars) for _ in range(length))

def create_tls_connection():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT_FILE)
    context.load_cert_chain(certfile=CLIENT_CERT_FILE, keyfile=CLIENT_KEY_FILE)
    context.check_hostname = False  # Disable hostname verification
    context.verify_mode = ssl.CERT_REQUIRED

    raw_sock = socket.create_connection((HOST, PORT))
    tls_sock = context.wrap_socket(raw_sock, server_hostname=HOST)
    return tls_sock

def handle_server():
    sock = create_tls_connection()
    authdata = ""

    try:
        while True:
            data = sock.recv(4096).decode('utf-8')
            if not data:
                break

            lines = data.strip().split('\n')
            for line in lines:
                print("Server:", line)
                args = line.strip().split(' ')
                cmd = args[0]

                if cmd == "HELO":
                    sock.sendall(b"TOAKUEI\n")

                elif cmd == "ERROR":
                    print("ERROR: " + " ".join(args[1:]))
                    return

                elif cmd == "POW":
                    authdata, difficulty = args[1], int(args[2])
                    while True:
                        suffix = random_string()
                        hash_result = sha1sum(authdata + suffix)
                        if hash_result.startswith("0" * difficulty):
                            sock.sendall((suffix + "\n").encode('utf-8'))
                            break

                elif cmd == "END":
                    sock.sendall(b"OK\n")
                    return

                elif cmd == "NAME":
                    sock.sendall((sha1sum(authdata + args[1]) + " " + "KeerthiKannan R\n").encode('utf-8'))

                elif cmd == "MAILNUM":
                    sock.sendall((sha1sum(authdata + args[1]) + " 2\n").encode('utf-8'))

                elif cmd == "MAIL1":
                    sock.sendall((sha1sum(authdata + args[1]) + " keerthikannan@example.com\n").encode('utf-8'))

                elif cmd == "MAIL2":
                    sock.sendall((sha1sum(authdata + args[1]) + " keerthi.dev@example.com\n").encode('utf-8'))

                elif cmd == "SKYPE":
                    sock.sendall((sha1sum(authdata + args[1]) + " keerthikannan.skype\n").encode('utf-8'))

                elif cmd == "BIRTHDATE":
                    sock.sendall((sha1sum(authdata + args[1]) + " 01.01.1990\n").encode('utf-8'))

                elif cmd == "COUNTRY":
                    sock.sendall((sha1sum(authdata + args[1]) + " India\n").encode('utf-8'))

                elif cmd == "ADDRNUM":
                    sock.sendall((sha1sum(authdata + args[1]) + " 2\n").encode('utf-8'))

                elif cmd == "ADDRLINE1":
                    sock.sendall((sha1sum(authdata + args[1]) + " 123 Main Street\n").encode('utf-8'))

                elif cmd == "ADDRLINE2":
                    sock.sendall((sha1sum(authdata + args[1]) + " Chennai 600001\n").encode('utf-8'))

    finally:
        sock.close()

if __name__ == "__main__":
    handle_server()
