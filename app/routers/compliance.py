from fastapi import APIRouter

from app.services.compliance_engine import run_compliance_checks

router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.post("/check")
def check_config(config_text: str):
    results = run_compliance_checks(config_text)

    return {
        "results": results
    }