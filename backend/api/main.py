# backend/api/main.py

import logging
from fastapi import FastAPI
from backend.api.routes import router
from backend.config import Settings
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# configure the root logger (or get uvicorn’s)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")  # you can also use __name__

app = FastAPI()

@app.on_event("startup")
async def print_settings():
    cfg = Settings()
    logger.info("Loaded settings: %r", cfg.dict())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("backend.api.main:app", host="127.0.0.1", port=8000, reload=True)
