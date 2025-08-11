from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from ..schemas import Target
from ..tools_registry import REGISTRY
from ..workers.tasks import enqueue_tool_job
from ..deps import require_api_key  # dépendance qui vérifie x-api-key

router = APIRouter(prefix="/api")


@router.post("/scan/{tool_id}")
def scan_tool(tool_id: str, payload: dict, _=Depends(require_api_key)):
    spec = REGISTRY.get(tool_id)
    if not spec:
        raise HTTPException(404, f"Outil inconnu: {tool_id}")
    try:
        target = Target.model_validate(payload.get("target", {}))
    except ValidationError as e:
        raise HTTPException(422, detail=e.errors())
    if target.kind not in spec.allowed_kinds:
        raise HTTPException(422, f"Cible {target.kind} non supportée pour {tool_id}")
    try:
        options = spec.options_model.model_validate(payload.get("options") or {})
    except ValidationError as e:
        raise HTTPException(422, detail=e.errors())
    job_id = enqueue_tool_job(
        tool_id=tool_id, target=target.model_dump(), options=options.model_dump()
    )
    return {"id": job_id, "tool": tool_id, "status": "queued"}
