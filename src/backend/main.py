from typing import List, Union, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File
from fastapi.param_functions import Depends
from pydantic import BaseModel, Field
from backend.pipeline import typical_pipeline

app = FastAPI()

Typical_pipeline = typical_pipeline.Typical_Pipeline()


@app.get("/")
def hello_world():
    return {"hello: world"}


@app.post("/ocr", description="ocr모델을 돌립니다.")
async def make_ocr(file: UploadFile = File(...)):
    image_bytes = await file.read()
    ocr_result = Typical_pipeline.clova_ocr(image_bytes)
    return ocr_result


class KoreanText(BaseModel):
    name: str
    text: str


@app.post("/mt", description="mt모델을 돌립니다.")
async def make_mt(text):
    mt_result = Typical_pipeline.papago(text)
    return mt_result


@app.post("/classification", description="classification모델을 돌립니다.")
async def make_classification(ocr_results: List):
    classification_result = Typical_pipeline.typical_font_classification(ocr_results)
    return classification_result
