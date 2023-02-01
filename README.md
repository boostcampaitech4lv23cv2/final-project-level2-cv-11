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

# Font Classifier 가중치 다운로드
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1a28eDYyOUrJEhvLHsfI1iFBHhA7LlWl7' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1a28eDYyOUrJEhvLHsfI1iFBHhA7LlWl7" -O /opt/ml/final-project-level2-cv-11/src/model/font_classifier/weights/typical/weight.pth && rm -rf ~/cookies.txt

# .env 파일 설정

# Backend (FastAPI) 실행 1019648 1096536
cd src/
python -m backend

# Frontend (Streamlit) 실행
cd /src/frontend
streamlit run frontend.py --server.port 30001
# --server.fileWatcherType none
```