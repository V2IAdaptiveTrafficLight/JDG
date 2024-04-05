from bluepy.btle import Scanner, DefaultDelegate
import base64

class BeaconDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.found_beacon = False

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if not self.found_beacon:
            for (adtype, desc, value) in dev.getScanData():
                if value.startswith("aafe"):
                    # 'aafe'로 시작하는 경우, 맨 앞에서부터 8글자를 삭제하고 출력 - URL 문자열 부분
                    hex_value = value[8:]
                
                    # 2f(/)를 기준으로 SSID와 패스워드 분리
                    ssid_hex, password_hex = hex_value.split("2f")
                    
                    # 16진수를 ASCII문자열로 변환하여 SSID와 패스워드 출력
                    ssid = ''.join([chr(int(ssid_hex[i:i+2], 16)) for i in range(0, len(ssid_hex), 2)])
                    password = ''.join([chr(int(password_hex[i:i+2], 16)) for i in range(0, len(password_hex), 2)])
                    
                    # 문자열 띄어쓰기 제거
                    ssid = ssid.replace(" ", "")
                    password = password.replace(" ", "")
                    
                    return [ssid, password]

if __name__ == "__main__":
    scanner = Scanner().withDelegate(BeaconDelegate())
    scanner.start()
    scanner.process(timeout=3)  # 10초 동안 스캔
    scanner.stop()
