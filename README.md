cv-11 구미호 최종 프로젝트

실행 방법

```bash
conda create -n {가상환경명} python=3.8
pip install --user poetry
poetry install
# poetry install 오류시 export PATH="$HOME/.local/bin:$PATH” 후 다시 poetry install

# 서버생성
python -m app

# frontend 연결
python -m streamlit run frontend.py --server.port 30001
#streamlit run frontend.py --server.port 30001 --server.fileWatcherType none
```