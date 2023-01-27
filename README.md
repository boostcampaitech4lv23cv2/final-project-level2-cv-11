cv-11 구미호 최종 프로젝트

실행 방법

```bash
conda create -n {가상환경명} python=3.8.5
pip install --user poetry
# (sudo) vi ~/.bashrc 입력 후, 맨 아래에 PATH="$HOME/.local/bin:$PATH" 추가 (한 번만 하면 됨)
poetry install
# poetry install 후 터미널 재실행

# Tesseract 4 설치 & 가중치 다운로드
apt install -y tesseract-ocr
wget -P /usr/share/tesseract-ocr/4.00/tessdata https://github.com/tesseract-ocr/tessdata/raw/main/kor.traineddata

# Font Classifier 가중치 다운로드후
# https://boostcampaitech.slack.com/files/U041L8WPYKW/F04K17EEXS7/weight.pth
# src/model/font_classifier/weights/typical_font/weight.pth 로 옮겨야 함

# .env 파일 설정

# Backend (FastAPI) 실행 1019648 1096536
cd src/
python -m backend

# Frontend (Streamlit) 실행
cd /src/frontend
streamlit run frontend.py --server.port 30001
# --server.fileWatcherType none
```