import socket
import threading

HOST = '127.0.0.1'  # ipconfig
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
usernames = []


# broadcast

def broadcast(message):
    for client in clients:
        client.send(message)


# handle

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{usernames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            username = usernames[index]
            print(f"{username} has disconnected") 
            clients.remove(client)            
            client.close()            
            usernames.remove(username)
            break


# receive

def receive():
    while True:
        client, address = server.accept()        
        print(f"Connected with {str(address)}")

        client.send('request to connect'.encode('utf-8'))
        username = client.recv(1024)

        usernames.append(username)
        clients.append(client)
        
        print(f"Username of the client is {username}".encode('utf-8'))
        # broadcast(f"{username} connected to the server".encode('utf-8'))
        # client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print(f"Server listening on port {PORT}")
receive()
