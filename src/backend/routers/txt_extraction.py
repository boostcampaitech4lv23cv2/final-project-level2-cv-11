from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, UploadFile, File
from backend.pipeline import typical_pipeline
import copy


router = APIRouter(prefix="/txt_extraction")


class Results(BaseModel):
    ocr_result: List
    font_result: List


@router.post("/", description="ocr모델을 돌립니다.", response_model=Results)
async def make_ocr_font(file: UploadFile = File(...)):
    Typical_pipeline = typical_pipeline.Typical_Pipeline()

    # OCR
    image_bytes = await file.read()
    ocr_result = Typical_pipeline.clova_ocr(image_bytes)

    # Font Classification
    font_cls_result = Typical_pipeline.typical_font_classification(
        copy.deepcopy(ocr_result)
    )

    res = Results(ocr_result=ocr_result, font_result=font_cls_result)
    return res


class RecFont(BaseModel):
    name: str
    prob: float


class Box(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    w: int
    h: int
    text: str
    fonts: List[RecFont]
    color: str


cache = {}

from hashlib import sha256


@router.post("/v2", description="OCR + 폰트 분류", response_model=List[Box])
async def v2(file: UploadFile = File(...)):
    image_bytes = await file.read()

    m = sha256()
    m.update(image_bytes)
    h = m.digest()
    if h in cache:
        return cache[h]

    Typical_pipeline = typical_pipeline.Typical_Pipeline()

    # OCR
    ocr_result = Typical_pipeline.clova_ocr(image_bytes)

    # Font Classification
    font_cls_result = Typical_pipeline.typical_font_classification(
        copy.deepcopy(ocr_result)
    )
    recs, colors = font_cls_result

    res = []
    for ocr, fonts, color in zip(ocr_result, recs, colors):
        p1, p2, text, _ = ocr
        x1, y1 = p1
        x2, y2 = p2
        recfonts = [
            RecFont(name=name.rstrip(".ttf"), prob=prob) for name, prob in fonts
        ]
        res.append(
            Box(
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                w=x2 - x1,
                h=y2 - y1,
                text=text,
                fonts=recfonts,
                color=color,
            )
        )

    cache[h] = res

    return res
