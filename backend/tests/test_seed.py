"""Проверка идемпотентности скрипта seed_demo."""
from __future__ import annotations

import pytest


@pytest.mark.db
@pytest.mark.asyncio
async def test_seed_demo_is_idempotent():
    from sqlalchemy import select

    from app.core.db import SessionLocal
    from app.models.device import Device
    from app.models.event import Event
    from app.models.schedule import Schedule
    from app.models.user import User
    from app.scripts.seed_demo import seed

    await seed()

    async with SessionLocal() as db:
        users_first = len(list(await db.scalars(select(User))))
        devs_first = len(list(await db.scalars(select(Device))))
        events_first = len(list(await db.scalars(select(Event))))
        sched_first = len(list(await db.scalars(select(Schedule))))

    await seed()  # повторно

    async with SessionLocal() as db:
        users_second = len(list(await db.scalars(select(User))))
        devs_second = len(list(await db.scalars(select(Device))))
        events_second = len(list(await db.scalars(select(Event))))
        sched_second = len(list(await db.scalars(select(Schedule))))

    assert users_first == users_second
    assert devs_first == devs_second
    assert events_first == events_second
    assert sched_first == sched_second
