"""Отчёты с устройств и их версии в архиве.

Соответствует функциям 4 «Управление устройствами» / «Архив текстовых
конфигураций и отчётов» оригинального ПК.

Один Report — это «срез типа отчёта для устройства» (например, running-config
для core-router-01). ReportVersion — конкретная зафиксированная версия.

Владелец моделей: Иван. Потребитель: Михаил (report_loader, diff_engine).
"""
from datetime import datetime

from sqlalchemy import (
    BigInteger,
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


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id", ondelete="CASCADE"), nullable=False
    )
    report_type: Mapped[str] = mapped_column(String(64), nullable=False)
    taken_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    latest_version_id: Mapped[int | None] = mapped_column(
        ForeignKey("report_versions.id", ondelete="SET NULL", use_alter=True),
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint("device_id", "report_type", name="uq_reports_device_type"),
    )

    versions: Mapped[list["ReportVersion"]] = relationship(
        back_populates="report",
        cascade="all, delete-orphan",
        foreign_keys="ReportVersion.report_id",
        order_by="ReportVersion.created_at.desc()",
    )


class ReportVersion(Base):
    __tablename__ = "report_versions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id", ondelete="CASCADE"), nullable=False
    )
    prev_id: Mapped[int | None] = mapped_column(
        ForeignKey("report_versions.id", ondelete="SET NULL"), nullable=True
    )
    # sha256(text) в hex
    hash: Mapped[str] = mapped_column(String(64), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Относительно settings.archive_path
    archive_path: Mapped[str] = mapped_column(String(512), nullable=False)
    diff_unified: Mapped[str | None] = mapped_column(Text, nullable=True)
    accepted_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_report_versions_report_ts", "report_id", created_at.desc()),
        Index("ix_report_versions_hash", "hash"),
    )

    report: Mapped[Report] = relationship(
        back_populates="versions", foreign_keys=[report_id]
    )
