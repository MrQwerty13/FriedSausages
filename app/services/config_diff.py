import difflib
from dataclasses import dataclass


@dataclass
class DiffResult:
    diff_text: str
    added_lines: list[str]
    removed_lines: list[str]
    risk_level: str
    summary: str


class ConfigDiff:
    DANGEROUS_PATTERNS = [
        "transport input telnet",
        "permit ip any any",
        "snmp-server community public",
        "snmp-server community private",
        "password 0",
        "username admin2",
    ]

    @classmethod
    def compare(cls, old_config: str, new_config: str) -> DiffResult:
        old_lines = old_config.splitlines()
        new_lines = new_config.splitlines()

        diff_lines = list(difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="old_config",
            tofile="new_config",
            lineterm=""
        ))

        added = [
            line[1:] for line in diff_lines
            if line.startswith("+") and not line.startswith("+++")
        ]

        removed = [
            line[1:] for line in diff_lines
            if line.startswith("-") and not line.startswith("---")
        ]

        risk = cls.calculate_risk(added)
        summary = cls.build_summary(added, removed, risk)

        return DiffResult(
            diff_text="\n".join(diff_lines),
            added_lines=added,
            removed_lines=removed,
            risk_level=risk,
            summary=summary
        )

    @classmethod
    def calculate_risk(cls, added_lines: list[str]) -> str:
        joined = "\n".join(added_lines).lower()

        critical_hits = [
            pattern for pattern in cls.DANGEROUS_PATTERNS
            if pattern in joined
        ]

        if "permit ip any any" in joined:
            return "critical"

        if critical_hits:
            return "high"

        if added_lines:
            return "medium"

        return "low"

    @staticmethod
    def build_summary(added: list[str], removed: list[str], risk: str) -> str:
        return (
            f"Добавлено строк: {len(added)}. "
            f"Удалено строк: {len(removed)}. "
            f"Уровень риска: {risk}."
        )