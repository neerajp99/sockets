import socket 

PORT = 5545
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = '192.168.0.100'

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

# sPrint the initial common message received.
print(client.recv(2048).decode(FORMAT))

# Take user input
print('\n') 
value = input('Your choice: ')

# Send the value to the server to process 
send_message(value)

first_statements = {
    "!DISCONNECT-one": "You have already taken the MCQ Test. Kindly wait until 4:20PM for the report.",
    "!DISCONNECT-two": "Kindly wait for the MCQ to start at 2:50.",
    "!DISCONNECT-three": "The MCQ is already over! Check back later for the next one."
}

if (value == '1'):
    # Receive MCQ options from the server and print it
    mcq = client.recv(2048).decode(FORMAT)
    if mcq in first_statements:
        print(first_statements[mcq])
    else:
        print(mcq)
        # Get mcq response from the user 
        mcq_choice = str(input("Your choice: "))
        # Send mcq response to the server 
        send_message(mcq_choice)
        print(client.recv(2048).decode(FORMAT))
else:
    # Print the final outcome from the server 
    print(client.recv(2048).decode(FORMAT))

send_message(DISCONNECT_MESSAGE)