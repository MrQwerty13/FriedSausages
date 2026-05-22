"""Расписания периодических задач (Celery beat).

Соответствует функциям 3.2 «Запуск проверок по расписанию» и
2.4 «Управление устройствами».

Владелец: Иван. Потребитель: Михаил (scheduler.reload_beat_schedule).
"""
from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models._enums import pg_enum


class ScheduleKind(StrEnum):
    FETCH_REPORT = "fetch_report"
    RUN_COMPLIANCE = "run_compliance"
    SYNC_VULNERABILITIES = "sync_vulnerabilities"
    ARCHIVE_GC = "archive_gc"


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    cron_expression: Mapped[str] = mapped_column(String(64), nullable=False)
    kind: Mapped[ScheduleKind] = mapped_column(
        pg_enum(ScheduleKind, name="schedule_kind"), nullable=False
    )
    # Аргументы для целевой задачи: device_id, standard_id, report_type, …
    params: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_run_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
