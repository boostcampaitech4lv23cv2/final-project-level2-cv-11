from typing import List, Union, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File
from fastapi.param_functions import Depends
from pydantic import BaseModel, Field
from pipeline import typical_pipeline

app = FastAPI()

Typical_pipeline = typical_pipeline.Typical_Pipeline()


@app.get('/')
def hello_world():
    return {'hello: world'}

@app.post('/ocr', description='ocr모델을 돌립니다.')
async def make_ocr(files: List[UploadFile] = File(...)):
    for file in files:
        image_bytes = await file.read()
    ocr_results = Typical_pipeline.clova_ocr(image_bytes)
    return ocr_results

class KoreanText(BaseModel):
    name: str
    text: str

@app.post('/mt/{text}', description='mt모델을 돌립니다.')
async def make_mt(text):
    mt_result = Typical_pipeline.papago(text)
    return mt_result

