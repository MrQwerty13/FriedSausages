from fastapi import APIRouter

from app.services.vulnerability_scanner import scan_vulnerabilities

router = APIRouter(prefix="/vulnerabilities", tags=["Vulnerabilities"])


@router.post("/scan")
def scan_device(os_version: str):
    vulnerabilities = scan_vulnerabilities(os_version)

    return {
        "vulnerabilities": vulnerabilities
    }