import socket 
import threading 
import pickle
from datetime import datetime, time 
import re
import getmac

PORT = 5545
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

# Global dictionary to store sessions 
global_sessions_dict = dict()
sessions = list()

# Method to process the client's response 
def process_request(value, mac_address, ip, connection):
    # For case 1
    if (value == "3"):
        connection.send('Disconnecting now....'.encode(FORMAT))
        return False 
    
    # For case 2 
    if (value == "1"):
        # Check if the user has already taken the MCQ Test 
        if mac_address in sessions:
            connection.send("!DISCONNECT".encode(FORMAT))
            return False 

        # Get the time verification
        current = check_time()

        # If current time is between start and end time 
        if current:
            mcq_question = f"Who invented the World Wide Web? \n (1) Vincent Cerf \n (2) Tim Bernes-Lee \n (3) Guido Van Rossum \n (4) Garett Camp \n \n Choose an option among 1, 2, 3 or 4."
            # Send mcq question to the client to fetch a answer 
            connection.send(mcq_question.encode(FORMAT))
            # Get mcq response 
            mcq_message_length = connection.recv(HEADER).decode(FORMAT)
            mcq_message_length = int(mcq_message_length)
            mcq_message = connection.recv(mcq_message_length).decode(FORMAT)
            print(f"MCQ response received: {mcq_message}")

            # Add results to the global sessions lost and object 
            sessions.append(mac_address)
            global_sessions_dict[mac_address] = mcq_message 
            # Return a standard response 
            connection.send(f"Thank you for participating. Your response is registered against your MAC address: {mac_address}".encode(FORMAT))
        
        return False

    # For case 3
    if (value == "2"):
        current = check_is_end_time() 
        print('CURRENT', current)

        if current:
            mcq_responses = "CHECK RESPONSE"
            connection.send(mcq_responses.encode(FORMAT))
        else:
            connection.send("Kindly wait until 04:20 for the report!".encode(FORMAT))

        return False

    # Else case 
    else:
        connection.send("Invalid Input, please tray again later!".encode(FORMAT))


# Method to check if time exists between two timings
def check_time(start = time(11, 50), end = time(22, 20), current = None):
    # Get current timestamp 
    current = datetime.now().time() or current 

    # Return if the time is between start and end time 
    return current >= start and current <= end 

# Method to check if the time is greater than the end time 
def check_is_end_time(end = time(22, 20), current = None):
    # Get current timestamp
    current = datetime.now().time() or current 

    # Return true or false 
    return current > end

# Method to handle requests 
def handleClient(connection, address, mac_address):
    print(f"[New Connection:] {address} connected!!")

    connected = True 
    while connected:
        # Message received with adding the number of bytes we wants from the client
        message_length = connection.recv(HEADER).decode(FORMAT)

        # We receive nothing (invalid) the first time, so we make sure it is an actual message 
        if message_length:
            message_length = int(message_length)

            message = connection.recv(message_length).decode(FORMAT)

            print(f'Message: {message}')

            # Disconnect if we get the !disconnect message 
            if message == DISCONNECT_MESSAGE:
                connected = False 
                connection.send("You are disconnected now!!".encode(FORMAT))
            else:
                # Print the client credentials
                print(f"[{address}] {message}")

                process_request(message, mac_address, address, connection)
    connection.close()

# Method to start the threads
def methodStart():
    server.listen()
    print(f"Server is listening on: {SERVER} ")

    while True:
        connection, address = server.accept()
        connection.send('We are running a quiz. \n You can participant in the quiz any time between 2:50 PM - 4:20 PM.  \n Reply with a ”1” if you want to participate now (time of connection must be between 2:50 PM - 4:20 PM); with a ”2” if you want to see the results (time of connection must be after 4:20 PM); and with ”3” otherwise.'.encode(FORMAT))
        mac_address = getmac.get_mac_address()
        thread = threading.Thread(target = handleClient, args = (connection, address, mac_address))
        thread.start()

        # Count the number of active threads 
        print(f"[ACTIVE THREADS] {threading.activeCount() - 1}")


print('Starting server....')
methodStart()