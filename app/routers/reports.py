from fastapi import APIRouter

from app.services.report_generator import generate_html_report

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/{device_id}")
def create_report(device_id: int):
    report = generate_html_report(device_id)

    return {
        "report": report
    }