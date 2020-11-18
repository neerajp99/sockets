import socket 

PORT = 8080 
SERVER = socket.gethostbyname(socket.gethostname())

# Tuple with port and server 
ADDR = (SERVER, PORT)

# Header to check the number of bytes, initially of length 64
HEADER = 64 

FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

# Method to send message to the server 
def send_message(message):
    message = message.encode(FORMAT)
    message_length = len(message)

    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

    # Print the message received back from the server 
    print(client.recv(2048).decode(FORMAT))

send_message('Hello bitches!')
send_message('Hello asses!!')

send_message(DISCONNECT_MESSAGE)