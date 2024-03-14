from fastapi import FastAPI, Request, Response, File, UploadFile, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List
from model import get_stream_video
from plate import plate_eval_all, getOCR
import shutil
import os
import cv2
# import numpy as np
# import base64


app = FastAPI()


templates = Jinja2Templates(directory='../client/html')
app.mount("/js", StaticFiles(directory="../client/js"), name="js")
app.mount("/css", StaticFiles(directory='../client/css'), name='css')


origins = [
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000",
]

# 모든 출처 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)


# index 페이지 로드
@app.get("/", response_class=HTMLResponse)
def main_page(request: Request):
  return templates.TemplateResponse('index.html', context={'request':request})


folder_name = "videos"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

UPLOAD_DIRECTORY = "./videos"
@app.post("/upload_video")
async def upload_video(video: UploadFile = File(...)):
    # 업로드된 파일의 경로
    upload_path = os.path.join(UPLOAD_DIRECTORY, video.filename)
    # 업로드된 파일을 서버에 저장
    with open(upload_path, "wb") as f:
        content = await video.read()
        f.write(content)
    print('동영상이 업로드 되었습니다')
    # 저장된 파일의 경로 반환
    return {"filename": video.filename, "saved_path": upload_path}

   
# 파일 업로드 POST 반응
@app.get("/video/")
async def videoStream(request: Request, query: str = Query(...)):
    # print(query)
    return StreamingResponse(get_stream_video(query), media_type="multipart/x-mixed-replace; boundary=frame")

# 이미지 잡혔는지 계속 가져오기
@app.get("/images")
async def send_images(request: Request, q: int = Query(...)):
    overload_folders = os.listdir('overload')
    img_cnt = len(overload_folders)
    print(q)
    print('이미지 업로드')

    if q < img_cnt:
        img_dir = os.path.join('overload', overload_folders[q])
        imgs = os.listdir(img_dir)

        # 번호판 평가 및 저장
        plate_eval_all(img_dir, imgs)

        return FileResponse(os.path.join(img_dir, imgs[0]), media_type='image/jpg')
    
# 세부사항 가져오기
@app.get("/info")
async def getInfo(request:Request, q: int = Query(...)):
    overload_folders = os.listdir('overload')
    target_folder = overload_folders[q]
    # overload/03-06_15-58-28
    target_folder_dir = os.path.join('overload', overload_folders[q])
    # 날짜 저장
    date = target_folder_dir.split("\\")[-1]
    imgs = os.listdir(target_folder_dir)
    # "perspective"로 시작하는 파일들만 가져오기
    perspective_files = [file for file in imgs if file.startswith("perspective")]
    if perspective_files:
        ocr_score = []
        best_ocr = None
        max_length_index = 0
        # 스코어 확인
        for pers_img in perspective_files:
            img = cv2.imread(os.path.join(target_folder_dir, pers_img))
            result = getOCR(img)
            if result:
                ocr_score.append(result)
        if ocr_score:
            # 최대 길이를 가지는 문자열의 인덱스 찾기
            max_length_index = max(range(len(ocr_score)), key=lambda i: len(ocr_score[i]))
            best_ocr = ocr_score[max_length_index]

        # overload/03-06_15-58-28/perspective1.jpg
        perspective_img_dir = os.path.join(target_folder_dir, perspective_files[max_length_index])
        

        data = {"perspective_path": perspective_img_dir, "OCR":best_ocr, "date":date}
        print(data)
    else:
        data = {"perspective_path": None, "OCR":None, "date":date}
        print(data)

    # JSONResponse를 사용하여 이미지 파일의 경로와 함께 JSON 데이터 반환
    return JSONResponse(content=data, media_type="application/json")

# perspective 이미지 가져오기
@app.get("/perspective")
async def getImg(request:Request, q: str = Query(...)):
    if not q:
        return {"message": 'sorry'}
    return FileResponse(q, media_type='image/jpg')