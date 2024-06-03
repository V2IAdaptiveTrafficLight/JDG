import RPi.GPIO as GPIO
import time
import socket
import threading
import pickle
import datetime
 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

# 버튼 핀의 입력설정 , PULL DOWN 설정 
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

s_data = {'pass' : 0} #우회전 유무 패킷
right = 0

def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        r_time = datetime.datetime.now().strftime("%H:%M:%S")
        r_data = pickle.loads(data)
        
        if r_data[0] != "1":
            print(f">> HOST의 message : {r_data} ({r_time})")
            print(f">> 남은 시간 : {r_data[0]['remain']}")
        
            if r_data[0]['plus'] != 0:
                print(f">> 추가된 시간 : {r_data[0]['plus']}")
        
            if r_data[0]['remain'] == 1:
                print(">> Pass the Crosswalk !!")

def send_signal():
    while True:
        global right
        
        if GPIO.input(15) == GPIO.HIGH:
            if right == 0:
                print(">> 우회전 버튼 On\n")
            else:
                print(">> 우회전 버튼 Off\n")
                
            right = not right

        time.sleep(0.5)

#TCP 연결
def connect_TCP(HOST, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    recv_thread = threading.Thread(target=recv_data, args=(client_socket,))
    recv_thread.start()
    print('>> Connect Server\n')
    
    while True:
        global s_data, right
        
        time.sleep(1)    
        if right == True:
            s_data['pass'] = int(right)
        
            s_time = datetime.datetime.now().strftime("%H:%M:%S")
            data = pickle.dumps([s_data, s_time])
            client_socket.sendall(data)  
        else:
            continue

    client_socket.close()

#UDP로부터 ip주소 얻고
def recv_UDP_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 9999))
    data, addr = sock.recvfrom(1024)
    
    HOST = addr[0]  # broadcast로 HOST ip를 받아옴
    PORT = 8261
    
    connect_TCP(HOST, PORT)
