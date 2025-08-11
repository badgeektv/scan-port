from fastapi import APIRouter, HTTPException, Depends
from pathlib import Path
import json

from ..deps import require_api_key

router = APIRouter(prefix="/api/jobs")

DATA_DIR = Path("data/reports")


@router.get("/")
async def list_jobs(_=Depends(require_api_key)):
    jobs = [p.name for p in DATA_DIR.iterdir() if p.is_dir()]
    return {"jobs": jobs}


@router.get("/{job_id}")
async def get_job(job_id: str, _=Depends(require_api_key)):
    job_dir = DATA_DIR / job_id
    if not job_dir.exists():
        raise HTTPException(404, "Job not found")
    summary = {}
    summary_file = job_dir / "summary.json"
    if summary_file.exists():
        summary = json.loads(summary_file.read_text())
    return {"id": job_id, "summary": summary}
