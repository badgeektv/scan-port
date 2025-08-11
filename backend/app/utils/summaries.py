from pathlib import Path
import json


def write_summary(job_dir: Path, data: dict) -> None:
    summary_file = job_dir / "summary.json"
    summary_file.write_text(json.dumps(data, indent=2))
