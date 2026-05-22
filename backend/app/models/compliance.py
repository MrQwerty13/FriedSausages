"""Стандарты безопасности, требования, прогоны и финдинги.

Соответствует функциям 3.5/3.11 «Аудит конфигураций по политикам»
и «Compliance проверки» оригинального ПК.

Владелец моделей: Иван. Потребитель: Михаил (compliance_engine).
"""
from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models._enums import pg_enum
from app.models.device import DeviceType


class ComplianceRunStatus(StrEnum):
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RequirementSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Standard(Base):
    __tablename__ = "standards"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    device_type: Mapped[DeviceType] = mapped_column(
        pg_enum(DeviceType, name="device_type"), nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_builtin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    requirements: Mapped[list["Requirement"]] = relationship(
        back_populates="standard", cascade="all, delete-orphan"
    )


class Requirement(Base):
    __tablename__ = "requirements"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    standard_id: Mapped[int] = mapped_column(
        ForeignKey("standards.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(128), nullable=True)
    report_type: Mapped[str] = mapped_column(String(64), nullable=False)
    pcre_pattern: Mapped[str] = mapped_column(Text, nullable=False)
    must_match: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    severity: Mapped[RequirementSeverity] = mapped_column(
        pg_enum(RequirementSeverity, name="requirement_severity"),
        default=RequirementSeverity.MEDIUM,
        nullable=False,
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("standard_id", "name", name="uq_requirements_standard_name"),
        Index("ix_requirements_standard", "standard_id"),
    )

    standard: Mapped[Standard] = relationship(back_populates="requirements")


class ComplianceRun(Base):
    __tablename__ = "compliance_runs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id", ondelete="CASCADE"), nullable=False
    )
    standard_id: Mapped[int] = mapped_column(
        ForeignKey("standards.id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[ComplianceRunStatus] = mapped_column(
        pg_enum(ComplianceRunStatus, name="compliance_run_status"),
        default=ComplianceRunStatus.RUNNING,
        nullable=False,
    )
    total: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    passed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_compliance_runs_device_started", "device_id", started_at.desc()),
        Index("ix_compliance_runs_standard", "standard_id"),
    )

    findings: Mapped[list["ComplianceFinding"]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )


class ComplianceFinding(Base):
    __tablename__ = "compliance_findings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    run_id: Mapped[int] = mapped_column(
        ForeignKey("compliance_runs.id", ondelete="CASCADE"), nullable=False
    )
    requirement_id: Mapped[int | None] = mapped_column(
        ForeignKey("requirements.id", ondelete="SET NULL"), nullable=True
    )
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    evidence: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_findings_run", "run_id"),
    )

    run: Mapped[ComplianceRun] = relationship(back_populates="findings")
