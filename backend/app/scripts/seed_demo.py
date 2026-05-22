"""Наполнение прототипа демонстрационными данными.

Запуск:
    docker compose exec backend python -m app.scripts.seed_demo

Идемпотентен: повторный запуск не создаёт дубликатов. Если пользователь
admin уже есть — скрипт ничего не пересоздаёт, но обновляет/добивает
недостающее (события, расписания, стандарт).
"""
from __future__ import annotations

import asyncio
import hashlib
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.fernet import Fernet
from sqlalchemy import select

from app.core.db import SessionLocal
from app.core.security import hash_password
from app.core.settings import settings
from app.models.compliance import Standard
from app.models.device import (
    AuthProfile,
    Device,
    DeviceGroup,
    DeviceStatus,
    DeviceType,
)
from app.models.event import Event, EventSeverity, EventSource
from app.models.schedule import Schedule, ScheduleKind
from app.models.user import User, UserRole
from app.scripts.import_standard import import_standard_xml

# Воспроизводимая случайность, чтобы CI не шумел.
RNG = random.Random(20260521)


def _fernet_key() -> bytes:
    """Возвращает 32-байтовый ключ для AES-GCM из settings.

    settings.device_secrets_key хранится как произвольная строка; превращаем
    её в стабильный 32-байт ключ через sha256 → base64 (нужный формат Fernet).
    """
    import base64

    digest = hashlib.sha256(settings.device_secrets_key.encode()).digest()
    return base64.urlsafe_b64encode(digest)


def _encrypt_secret(plain: str) -> str:
    return Fernet(_fernet_key()).encrypt(plain.encode()).decode()


# ---------------------------------------------------------------------------
# Шаги
# ---------------------------------------------------------------------------


async def _seed_users(db) -> None:
    existing = await db.scalar(select(User).where(User.login == "admin"))
    if existing:
        print("[users] admin уже есть, пропускаю создание пользователей")
        return

    users = [
        User(
            login="admin",
            password_hash=hash_password("admin123"),
            email="admin@example.local",
            role=UserRole.ADMIN,
            description="Первичный администратор",
            must_change_password=True,
        ),
        User(
            login="operator",
            password_hash=hash_password("operator123"),
            email="operator@example.local",
            role=UserRole.OPERATOR,
            description="Сетевой оператор",
        ),
        User(
            login="auditor",
            password_hash=hash_password("auditor123"),
            email="auditor@example.local",
            role=UserRole.AUDITOR,
            description="Аудитор, только чтение",
        ),
    ]
    db.add_all(users)
    await db.flush()
    print(f"[users] создано: {len(users)}")


async def _seed_groups(db) -> dict[str, DeviceGroup]:
    by_name: dict[str, DeviceGroup] = {}
    for name, parent_name, description in [
        ("Сетевое оборудование", None, "Маршрутизаторы и коммутаторы"),
        ("Серверы", None, "Linux-серверы и хосты"),
        ("Граничные маршрутизаторы", "Сетевое оборудование", "Edge router'ы"),
    ]:
        existing = await db.scalar(select(DeviceGroup).where(DeviceGroup.name == name))
        if existing:
            by_name[name] = existing
            continue
        parent_id = by_name[parent_name].id if parent_name else None
        group = DeviceGroup(name=name, description=description, parent_id=parent_id)
        db.add(group)
        await db.flush()
        by_name[name] = group
    print(f"[groups] всего: {len(by_name)}")
    return by_name


async def _seed_auth_profile(db) -> AuthProfile:
    profile = await db.scalar(
        select(AuthProfile).where(AuthProfile.name == "Default SSH")
    )
    if profile:
        return profile
    profile = AuthProfile(
        name="Default SSH",
        username="admin",
        password_enc=_encrypt_secret("demo-password"),
    )
    db.add(profile)
    await db.flush()
    print("[profiles] создан профиль 'Default SSH'")
    return profile


async def _seed_devices(
    db, groups: dict[str, DeviceGroup], profile: AuthProfile
) -> list[Device]:
    plan = [
        ("core-router-01", DeviceType.CISCO_IOS, "10.0.1.1", "Граничные маршрутизаторы"),
        ("edge-mikrotik-01", DeviceType.MIKROTIK_ROUTEROS, "10.0.2.1", "Сетевое оборудование"),
        ("linux-bastion-01", DeviceType.LINUX_HOST, "10.0.0.5", "Серверы"),
    ]
    created: list[Device] = []
    for name, dtype, address, group_name in plan:
        existing = await db.scalar(select(Device).where(Device.name == name))
        if existing:
            created.append(existing)
            continue
        dev = Device(
            group_id=groups[group_name].id,
            type=dtype,
            name=name,
            address=address,
            port=22,
            description="Демо-устройство",
            profile_id=profile.id,
            status=DeviceStatus.UNKNOWN,
        )
        db.add(dev)
        await db.flush()
        created.append(dev)
    print(f"[devices] всего: {len(created)}")
    return created


