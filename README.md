# 과적차량 자동 감지 시스템

## 📌 시스템 개요
* 도로의 CCTV로 과적차량을 탐지하고 해당 차량 사진 저장 및 번호판을 인식하는 시스템
* Ultralytics의 YOLOv5s모델을 사용하여 과적차량의 탐지 및 분석에 도움을 주는 서비스
* 기존 과속 단속 기능에 추가로 과적차량까지 탐지하여 도로 안전 개선을 위해 기획

## 💡 프로젝트 개발 과정
* 데이터 수집(AIHub) 및 정제
* 프로젝트에 사용할 사전학습 모델을 선정하기 위해 YOLOv5, YOLOv5s, YOLOv5s6, YOLOv5l6등 많은 모델을 테스트
  * YOLOv5s를 사용
* 결과 후처리
* 서버 및 UI 제작

## 📚 사용한 데이터
* [AIHUB 과적차량 도로 위험 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=data&dataSetSn=530)
* [AIHUB 자동차 차종/연식/번호판 인식용 영상 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=172)
* 데이터 라벨링 변환 : Google Colab을 이용하여 필요한 라벨링만 추출 후 정제


# 설치 및 사용방법

1. 자신의 다운로드 OR git clone을 이용하여 VScode에 받습니다.
2. 터미널에서 cd server
3. uvicorn main:app --reload 를 입력하여 서버를 기동합니다.
4. 터미널에서 http://127.0.0.1:8000를 ctrl + 마우스 왼쪽 클릭으로 실행합니다. 혹은 VScode에서 live server가 실행되어 있으면
윈도우 : client/html/index.html을 클릭 후 ALT + L + O
맥북 : client/html/index.html을 클릭 후 command + L + O

## 필요한 모듈 설치
1. pip install fastapi
2. pip install paddlepaddle, paddleocr
3. pip install opencv-python
4. pip install torch
5. pip install uvicorn
6. pip install utils
7. pip install jinja2

* 만약 맥북에서 paddlepaddle, paddleocr 설치 중 오류가 발생시 아래와 같이 진행하면 됩니다.
  1. brew update
  2. brew install mupdf swig
  3. pip install https://github.com/pymupdf/PyMuPDF/archive/master.tar.gz
  4. 다시 처음부터 paddlepaddle, paddleocr을 설치하면 됩니다.


# ☑ Skills
### Language
<div align="center">
    <img src="https://img.shields.io/badge/python-3776AB?style=flat&logo=python&logoColor=white" />
</div>

### AI
<div align="center">
    <img src="https://img.shields.io/badge/Opencv-5C3EE8?style=flat&logo=opencv&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/pytorch-EE4C2C?style=flat&logo=pytorch&logoColor=white" />
</div>

### Front-End
<div align="center">
    <img src="https://img.shields.io/badge/html5-E34F26?style=flat&logo=html&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/javascript-F7DF1E?style=flat&logo=javascript&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/css3-1572B6?style=flat&logo=css&logoColor=white" />
</div>

### Back-End
<div align="center">
    <img src="https://img.shields.io/badge/fastapi-009688?style=flat&logo=fastapi&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/jinja-B41717?style=flat&logo=jinja2&logoColor=white" />
</div>

### Tools
<div align="center">
    <img src="https://img.shields.io/badge/git-F05032?style=flat&logo=git&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/github-181717?style=flat&logo=github&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/slack-4A154B?style=flat&logo=slack&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/discord-5865F2?style=flat&logo=discord&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/pycharm-000000?style=flat&logo=pycharm&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/jupyter-F37626?style=flat&logo=jupyter&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/googlecolab-F9AB00?style=flat&logo=googlecolab&logoColor=white" /> &nbsp&nbsp
    <img src="https://img.shields.io/badge/visualstudiocode-007ACC?style=flat&logo=visualstudiocode&logoColor=white" />
</div>
