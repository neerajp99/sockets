import socket 
import threading 

PORT = 8080 
SERVER = socket.gethostbyname(socket.gethostname())

# Tuple with port and server 
ADDR = (SERVER, PORT)

# Header to check the number of bytes, initially of length 64
HEADER = 64 

FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT"

# What type of IP we are going to accept  and using sock.STREAM means we are going to stream data 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server.bind(ADDR)

# Store all message of clients respectively 

def handleClient(connection, address):
    print(f"[New Connection:] {address} connected!!")

    connected = True 
    while connected:
        # Message received with adding the number of bytes we wants from the client
        message_length = connection.recv(HEADER).decode(FORMAT)

        # We receive nothing (invalid) the first time, so we make sure it is an actual message 
        if message_length:
            message_length = int(message_length)

            message = connection.recv(message_length).decode(FORMAT)

            # Disconnect if we get the !disconnect message 
            if message == DISCONNECT_MESSAGE:
                connected = False 

            print(f"[{address}] {message}")

            # Sending message back to the client 
            connection.send("Message Received".encode(FORMAT))

    connection.close()


def methodStart():
    server.listen()

    print(f"Server is listening on: {SERVER} ")

    while True:
        connection, address = server.accept()
        thread = threading.Thread(target = handleClient, args = (connection, address))
        thread.start()

        # Count the number of active threads 
        print(f"[ACTIVE THREADS] {threading.activeCount() - 1}")


print('Starting server....')
methodStart()