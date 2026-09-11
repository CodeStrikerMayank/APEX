from fastapi import APIRouter, Query
from backend.app.services.open_mm_rl_service import OpenMMRLService

router = APIRouter(prefix="/curriculum", tags=["Curriculum & Open-MM-RL V1"])
_open_mm_rl_service = OpenMMRLService()


@router.get("/open-mm-rl/sample")
def get_open_mm_rl_sample_v1(
    offset: int = Query(0, ge=0, description="Offset index for dataset pagination"),
    length: int = Query(10, ge=1, le=100, description="Number of problem rows to fetch")
):
    """
    GET /api/v1/curriculum/open-mm-rl/sample & /api/curriculum/open-mm-rl/sample
    Fetches structured multimodal STEM problems from Hugging Face Open-MM-RL dataset.
    Features 2-tier resilience (HF API with 15s timeout + local cache fallback),
    LaTeX typesetting data, multimodal image URLs, and mapped APEX concept IDs.
    """
    return _open_mm_rl_service.fetch_live_rows(offset=offset, length=length)
