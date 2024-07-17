import paho.mqtt.client as mqtt
import signal
import sys
import time
import json

# 전역 변수 초기화
log1 = []
log2 = []
name1 = ""
name2 = ""
datedata = time.strftime('%y%m%d%H%M%S', time.localtime(time.time()))


# 메시지 수신 콜백 함수
def on_message(client, userdata, message):
    global name1, name2  # 전역 변수를 사용하도록 지정
    payload = json.loads(message.payload.decode("utf-8"))
    print("메시지 수신: ", message.payload.decode("utf-8"))
    print("메시지 주제: ", message.topic)

    device_name = payload["deviceName"]
    if device_name[-4:] == "C03A":
        name1 = device_name
        print(name1)
        if len(payload["object"]) > 2:
            log1.append(str(payload["object"]))
    else:
        name2 = device_name
        print(device_name)
        if len(payload["object"]) > 2:
            log2.append(str(payload["object"]))


# 연결 콜백 함수
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("연결 성공")
        client.subscribe("application/5/device/+/event/up")
        print("주제 구독: application/5/device/+/event/up")
    else:
        print("연결 실패, 코드: ", rc)


# 로그 콜백 함수
def on_log(client, userdata, level, buf):
    print("로그: ", buf)


# 종료 시 호출될 함수
def save_log_and_exit(signal, frame):
    global name1, name2  # 전역 변수를 사용하도록 지정
    print("프로그램 종료 중... 로그를 저장합니다.")

    # name1과 name2가 비어있는지 확인
    if name1:
        filename1 = f'{name1}_{datedata}.txt'
        with open(filename1, "w") as f:
            for entry in log1:
                f.write(entry + "\n")
        print(f"{filename1}에 로그가 저장되었습니다.")
    else:
        print("로그 저장을 실패 했습니다.")

    if name2:
        filename2 = f'{name2}_{datedata}.txt'
        with open(filename2, "w") as f:
            for entry in log2:
                f.write(entry + "\n")
        print(f"{filename2}에 로그가 저장되었습니다.")
    else:
        print("로그 저장을 실패 했습니다.")

    sys.exit(0)


# SIGINT(Ctrl+C) 신호를 처리할 핸들러 설정
signal.signal(signal.SIGINT, save_log_and_exit)

# 브로커 주소와 인증 정보
broker_address = ""
username = ""
password = ""

# 클라이언트 생성
client1 = mqtt.Client(client_id="", protocol=mqtt.MQTTv311)
client1.username_pw_set(username, password)
client1.on_connect = on_connect
client1.on_message = on_message
client1.on_log = on_log

# 연결 시도
print("연결 시도 중...")
client1.connect(broker_address)

# 메시지 루프 시작
client1.loop_forever()
