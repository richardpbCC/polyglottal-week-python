import socket
import threading

HOST = '127.0.0.1'  # ipconfig
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []


# broadcast

def broadcast(message):
    for client in clients:
        client.send(message)


# handle

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            nickname = nicknames[index]
            print(f"{nickname} has disconnected") 
            clients.remove(client)            
            client.close()            
            nicknames.remove(nickname)
            break


# receive

def receive():
    while True:
        client, address = server.accept()        
        print(f"Connected with {str(address)}")

        client.send('request to connect'.encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}\n".encode('utf-8'))
        broadcast(f"{nickname} connected to the server\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print(f"Server listening on port {PORT}")
receive()
