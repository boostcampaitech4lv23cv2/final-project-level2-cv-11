from fastapi import APIRouter, Query
from backend.pipeline import typical_pipeline


router = APIRouter(prefix="/mt")

Typical_pipeline = typical_pipeline.Typical_Pipeline()


@router.post("/", description="mt모델을 돌립니다.")
async def make_mt(text: str = Query(...)):
    text = text.strip()
    # TODO: 한글임을 판단하는 로직 추가
    if text == "":
        return text
    mt_result = Typical_pipeline.papago(text)
    return mt_result
