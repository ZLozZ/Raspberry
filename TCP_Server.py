import socket
from threading import Thread

LocalIP = "0.0.0.0" #server không quan tâm đến server
localPort = 20000
bufferSize = 1024
msgToClient = "Hello TCP Client"
bytesToSend = str.encode(msgToClient)

def new_client(conn, addr):
    while True:
        ClientMsg = conn.recv(bufferSize)
        if not ClientMsg:
            break
        message = "Message from Client: {}".format(ClientMsg)
        print(message)
        conn.sendall(bytesToSend)
        print("End connection from {}".format(addr))
        conn.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((LocalIP, localPort))
sock.listen(1)
i = 0
while True:
    i=i+1
    conn, addr = sock.accept()
    print("Got connection from {}".format(addr))
    Thread(target=new_client, args=(conn, addr)).start()
    print(i)