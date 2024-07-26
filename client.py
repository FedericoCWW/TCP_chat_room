import socket, threading
import colorama

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 45572))

nickname = input("choose a nickame: ")

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(msg)
        except:
            print("An error happened!")
            client.close()
            break

def write():
    while True:
        nick_msg = input("")
        msg = f'{nickname}: {nick_msg}'
        client.send(msg.encode('ascii'))

recieve_thread = threading.Thread(target=receive)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
