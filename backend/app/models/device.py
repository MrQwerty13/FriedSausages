from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models._enums import pg_enum


class DeviceType(StrEnum):
    CISCO_IOS = "cisco_ios"
    MIKROTIK_ROUTEROS = "mikrotik_routeros"
    ELTEX_MES = "eltex_mes"
    LINUX_HOST = "linux_host"
    WINDOWS_HOST = "windows_host"
    GENERIC_SSH = "generic_ssh"


class DeviceStatus(StrEnum):
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    UNKNOWN = "unknown"


class DeviceGroup(Base):
    __tablename__ = "device_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("device_groups.id", ondelete="CASCADE"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    devices: Mapped[list["Device"]] = relationship(back_populates="group", cascade="all, delete-orphan")
    parent: Mapped["DeviceGroup | None"] = relationship(remote_side="DeviceGroup.id", backref="children")


class AuthProfile(Base):
    __tablename__ = "auth_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    username: Mapped[str] = mapped_column(String(128))
    password_enc: Mapped[str | None] = mapped_column(Text, nullable=True)
    enable_password_enc: Mapped[str | None] = mapped_column(Text, nullable=True)
    private_key_enc: Mapped[str | None] = mapped_column(Text, nullable=True)


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("device_groups.id", ondelete="CASCADE"))
    type: Mapped[DeviceType] = mapped_column(pg_enum(DeviceType, name="device_type"))
    name: Mapped[str] = mapped_column(String(128))
    address: Mapped[str] = mapped_column(String(128))
    port: Mapped[int] = mapped_column(Integer, default=22)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    profile_id: Mapped[int | None] = mapped_column(
        ForeignKey("auth_profiles.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[DeviceStatus] = mapped_column(
        pg_enum(DeviceStatus, name="device_status"), default=DeviceStatus.UNKNOWN
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    group: Mapped[DeviceGroup] = relationship(back_populates="devices")
    profile: Mapped[AuthProfile | None] = relationship()
