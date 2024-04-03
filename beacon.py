import subprocess
import time

def execute_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Command executed successfully: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command {command}: {e}")

def main():
    # 블루투스 어댑터 활성화
    execute_command("sudo hciconfig hci0 up")
    time.sleep(1)  # 1초 대기

    # iBeacon 활성화
    execute_command("sudo hciconfig hci0 leadv 3")
    time.sleep(1)  # 1초 대기

    # iBeacon 데이터 전송
    execute_command("sudo hcitool -i hci0 cmd 0x08 0x0008 1b 02 01 06 03 03 aa fe 13 16 aa fe 10 00 4a 44 47 2f 6a 64 67 31 30 37 32 34 30 34 00 00 00 00")

if __name__ == "__main__":
    main()
