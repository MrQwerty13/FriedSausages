"""Реестр всех ORM-моделей прототипа.

Импорт каждой модели обязателен — без него Alembic не «увидит» таблицу
в Base.metadata. Любая новая модель должна быть добавлена в список ниже.
"""
from app.models.audit import AuditLog
from app.models.compliance import (
    ComplianceFinding,
    ComplianceRun,
    ComplianceRunStatus,
    Requirement,
    RequirementSeverity,
    Standard,
)
from app.models.device import (
    AuthProfile,
    Device,
    DeviceGroup,
    DeviceStatus,
    DeviceType,
)
from app.models.event import Event, EventSeverity, EventSource
from app.models.report import Report, ReportVersion
from app.models.schedule import Schedule, ScheduleKind
from app.models.user import User, UserRole
from app.models.vulnerability import Vulnerability, VulnerabilitySeverity

__all__ = [
    # users
    "User",
    "UserRole",
    # devices
    "Device",
    "DeviceGroup",
    "DeviceType",
    "DeviceStatus",
    "AuthProfile",
    # audit
    "AuditLog",
    # events
    "Event",
    "EventSource",
    "EventSeverity",
    # schedules
    "Schedule",
    "ScheduleKind",
    # reports
    "Report",
    "ReportVersion",
    # compliance
    "Standard",
    "Requirement",
    "RequirementSeverity",
    "ComplianceRun",
    "ComplianceRunStatus",
    "ComplianceFinding",
    # vulnerabilities
    "Vulnerability",
    "VulnerabilitySeverity",
]
