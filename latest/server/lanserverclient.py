import socket
import threading
import sys

# Funzione per la lettura dei dati dal server
def receive_data(sock):
    while True:
        try:
            data = sock.recv(1024)
        except socket.error:
            break
        if not data:
            break
        print(f"Received: {data.decode()}")

# Funzione per l'invio dei dati al server
def send_data(sock):
    while True:
        data = input("")
        if data == "quit":
            break
        try:
            sock.sendall(data.encode())
        except socket.error:
            break

# Connessione al server
host, port = sys.argv[1], int(sys.argv[2])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
print(f"Connected to {host}:{port}")

# Avvio dei thread di lettura e scrittura
recv_thread = threading.Thread(target=receive_data, args=(sock,))
recv_thread.start()
send_thread = threading.Thread(target=send_data, args=(sock,))
send_thread.start()

# Attende la fine dei thread di lettura e scrittura
recv_thread.join()
send_thread.join()

# Chiude la connessione
sock.close()
print("Connection closed")

