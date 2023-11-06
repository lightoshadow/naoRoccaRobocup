import bluetooth
import threading
import queue
import socket

# Lista clients bluetooth connessi
bluetooth_clients = []

# Funzione per la ricezione di dati nel client tcp
def receive_tcp_data(sock, btsock):
    while True:
        try:
            data = sock.recv(2048)
        except socket.error:
            break
        if not data:
            break
        print(data.decode())
        for client in bluetooth_clients:
            client.send(data)


# Funzione che viene eseguita in un thread separato per gestire le connessioni in arrivo
def handle_client(client_socket, client_info, queue):
    bluetooth_clients.append(client_socket)
    try:
        # Riceve i dati dal client finché non viene chiusa la connessione
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            queue.put((client_info[0], data))
    except OSError:
        pass
    finally:
        bluetooth_clients.remove(client_socket)
        client_socket.close()

# Funzione che viene eseguita in un thread separato per gestire i dati ricevuti
def handle_data(queue):
    while True:
        client_info, data = queue.get()
        print("[{}] {}".format(client_info, data.decode("utf-8")))


# Inizializza il socket Bluetooth
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))
server_socket.listen(1)

# Inizializza il socket TCP per la connessione al server in localhost
localhost_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 8080
localhost_client.connect((host, port))
print(f'Connected to {host}:{port}')

# Avvia un thread separato per gestire la parte di TCP
recv_thread = threading.Thread(
    target=receive_tcp_data, args=(localhost_client, server_socket))
recv_thread.start()

# Stampa l'indirizzo del server per permettere ai client di connettersi
print("In attesa di connessioni su: {}".format(server_socket.getsockname()))

# Crea una coda per gestire i dati ricevuti dai client
data_queue = queue.Queue()

# Avvia un thread separato per gestire i dati ricevuti
data_thread = threading.Thread(target=handle_data, args=(data_queue,))
data_thread.start()

# Accetta connessioni in un loop infinito
while True:
    # Accetta una connessione
    client_socket, client_info = server_socket.accept()
    print("Connessione accettata da: {}".format(client_info[0]))

    # Avvia un nuovo thread per gestire la connessione
    client_thread = threading.Thread(target=handle_client, args=(
        client_socket, client_info, data_queue))
    client_thread.start()

