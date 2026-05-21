# models/compliance_rule.py
from typing import Optional


class ComplianceRule:
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str],
        pattern: str,
        severity: str,
        recommendation: Optional[str],
        enabled: bool,
    ):
        self._id = id
        self._name = name
        self._description = description
        self._pattern = pattern
        self._severity = severity
        self._recommendation = recommendation
        self._enabled = enabled

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def pattern(self) -> str:
        return self._pattern

    @property
    def severity(self) -> str:
        return self._severity

    @property
    def recommendation(self) -> Optional[str]:
        return self._recommendation

    @property
    def enabled(self) -> bool:
        return self._enabled