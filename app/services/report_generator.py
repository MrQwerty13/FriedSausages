import json
from datetime import datetime


class ReportGenerator:
    @staticmethod
    def generate_json(compliance_results, vulnerabilities, diff=None):
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "compliance": compliance_results,
            "vulnerabilities": vulnerabilities,
            "diff": diff
        }

        return json.dumps(report, indent=4, ensure_ascii=False)

    @staticmethod
    def save_report(report, path):
        with open(path, "w", encoding="utf-8") as file:
            file.write(report)

        return path