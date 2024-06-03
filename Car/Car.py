from TCP_client import recv_data, recv_UDP_data, connect_TCP, send_signal #UDP, TCP연결 관련
from Beacon_Network_Connect import BeaconDelegate, connect_to_wifi, scan_beacon #Network 연결 관련
from moter import forward, backward, left, right, stop, move

import socket
import threading
import pickle
from bluepy.btle import Scanner, DefaultDelegate, BTLEDisconnectError
import subprocess
import time

# UDP 데이터 받기
threading.Thread(target=recv_UDP_data).start()

# Signal
threading.Thread(target=send_signal).start()

# Beacon 스캔 계속
threading.Thread(target=scan_beacon).start()

# Move
threading.Thread(target=move).start()
