from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import (
    txt_extraction,
    machine_translation,
    untypical_txt_extraction,
    untypical_machine_translation,
    untypical_generation,
    test,
)

app = FastAPI()

# TODO: 배포 단계에서는 프론트 서버의 도메인으로 변경해야 함
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(txt_extraction.router)
app.include_router(machine_translation.router)
app.include_router(untypical_txt_extraction.router)
app.include_router(untypical_machine_translation.router)
app.include_router(untypical_generation.router)
app.include_router(test.router)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": str(exc)})
