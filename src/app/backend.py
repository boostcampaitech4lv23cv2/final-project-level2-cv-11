from typing import List, Union, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File
from fastapi.param_functions import Depends
from pydantic import BaseModel, Field
from pipeline import typical_pipeline

app = FastAPI()

@app.get('/')
def hello_world():
    return {'hello: world'}

@app.post('/ocr', description='ocr모델을 돌립니다.')
async def make_order(files: List[UploadFile] =File(...)):
    for file in files:
        image_bytes = await file.read()
        print('image_bytes: ', image_bytes, '결과끝')
    Typical_pipeline = typical_pipeline.Typical_Pipeline()
    ocr_results = Typical_pipeline.clova_ocr(image_bytes)
    print(ocr_results)
    return ocr_results