async def _seed_schedules(db) -> None:
    plan = [
        Schedule(
            name="Сбор конфигов каждые 5 минут",
            cron_expression="*/5 * * * *",
            kind=ScheduleKind.FETCH_REPORT,
            params={"report_type": "running-config"},
        ),
        Schedule(
            name="Обновление БДУ ежедневно",
            cron_expression="0 3 * * *",
            kind=ScheduleKind.SYNC_VULNERABILITIES,
            params={},
        ),
        Schedule(
            name="GC архива по воскресеньям",
            cron_expression="30 2 * * 0",
            kind=ScheduleKind.ARCHIVE_GC,
            params={"older_than_days": 90},
        ),
    ]
    added = 0
    for sch in plan:
        exists = await db.scalar(select(Schedule).where(Schedule.name == sch.name))
        if exists:
            continue
        db.add(sch)
        added += 1
    print(f"[schedules] добавлено новых: {added}")


async def _seed_events(db, devices: list[Device]) -> None:
    existing = await db.scalar(select(Event.id).limit(1))
    if existing:
        print("[events] уже есть события, пропускаю генерацию синтетики")
        return

    severities = list(EventSeverity)
    sources = list(EventSource)
    sample_types = [
        ("Syslog-сообщение", EventSource.SYSLOG),
        ("Загрузка отчёта", EventSource.INTERNAL),
        ("Изменение отчёта", EventSource.INTERNAL),
        ("Ошибка подключения", EventSource.INTERNAL),
        ("Ошибка аутентификации", EventSource.SYSLOG),
        ("Перезагрузка устройства", EventSource.SYSLOG),
    ]
    sample_messages = [
        "Failed login from 192.168.5.7 user admin",
        "Configuration changed by user oper",
        "Link state UP on Gi0/1",
        "Interface Gi0/2 DOWN",
        "BGP neighbor 10.10.10.1 reset",
        "Memory utilization 85%",
    ]

    now = datetime.now(tz=timezone.utc)
    events: list[Event] = []
    for i in range(60):
        type_name, source = RNG.choice(sample_types)
        severity = RNG.choices(
            severities, weights=[0.45, 0.30, 0.20, 0.05], k=1
        )[0]
        device = RNG.choice(devices) if RNG.random() > 0.1 else None
        ts = now - timedelta(minutes=RNG.randint(0, 7 * 24 * 60))
        events.append(
            Event(
                ts=ts,
                source=source,
                type=type_name,
                severity=severity,
                device_id=device.id if device else None,
                fields={
                    "message": RNG.choice(sample_messages),
                    "facility": "auth" if source == EventSource.SYSLOG else "system",
                    "host": device.address if device else "localhost",
                },
            )
        )
    db.add_all(events)
    await db.flush()
    print(f"[events] сгенерировано: {len(events)}")


async def _seed_standard(db) -> None:
    exists = await db.scalar(
        select(Standard).where(Standard.name == "CIS Cisco IOS Lite")
    )
    if exists:
        print("[standards] CIS Cisco IOS Lite уже загружен")
        return

    xml_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "standards"
        / "cis_cisco_ios_lite.xml"
    )
    if not xml_path.exists():
        print(f"[standards] файл {xml_path} не найден, пропуск")
        return
    _, count = await import_standard_xml(xml_path)
    print(f"[standards] загружено требований: {count}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


async def seed() -> None:
    async with SessionLocal() as db:
        await _seed_users(db)
        groups = await _seed_groups(db)
        profile = await _seed_auth_profile(db)
        devices = await _seed_devices(db, groups, profile)
        await _seed_schedules(db)
        await _seed_events(db, devices)
        await db.commit()

    # import_standard сам управляет своей сессией
    async with SessionLocal() as db:
        await _seed_standard(db)


def main() -> int:
    asyncio.run(seed())
    print("\nГотово. Учётки по умолчанию:")
    print("  admin    / admin123    (требуется смена при первом входе)")
    print("  operator / operator123")
    print("  auditor  / auditor123")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
