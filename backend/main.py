import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.cad_controller import router as cad_router

app = FastAPI()

# Parse CORS origins from environment, fallback to allowing all locally
cors_origins_env = os.getenv("CORS_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in cors_origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cad_router)


@app.get("/health")
def health():
    return {"status": "ok"}