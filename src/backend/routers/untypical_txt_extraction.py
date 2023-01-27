from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, UploadFile, File
from backend.pipeline import untypical_pipeline
import copy


router = APIRouter(prefix="/untypical/txt_extraction")


class Results(BaseModel):
    ocr_result: list
    font_result: List[str]


@router.post("/", description="ocr모델을 돌립니다.", response_model=Results)
async def make_ocr_font(file: UploadFile = File(...)):
    Untypical_pipeline = untypical_pipeline.Untypical_Pipeline("/opt/ml/final-project-level2-cv-11/")

    # OCR
    image_bytes = await file.read()
    ocr_result = Untypical_pipeline.clova_ocr(image_bytes)

    # Font Classification
    font_cls_result = Untypical_pipeline.untypical_font_classification(
        copy.deepcopy(ocr_result)
    )

    res = Results(ocr_result=ocr_result, font_result=font_cls_result)
    return res



