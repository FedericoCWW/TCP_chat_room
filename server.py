import threading, socket
from colorama import Fore, Back, Style

host = '127.0.0.1'      #local host
port = 45572

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print(f'{nickname} disconected')
            broadcast(f'{nickname} left the the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(Fore.GREEN + f'Connected with {str(address)}')
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(Fore.CYAN + f'Nickname: {nickname} connected')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('connected to the server'.encode('ascii'))
        #parte threading
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print(Fore.GREEN + "server is listening...")
receive()           #recieve seria el main