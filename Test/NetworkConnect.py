import subprocess

def connect_to_wifi(ssid, password):
    # nmcli 명령을 사용하여 Wi-Fi에 연결
    command = f"nmcli device wifi connect '{ssid}' password '{password}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # 명령 실행 결과 확인
    if result.returncode == 0:
        print(f"Wi-Fi에 {ssid}에 성공적으로 연결되었습니다!")
        return True
    else:
        print(f"{ssid}에 연결하는 데 실패했습니다.")
        print("오류:", result.stderr)
        return False

# 네트워크 ㅑ
ssid = 'JDG'
password = 'jdg1072404'

# Wi-Fi에 연결
connect_to_wifi(ssid, password)

