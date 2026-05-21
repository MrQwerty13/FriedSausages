from dataclasses import dataclass


@dataclass
class ComplianceResult:
    rule: str
    status: str
    severity: str
    details: str
    recommendation: str


class ComplianceEngine:
    DEFAULT_RULES = [
        {
            "name": "Telnet disabled",
            "pattern": "transport input telnet",
            "must_not_contain": True,
            "severity": "high",
            "recommendation": "Отключить Telnet и использовать SSH."
        },
        {
            "name": "SNMP public/private disabled",
            "pattern": "snmp-server community public",
            "must_not_contain": True,
            "severity": "high",
            "recommendation": "Заменить public/private community на защищённую строку."
        },
        {
            "name": "Weak password storage disabled",
            "pattern": "password 0",
            "must_not_contain": True,
            "severity": "medium",
            "recommendation": "Использовать secret/hash вместо password 0."
        },
        {
            "name": "Dangerous ACL disabled",
            "pattern": "permit ip any any",
            "must_not_contain": True,
            "severity": "critical",
            "recommendation": "Ограничить ACL конкретными источниками и назначениями."
        },
        {
            "name": "Logging host configured",
            "pattern": "logging host",
            "must_contain": True,
            "severity": "medium",
            "recommendation": "Настроить отправку логов на централизованный сервер."
        },
    ]

    def __init__(self, rules=None):
        self.rules = rules or self.DEFAULT_RULES

    def check(self, config_text: str) -> list[ComplianceResult]:
        config_lower = config_text.lower()
        results = []

        for rule in self.rules:
            pattern = rule["pattern"].lower()

            if rule.get("must_not_contain"):
                passed = pattern not in config_lower
            elif rule.get("must_contain"):
                passed = pattern in config_lower
            else:
                passed = False

            results.append(ComplianceResult(
                rule=rule["name"],
                status="passed" if passed else "failed",
                severity=rule["severity"],
                details=f"Pattern checked: {rule['pattern']}",
                recommendation=rule["recommendation"]
            ))

        return results

    @staticmethod
    def summary(results: list[ComplianceResult]) -> dict:
        failed = [r for r in results if r.status == "failed"]

        return {
            "total": len(results),
            "passed": len(results) - len(failed),
            "failed": len(failed),
            "critical": len([r for r in failed if r.severity == "critical"]),
            "high": len([r for r in failed if r.severity == "high"]),
            "medium": len([r for r in failed if r.severity == "medium"]),
        }