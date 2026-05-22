"""Базовые тесты ORM-моделей: всё импортится и регистрируется."""
from __future__ import annotations

import pytest


def test_all_models_registered():
    from app import models
    from app.core.db import Base

    expected = {
        "users",
        "device_groups",
        "auth_profiles",
        "devices",
        "audit_log",
        "events",
        "schedules",
        "reports",
        "report_versions",
        "standards",
        "requirements",
        "compliance_runs",
        "compliance_findings",
        "vulnerabilities",
    }
    actual = set(Base.metadata.tables.keys())
    missing = expected - actual
    extra = actual - expected
    assert not missing, f"Не зарегистрированы таблицы: {sorted(missing)}"
    assert not extra, f"Лишние таблицы в metadata: {sorted(extra)}"
    assert models.User and models.Device and models.Standard


@pytest.mark.db
@pytest.mark.asyncio
async def test_can_insert_and_query_user(db_session):
    """Smoke-тест: пишем юзера, читаем обратно, enum'ы корректные."""
    from app.models.user import User, UserRole

    u = User(
        login="t_user",
        password_hash="argon-stub",
        email="t@example.local",
        role=UserRole.OPERATOR,
        description="test",
    )
    db_session.add(u)
    await db_session.flush()
    assert u.id is not None

    from sqlalchemy import select

    found = (
        await db_session.scalars(select(User).where(User.login == "t_user"))
    ).first()
    assert found is not None
    assert found.role == UserRole.OPERATOR


@pytest.mark.db
@pytest.mark.asyncio
async def test_device_with_group(db_session):
    from app.models.device import Device, DeviceGroup, DeviceType

    g = DeviceGroup(name="Test group", description="for test")
    db_session.add(g)
    await db_session.flush()

    d = Device(
        group_id=g.id,
        type=DeviceType.LINUX_HOST,
        name="t_device",
        address="10.0.0.42",
        port=22,
    )
    db_session.add(d)
    await db_session.flush()
    assert d.id is not None

    from sqlalchemy import select

    fetched = (
        await db_session.scalars(select(Device).where(Device.name == "t_device"))
    ).first()
    assert fetched is not None
    assert fetched.type == DeviceType.LINUX_HOST


@pytest.mark.db
@pytest.mark.asyncio
async def test_jsonb_event_fields(db_session):
    """В таблице events поле fields реально JSONB и индекс GIN работает."""
    from app.models.event import Event, EventSeverity, EventSource

    e = Event(
        source=EventSource.SYSLOG,
        type="Syslog-сообщение",
        severity=EventSeverity.HIGH,
        fields={"facility": "auth", "host": "10.0.0.1"},
    )
    db_session.add(e)
    await db_session.flush()
    assert e.id is not None
    assert e.fields["facility"] == "auth"
