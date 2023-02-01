from typing import List
from fastapi import APIRouter, Response
from backend.pipeline import untypical_pipeline
import base64


router = APIRouter(prefix="/untypical/generation")


@router.post("/", description="untypical 정보를 받아 font를 생성하고 font file 위치를 반환합니다.")
async def gen_font(classified_font : List[str], en_list: List[str]):
    Untypical_pipeline = untypical_pipeline.Untypical_Pipeline("/opt/ml/final-project-level2-cv-11/")
    
    Untypical_pipeline.font_generate_mx_font(classified_font, en_list)
    Untypical_pipeline.png2svg()
    font_path = Untypical_pipeline.svg2ttf()
    
    res = []
    for fp in font_path:
        f = open(fp[0], 'rb')
        bytes = f.read()
        encoded = base64.b64encode(bytes)
        res.append(f'data:font/ttf;base64,{str(encoded, "utf-8")}')
        f.close()
    
    return res