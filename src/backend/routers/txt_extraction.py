from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, UploadFile, File
from backend.pipeline import typical_pipeline
import copy


router = APIRouter(prefix="/txt_extraction")


class Results(BaseModel):
    ocr_result: list
    font_result: List[str]


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


class Box(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    text: str
    font: str


@router.post("/v2", description="OCR + 폰트 분류", response_model=List[Box])
async def v2(file: UploadFile = File(...)):
    Typical_pipeline = typical_pipeline.Typical_Pipeline()

    # OCR
    image_bytes = await file.read()
    ocr_result = Typical_pipeline.clova_ocr(image_bytes)

    # Font Classification
    font_cls_result = Typical_pipeline.typical_font_classification(
        copy.deepcopy(ocr_result)
    )

    res = []
    for ocr, font in zip(ocr_result, font_cls_result):
        p1, p2, text = ocr
        x1, y1 = p1
        x2, y2 = p2
        res.append(Box(x1=x1, y1=y1, x2=x2, y2=y2, text=text, font=font))

    return res
