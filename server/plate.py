import cv2
import numpy as np
import os
import torch
import pathlib
from paddleocr import PaddleOCR

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# custom/local model
plate_model = torch.hub.load('ultralytics/yolov5', 'custom', 'plate_best.pt')

# 번호판 인식하면 perspective하는 함수
def plate_eval_all(img_dir, imgs):
    for img in imgs:
        test_img_dir = os.path.join(img_dir, img)
        test_img = cv2.imread(test_img_dir)

        # 모델 돌리기
        with torch.no_grad():
            prediction = plate_model(test_img)

        # plate 좌표값으로 perspective 이미지 만드는 함수
        getPerspective(test_img, prediction, img_dir)
    return 'ok'

def getPerspective(image, prediction, img_dir):
    cord = prediction.xyxy[0]
    name = prediction.names
    size = len(cord)

    for i in range(size - 1):
        XMin, YMin, XMax, YMax, conf, cls = cord[i, :6]
        print(f"{name[int(cls)]} cord:", cord[i, :5])
        if int(cls) == 1:
            coord = [[XMin, YMin], [XMax, YMin], [XMax, YMax], [XMin, YMax]]
            # perspective 해주는 함수
            dst = perspective(image, coord)

            # 이미지 저장
            print('다운로드')
            cv2.imwrite(os.path.join(img_dir, f'perspective{i}.jpg'), dst)
    return 'ok'


def perspective(img, coord):
    w, h = 400, 100
    srcQuad = np.array(coord, np.float32)
    dstQuad = np.array([[0, 0], [w, 0],[w, h],[0, h]], np.float32)

    pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
    dst = cv2.warpPerspective(img, pers, (w, h))

    return dst


# OCR ----------------------------------------------------------------------


# perspective 이미지로 paddle ocr
# ocr돌리고 ocr_score append하는 함수
def getOCR(dst):
    ocr_score = []
    # dst 파일을 OCR로 읽어오기
    por = PaddleOCR()
    result = por.ocr(dst, cls=False)
    text = ''
    # OCR 결과가 None인 경우 처리
    if result == [None]:
        return None
    else:
        for line in result[0]:
            extracted_text = line[1][0]

            # 추출된 텍스트를 기존에 추출된 텍스트에 추가
            text += extracted_text + " "

        return text



# # 결과값을 텍스트파일 생성,저장
# def save_text(text, file_path):

#     os.makedirs(os.path.dirname(file_path), exist_ok=True)
#     with open(file_path, "w") as f:
#         f.write(text)

