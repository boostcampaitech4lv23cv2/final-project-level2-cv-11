cv-11 구미호 최종 프로젝트

실행 방법

```bash
conda create -n {가상환경명} python=3.8
pip install --user poetry
# (sudo) vi ~/.bashrc 입력 후, 맨 아래에 PATH="$HOME/.local/bin:$PATH" 추가 (한 번만 하면 됨)
poetry install
# poetry install 후 터미널 재실행

# 서버생성
python -m app

# frontend 연결
python -m streamlit run frontend.py --server.port 30001
#streamlit run frontend.py --server.port 30001 --server.fileWatcherType none
```