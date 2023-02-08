# [CV-11] Toonslator | 생동감있는 웹툰 자동 번역 서비스

# **💁** 팀 소개
## CV 11조 🦊구미호🦊
| [류건](https://github.com/jerry-ryu) | [심건희](https://github.com/jane79) | [윤태준](https://github.com/ta1231) | [이강희](https://github.com/ganghe74) | [이예라](https://github.com/Yera10) |
| :-: | :-: | :-: | :-: | :-: | 
| <img src="https://avatars.githubusercontent.com/u/62556539?v=4" width="200"> | <img src="https://avatars.githubusercontent.com/u/48004826?v=4" width="200"> | <img src="https://avatars.githubusercontent.com/u/54363784?v=4"  width="200"> | <img src="https://avatars.githubusercontent.com/u/30896956?v=4" width="200"> | <img src="https://avatars.githubusercontent.com/u/57178359?v=4" width="200"> |  
|[Blog](https://kkwong-guin.tistory.com/)  |[Blog](https://velog.io/@goodheart50)|[Blog](https://velog.io/@ta1231)| [Blog](https://dddd.ac/blog) | [Blog](https://yedoong.tistory.com/) |
| <code>모델링</code><br><code>파이프라인</code><br><code>데이터 수집</code> | <code>모델링</code><br><code>연구</code><br><code>데이터 수집</code>  |  <code>백엔드</code><br><code>발표자료</code><br><code>협업 관리</code>  | <code>프론트엔드</code><br><code>서비스 배포</code><br><code>파이프라인</code> | <code>백엔드</code><br><code>서비스 배포</code><br><code>파이프라인</code> |

<div align="center">

![python](http://img.shields.io/badge/Python-000000?style=flat-square&logo=Python)
![pytorch](http://img.shields.io/badge/PyTorch-000000?style=flat-square&logo=PyTorch)
![ubuntu](http://img.shields.io/badge/Ubuntu-000000?style=flat-square&logo=Ubuntu)
![git](http://img.shields.io/badge/Git-000000?style=flat-square&logo=Git)
![github](http://img.shields.io/badge/Github-000000?style=flat-square&logo=Github)

</div align="center">

## 목차

- [프로젝트 소개](#프로젝트-소개)
  * [Toonslator](#toonslator)
  * [Environments](#environments)
  * [프로젝트 배경](#프로젝트-배경)
  * [문제정의 및 프로젝트 목표](#문제정의-및-프로젝트-목표)
  * [서비스 아키텍처](#서비스-아키텍처)
  * [서비스 파이프라인](#서비스-파이프라인)
  
- [Demo](#demo)
- [실행방법](#실행방법)
  * [Frontend](#frontend)
  * [Backend](#backend)
  * [Training](#training)
- [Reference](#reference)


# **📃** 프로젝트 소개

## 🧑‍🎨Toonslator🎨

저희의 서비스는 작품을 해외로 진출하고 싶은 웹툰 작가나 번역 및 편집에 어려움을 겪는 번역-편집자를 위한 서비스를 제공합니다.

(Web**toon**)+(Translation)을 합쳐 Toonslator라는 서비스를 만들었습니다.

## Environments
> - Ubuntu 18.04.5 LTS
> - Intel(R) Xeon(R) Gold 5120 CPU @ 2.20GHz
> - NVIDIA Tesla V100-PCIE-32GB
> - React
> - pytorch
> - FastAPI
> - Nginx
> - OpenCV

## **프로젝트 배경**

디지털 만화시장의 점유율이 점차 높아져 결국 2019년에는 인쇄 만화 시장을 뛰어 넘었습니다.

소비자들의 성공적 반응으로 세계적으로 수출 시장이 커지는 중입니다.

**하지만  번역 및 현지화 과정은 웹툰 수출 과정에서 걸림돌입니다.**

![image](https://user-images.githubusercontent.com/54363784/217152294-bb9cd0b3-d447-4fda-824e-2a32f5f75151.png)

## **문제정의 및 프로젝트 목표**

- 문제정의
    - 적절한 편집 도구 없이 번역을 할 경우 비용이 증가
    - 현지화가 잘 되지 않는 경우 수요 감소로 인한 수익 하락
- 프로젝트 목표
    - **편집 자동화**를 통해 번역과정의 **비용을 최소화**하고 소비자 증가를 통한 **수익 극대화**를 목표로 합니다.

![image](https://user-images.githubusercontent.com/54363784/217152371-42b6de05-53ce-4667-8258-3138f4f53860.png)

## 서비스 아키텍처

- **Frontend**
    - HTML
    - CSS
    - React
- **Backend**
    - FastAPI
- **API**
    - Clova OCR
    - Papago 기계번역

![image](https://user-images.githubusercontent.com/54363784/217152401-3e46c546-d8cd-4f8b-8cde-781f0e58daca.png)

## 서비스 파이프라인

1. 사용자로부터 배경, 대사 효과음 이미지를 받습니다.
2. 대사 이미지는 대사 파이프라인을 통해 대사의 위치를 찾고, 번역 및 폰트를 분류과정을 거칩니다.
3. 효과음 파이프라인은 대사 파이프라인을 통한 output을 사용하여 폰트 생성하는 과정을 거칩니다.
4. 번역된 결과물을 이용하여 폰트를 수정, 위치 변경, 색 변경 등의 편집을 할 수 있습니다.
5. 편집이 완료되면 최종 결과물을 얻을 수 있습니다.

![image](https://user-images.githubusercontent.com/54363784/217152527-0a5e631a-94c9-43de-9234-8cbacd1bbe66.png)

## 결과물
![image](https://user-images.githubusercontent.com/54363784/217299454-60cd10a4-f10f-4f5f-84b9-c408695230d4.png)

# 📹Demo



# 🚀실행방법


## Frontend

1. 경로 이동

```bash
cd src
cd frontend-react
```

2. Nodejs 설치 (우분투)

```bash
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - &&\
sudo apt-get install -y nodejs
```

3. 패키지 설치

```bash
npm install
```

4. 서버 시작

```bash
npm start
```

## Backend

1. 패키지 환경 설정

```bash
pip install --user poetry
# (sudo) vi ~/.bashrc 입력 후, 맨 아래에 PATH="$HOME/.local/bin:$PATH" 추가 (한 번만 하면 됨)
# 프로젝트 폴더 내에 가상환경을 저장
poetry config virtualenvs.in-project true
# poetry 가상환경 내에서 실행
poetry shell
```

2. 가중치, font 다운로드 및 환경변수 설정
- Font Classifier 가중치

```bash
# 링크1 : https://drive.google.com/file/d/1a28eDYyOUrJEhvLHsfI1iFBHhA7LlWl7/view?usp=sharing
# -O 옵션에 다운받을 경로 지정
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1a28eDYyOUrJEhvLHsfI1iFBHhA7LlWl7' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1a28eDYyOUrJEhvLHsfI1iFBHhA7LlWl7" -O /opt/ml/final-project-level2-cv-11/src/model/font_classifier/weights/typical/weight.pth && rm -rf ~/cookies.txt
```
```bash
# 링크2 : https://drive.google.com/file/d/107iA6ir5Fbii-5JimkGaL-HBomTDeKR1/view?usp=sharing
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=107iA6ir5Fbii-5JimkGaL-HBomTDeKR1' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=107iA6ir5Fbii-5JimkGaL-HBomTDeKR1" -O /opt/ml/final-project-level2-cv-11/src/model/font_classifier/weights/untypical/weight.pth && rm -rf ~/cookies.txt
```

- Font Generator 가중치

```bash
# mxfont링크: https://drive.google.com/file/d/1URxBMtHx1SXAAJ4b4A2jbmD44S1Ns1Jp/view?usp=sharing
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1URxBMtHx1SXAAJ4b4A2jbmD44S1Ns1Jp' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1URxBMtHx1SXAAJ4b4A2jbmD44S1Ns1Jp" -O /opt/ml/final-project-level2-cv-11/src/model/font_generator/mxfont/mxfont_weight.pth && rm -rf ~/cookies.txt
```
```bash
# gasnext링크: https://drive.google.com/file/d/173SEHgYuSoJ6eze-BaofzJutjd6bAIGo/view?usp=sharing
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=173SEHgYuSoJ6eze-BaofzJutjd6bAIGo' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=173SEHgYuSoJ6eze-BaofzJutjd6bAIGo" -O /opt/ml/final-project-level2-cv-11/src/model/font_generator/gasnext/checkpoints/gasnext_weight.pth && rm -rf ~/cookies.txt
```

- Script Font 다운로드

```bash
# 링크 : https://drive.google.com/file/d/1p7Rwc08Xbk9bHGIE_7UoWl5OQksfVHrm/view?usp=sharing
mkdir -p data/font/typical
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1p7Rwc08Xbk9bHGIE_7UoWl5OQksfVHrm' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1p7Rwc08Xbk9bHGIE_7UoWl5OQksfVHrm" -O /opt/ml/final-project-level2-cv-11/data/font/typical.zip && rm -rf ~/cookies.txt
unzip data/font/typical.zip -d data/font
```

- Effect Font 다운로드

```bash
# 링크 : https://drive.google.com/file/d/14rTAp7WJpr4Cl4qLrh5H7qgeiy4SfHw9/view?usp=sharing
mkdir -p data/font/untypical
wget --load-cookies ~/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=14rTAp7WJpr4Cl4qLrh5H7qgeiy4SfHw9' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=14rTAp7WJpr4Cl4qLrh5H7qgeiy4SfHw9" -O /opt/ml/final-project-level2-cv-11/data/font/untypical.zip && rm -rf ~/cookies.txt
unzip data/font/untypical.zip -d data/font
```

- .env 파일 설정

```bash
# .env파일 만들고 아래 입력
# 사용을 위해서 두 사이트에서 key를 발급받아야 합니다.
# 파파고:https://developers.naver.com/docs/papago/papago-nmt-example-code.md
# Clova OCR: https://guide-fin.ncloud-docs.com/docs/ocr-ocr-1-4

PAPAGO_ID="인증 ID를 입력해주세요"
PAPAGO_SECRET="인증 key를 입력해주세요"
CLOVA_URL="인증 URL을 입력해주세요"
CLOVA_KEY="인증 key를 입력해주세요"
```

- 실행

```bash
# Backend (FastAPI) 실행
cd src/
python -m backend
```

## Training

# 🗞️Reference

- Font Generation
    - mxfont
        - paper: [https://arxiv.org/abs/2104.00887](https://arxiv.org/abs/2104.00887)
        - repo: [https://github.com/clovaai/mxfont](https://github.com/clovaai/mxfont)
    - gasnext:
        - paper: [https://arxiv.org/abs/2212.02886](https://arxiv.org/abs/2212.02886)
        - repo: [https://github.com/cmu-11785-F22-55/GAS-NeXt](https://github.com/cmu-11785-F22-55/GAS-NeXt)
- Dataset
    - typical:
    - untypical:
- Open source
    - svg2ttf: [https://github.com/fontello/svg2ttf](https://github.com/fontello/svg2ttf)
    - pytesseract: [https://github.com/tesseract-ocr/tesstrain](https://github.com/tesseract-ocr/tesstrain)
    - tesseract: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
    - 
