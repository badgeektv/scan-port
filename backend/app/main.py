from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

from .routers import scans, jobs

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Pentest API")
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scans.router)
app.include_router(jobs.router)


@app.get("/api/healthz")
async def healthz():
    return {"status": "ok"}
