import os
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, UploadFile, File
from backend.pipeline import typical_pipeline
from dotenv import load_dotenv
import pytesseract
import numpy as np
import cv2
from pathlib import Path


load_dotenv()
api_url = os.getenv("CLOVA_URL")
secret_key = os.getenv("CLOVA_KEY")

router = APIRouter(prefix="/test")


class Box(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    w: int
    h: int
    text: str


@router.get("/raise", description="Exception Handling 테스트")
async def raise_exception():
    y = 1 / 0
    return "success"


@router.post(
    "/clova_raw", description="clova ocr 테스트 (후처리 X)", response_model=List[Box]
)
async def clova(file: UploadFile = File(...)):
    tp = typical_pipeline.Typical_Pipeline()
    bytes = await file.read()
    result = tp.OCR.request(bytes)

    res = []
    for ocr in result[1].values():
        p1, p2, text, _ = ocr
        x1, y1 = p1
        x2, y2 = p2
        box = Box(x1=x1, y1=y1, x2=x2, y2=y2, w=x2 - x1, h=y2 - y1, text=text)
        res.append(box)

    return res


@router.post(
    "/clova_post", description="clova ocr 테스트 (후처리 O)", response_model=List[Box]
)
async def clova_post(file: UploadFile = File(...)):
    tp = typical_pipeline.Typical_Pipeline()
    bytes = await file.read()
    ocr_result = tp.clova_ocr(bytes)

    res = []
    for ocr in ocr_result:
        p1, p2, text, _ = ocr
        x1, y1 = p1
        x2, y2 = p2
        box = Box(x1=x1, y1=y1, x2=x2, y2=y2, w=x2 - x1, h=y2 - y1, text=text)
        res.append(box)
    return res


@router.post(
    "/clova_tess", description="tesseract ocr 테스트 (후처리 O)", response_model=List[Box]
)
async def clova_tess(file: UploadFile = File(...)):
    tp = typical_pipeline.Typical_Pipeline()
    bytes = await file.read()
    encoded_img = np.fromstring(bytes, dtype=np.uint8)
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    ocr_result = tp.clova_ocr(bytes)

    res = []
    for m in ocr_result:
        x1 = m[0][0]
        x2 = m[1][0]
        y1 = m[0][1]
        y2 = m[1][1]
        img_crop = img[y1 : y2 + 1, x1 : x2 + 1]
        boxes = pytesseract.image_to_boxes(img_crop, lang="kor")

        img_crop_letters = []
        for b in boxes.splitlines():
            b = b.split(" ")
            cx1, cy1, cx2, cy2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            h = y2 - y1
            cropped_image = img_crop[h - cy2 : h - cy1 + 1, cx1:cx2]
            i, j, k = cropped_image.shape
            if i and j and k:
                img_crop_letters.append(cropped_image)
                box = Box(
                    x1=x1 + cx1,
                    y1=y1 + cy1,
                    x2=x2 + cx2,
                    y2=y2 + cy2,
                    w=cx2 - cx1,
                    h=cy2 - cy1,
                    text=b[0],
                )
                res.append(box)

    return res
