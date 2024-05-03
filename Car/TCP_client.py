import socket
import threading
import pickle

def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        print("recive : ", pickle.loads(data))

#TCP 연결
def connect_TCP(HOST, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("hi")
    
    recv_thread = threading.Thread(target=recv_data, args=(client_socket,))
    recv_thread.start()
    print('>> Connect Server')
    
    while True:
        message = input()
        data = pickle.dumps([message])
        if message == 'quit':
            close_data = message
            break

        client_socket.sendall(data)

    client_socket.close()

#UDP로부터 ip주소 얻고
def recv_UDP_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 9999))
    data, addr = sock.recvfrom(1024)
    
    HOST = addr[0]  # broadcast로 HOST ip를 받아옴
    PORT = 8261
    
    connect_TCP(HOST, PORT)
