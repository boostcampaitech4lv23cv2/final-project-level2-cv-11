cv-11 구미호 최종 프로젝트

## 실행 방법

패키지 환경 설정
```bash
pip install --user poetry
# (sudo) vi ~/.bashrc 입력 후, 맨 아래에 PATH="$HOME/.local/bin:$PATH" 추가 (한 번만 하면 됨)
# 프로젝트 폴더 내에 가상환경을 저장
poetry config virtualenvs.in-project true
# poetry 가상환경 내에서 실행
poetry shell
```

가중치, font 다운로드 및 환경변수 설정
```bash
# Tesseract 4 설치 & 가중치
apt install -y tesseract-ocr
wget -P /usr/share/tesseract-ocr/4.00/tessdata https://github.com/tesseract-ocr/tessdata/raw/main/kor.traineddata

# Font Classifier 가중치
# 링크1 : https://drive.google.com/file/d/1a28eDYyOUrJEhvLHsfI1iFBHhA7LlWl7/view?usp=sharing
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1a28eDYyOUrJEhvLHsfI1iFBHhA7LlWl7' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1a28eDYyOUrJEhvLHsfI1iFBHhA7LlWl7" -O /opt/ml/final-project-level2-cv-11/src/model/font_classifier/weights/typical/weight.pth && rm -rf ~/cookies.txt
# 링크2 : https://drive.google.com/file/d/107iA6ir5Fbii-5JimkGaL-HBomTDeKR1/view?usp=sharing
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=107iA6ir5Fbii-5JimkGaL-HBomTDeKR1' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=107iA6ir5Fbii-5JimkGaL-HBomTDeKR1" -O /opt/ml/final-project-level2-cv-11/src/model/font_classifier/weights/untypical/weight.pth && rm -rf ~/cookies.txt

# Script Font 다운로드
# 링크 : https://drive.google.com/file/d/1p7Rwc08Xbk9bHGIE_7UoWl5OQksfVHrm/view?usp=sharing
mkdir -p data/font/typical
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1p7Rwc08Xbk9bHGIE_7UoWl5OQksfVHrm' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1p7Rwc08Xbk9bHGIE_7UoWl5OQksfVHrm" -O /opt/ml/final-project-level2-cv-11/data/font/typical.zip && rm -rf ~/cookies.txt
unzip data/font/typical.zip -d data/font

# Effect Font 다운로드
# 링크 : https://drive.google.com/file/d/14rTAp7WJpr4Cl4qLrh5H7qgeiy4SfHw9/view?usp=sharing
mkdir -p data/font/untypical
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=14rTAp7WJpr4Cl4qLrh5H7qgeiy4SfHw9' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=14rTAp7WJpr4Cl4qLrh5H7qgeiy4SfHw9" -O /opt/ml/final-project-level2-cv-11/data/font/untypical.zip && rm -rf ~/cookies.txt
unzip data/font/untypical.zip -d data/font

# .env 파일 설정
```

Backend & Frontend 실행
```bash
# Backend (FastAPI) 실행
cd src/
python -m backend

# Frontend (Streamlit) 실행
cd /src/frontend
streamlit run frontend.py --server.port 30001
# --server.fileWatcherType none
```