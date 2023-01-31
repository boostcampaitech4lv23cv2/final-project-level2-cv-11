from fastapi import APIRouter, Query
from backend.pipeline import untypical_pipeline


router = APIRouter(prefix="/untypical/mt")


@router.post("/", description="mt모델을 돌립니다.")
async def make_mt(text: str = Query(...)):
    Untypical_pipeline = untypical_pipeline.Untypical_Pipeline("/opt/ml/final-project-level2-cv-11/")
    
    text = text.strip()
    # TODO: 한글임을 판단하는 로직 추가
    if text == "":
        return text
    mt_result = Untypical_pipeline.papago(text)
    return mt_result
