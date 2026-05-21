import json
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    @staticmethod
    def generate_json(
        device: dict,
        diff_result,
        compliance_results,
        vulnerabilities,
        alerts
    ) -> str:
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "device": device,
            "diff": {
                "risk_level": diff_result.risk_level,
                "summary": diff_result.summary,
                "added_lines": diff_result.added_lines,
                "removed_lines": diff_result.removed_lines,
                "diff_text": diff_result.diff_text,
            },
            "compliance": [r.__dict__ for r in compliance_results],
            "vulnerabilities": [v.__dict__ for v in vulnerabilities],
            "alerts": [a.__dict__ for a in alerts],
        }

        return json.dumps(report, indent=4, ensure_ascii=False)

    @staticmethod
    def save_report(report: str, path: str) -> str:
        Path(path).write_text(report, encoding="utf-8")
        return path