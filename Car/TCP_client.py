import socket
import threading
import pickle
import datetime

s_data = {'pass' : 0} #우회전 유무 패킷

def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        r_time = datetime.datetime.now().strftime("%H:%M:%S")
        r_data = pickle.loads(data)
        print(f"\n>> HOST의 message : {r_data} ({r_time})")

#TCP 연결
def connect_TCP(HOST, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    recv_thread = threading.Thread(target=recv_data, args=(client_socket,))
    recv_thread.start()
    print('>> Connect Server')
    
    while True:
        global s_data
        
        pass_v = input("Enter value for pass : ")   #건너는 유무 판단 - 추후 버튼으로 수정
        
        s_data['pass'] = pass_v
        
        s_time = datetime.datetime.now().strftime("%H:%M:%S")
        data = pickle.dumps([s_data, s_time])
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
