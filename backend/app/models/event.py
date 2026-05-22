"""Журнал событий: syslog, SNMP-traps, внутренние события сервера ПК.

Соответствует функциям 1.2.3 «Сбор, обработка событий» и
3.8/4 «Журнал событий устройств».

Потребители: Алексей (API /events, триггеры), Михаил (syslog/SNMP/internal-эмиттеры).
"""
from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models._enums import pg_enum


class EventSource(StrEnum):
    INTERNAL = "internal"
    SYSLOG = "syslog"
    SNMP_TRAP = "snmp_trap"


class EventSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    source: Mapped[EventSource] = mapped_column(
        pg_enum(EventSource, name="event_source"), nullable=False
    )
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[EventSeverity] = mapped_column(
        pg_enum(EventSeverity, name="event_severity"),
        nullable=False,
        default=EventSeverity.LOW,
    )
    device_id: Mapped[int | None] = mapped_column(
        ForeignKey("devices.id", ondelete="SET NULL"), nullable=True
    )
    # Произвольные поля: facility/severity/host/message для syslog,
    # oid/values для SNMP, любые kv для internal.
    fields: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        Index("ix_events_ts_desc", ts.desc()),
        Index("ix_events_device_ts", "device_id", ts.desc()),
        Index("ix_events_severity_ts", "severity", ts.desc()),
        Index("ix_events_source_ts", "source", ts.desc()),
        Index("ix_events_fields_gin", "fields", postgresql_using="gin"),
    )
