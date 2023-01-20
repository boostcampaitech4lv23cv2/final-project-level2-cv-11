from fastapi import APIRouter
from backend.pipeline import typical_pipeline


router = APIRouter(prefix="/mt")

Typical_pipeline = typical_pipeline.Typical_Pipeline()


@router.post("/", description="mt모델을 돌립니다.")
async def make_mt(text):
    mt_result = Typical_pipeline.papago(text)
    return mt_result
