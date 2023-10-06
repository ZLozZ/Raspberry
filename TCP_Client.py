import socket
from time import sleep

ServerAddress = "192.168.1.16" #địa chỉ IP của server
ServerPort = 20000 #port chọn những port chưa có nào dùng
bufferSize = 1024
msgToSever = "Hello TCP Server"
byteToSend = str.encode(msgToSever)


while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ServerAddress,ServerPort))

    sock.sendall(byteToSend)

    ServerMsg = sock.recv(bufferSize)

    message = "Message from Server: {}".format(ServerMsg)
    print(message)
    sock.close()
    sleep(5)