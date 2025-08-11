import uuid
import subprocess
from pathlib import Path
from .celery_app import celery_app
from ..tools_registry import REGISTRY
from ..utils.summaries import write_summary
from ..schemas import Target

DATA_DIR = Path("data/reports")
DATA_DIR.mkdir(parents=True, exist_ok=True)


@celery_app.task
def run_tool(job_id: str, tool_id: str, target: dict, options: dict):
    spec = REGISTRY[tool_id]
    job_dir = DATA_DIR / job_id / tool_id
    job_dir.mkdir(parents=True, exist_ok=True)
    cmd = spec.build_cmd(Target(**target), spec.options_model(**options), str(job_dir))
    log_file = job_dir / "run.log"
    with log_file.open("w") as log:
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
        proc.wait()
    write_summary(job_dir, {"tool": tool_id, "cmd": cmd, "returncode": proc.returncode})


def enqueue_tool_job(tool_id: str, target: dict, options: dict) -> str:
    job_id = uuid.uuid4().hex
    run_tool.delay(job_id=job_id, tool_id=tool_id, target=target, options=options)
    return job_id
