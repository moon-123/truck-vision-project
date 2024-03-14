import cv2
import torch
import os
import time
import pathlib

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# custom/local model
model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')

overload_folder = "overload"

if not os.path.exists(overload_folder):
    os.makedirs(overload_folder)

def get_stream_video(query):
    # camera 정의
    video = cv2.VideoCapture(f'./videos/{query}')

    while (video.isOpened()):
        ret, frame = video.read()
        if ret:
            # 모델 돌리기
            with torch.no_grad():
                prediction = model(frame)

            annotated_image = visualize_prediction(frame, prediction)

            success, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(frame) + b'\r\n')
            
download = False
cnt = 0
current_time = 0
current_folder = None

def visualize_prediction(image, prediction):
    global download, cnt, current_folder, current_time

    cord = prediction.xyxy[0]
    name = prediction.names
    size = len(cord)
    
    for i in range(size - 1):
        XMin, YMin, XMax, YMax, conf, cls = cord[i, :6]
        # print(XMin, YMin, XMax, YMax)
        # print(f"{name[int(cls)]} cord:", cord[i, :5])
        if int(cls) == 0:
            if conf > 0.85:  # 신뢰도가 일정 수준 이상인 객체만 표시
                cv2.rectangle(image, (int(XMin), int(YMin)), (int(XMax), int(YMax)), (0, 0, 255), 2)
                cv2.putText(image, f'Overload:{conf:.2f}', (int(XMin), int(YMin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
                print(f"{name[int(cls)]} cord:", cord[i, :5])
                if not download:
                    if YMax > 710 and YMax < 730:
                        download = True
                        # 한 객체 폴더 생성
                        current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())[5:]
                        current_folder = os.path.join(overload_folder, current_time)
                        if not os.path.exists(current_folder):
                            os.makedirs(current_folder)
                        # 이미지 저장
                        print('다운로드 시작')
                        cv2.imwrite(os.path.join(current_folder, f"{current_time}_{cnt}.jpg"), image)
                        cnt += 1
    # 이미지 저장
    if download:
        cv2.imwrite(os.path.join(current_folder, f"{current_time}_{cnt}.jpg"), image)
        cnt += 1
        print('다운로드')
    # 5장 저장하면 stop
    if cnt == 3:
        download = False
        cnt = 0
        print('다운로드 끝')

                
    return image