from fastapi import FastAPI
from backend.routers import txt_extraction, machine_translation

app = FastAPI()

app.include_router(txt_extraction.router)
app.include_router(machine_translation.router)
