import socket
import threading
import datetime
import pickle
import time

client_sockets = []
client_sockets_lock = threading.Lock()

# 서버 호스트의 ip주소 알아옴
HOST = socket.gethostbyname(socket.gethostname())
PORT1 = 9999  # broadcast port
PORT2 = 8261  # tcp 연결을 위한 port

s_data = {'remain': 0, 'plus': 0}

right = 0   #차량이 우회전 하는지 안하는지 flag

def broadcast_UDP():
    while True:
        # UDP 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Broadcast 메시지 전송
        message = "Host ip 전송중, 차량 검색중"
        split_address = HOST.split('.')
        split_address = split_address[:3]
        broadcast_ip_address = '.'.join(split_address)
        broadcast_ip_address += '.255'
        sock.sendto(message.encode(), (broadcast_ip_address, PORT1))
        print(message)
        time.sleep(5)  # 5초마다 전송


# 클라이언트 메시지 받는 스레드
def server_message_receive(client_socket, addr):
    print(f'>> {addr[0]}({addr[1]})와 연결완료.')

    while True:
        global s_data, right
        data = client_socket.recv(1024)

        r_time = datetime.datetime.now().strftime("%H:%M:%S")
        r_data = pickle.loads(data)
        print(f">> {addr[0]}({addr[1]})의 message : {r_data} ({r_time})")

        if r_data[0]['pass'] == '1':    #우회전 한다고 표시
            right = 1    #right 변수 1로 설정

    client_socket.close()
    client_sockets[:] = [c for c in client_sockets if c != client_socket]


# 서버에서 메시지 입력하는 경우
def server_message_input():
    while True:
        global right

        if right == 1:  #우회전 하는 상황일때 차량에게 패킷 전송
            send_message_to_clients()  # 입력된 메시지를 모든 클라이언트에게 전송
            right = 0   #다시 right 0으로 초기화 시켜야 오류가 안생김 (즉 지속적으로 차량은 우회전하는 신호를 계속 줘야함)


# 서버와 연결된 모든 클라이언트에게 메시지 전달
def send_message_to_clients():
    with client_sockets_lock:
        global s_data

        for client in client_sockets:
            s_time = datetime.datetime.now().strftime("%H:%M:%S")
            data = pickle.dumps([s_data, s_time])
            client.sendall(data)


print('>> Server Start with ip :', HOST)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT2))
server_socket.listen()


def client_acceptance():
    try:
        while True:
            print('>> Wait')
            client_socket, addr = server_socket.accept()
            with client_sockets_lock:
                client_sockets.append(client_socket)
            threading.Thread(target=server_message_input).start()  # 서버 메시지 전송 (서버 -> 클라이언트)
            threading.Thread(target=server_message_receive,
                             args=(client_socket, addr)).start()  # 클라이언트 메시지 스레드 (클라이언트 -> 서버)
            print("참가자 수 : ", len(client_sockets))

    finally:
        server_socket.close()
        with client_sockets_lock:
            for client_socket in client_sockets:
                client_socket.close()


threading.Thread(target=broadcast_UDP).start()  # broadcast 쓰레드
threading.Thread(target=client_acceptance).start()  # 클라이언트 연결 대기 쓰레드
