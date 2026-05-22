"""Конфигурация pytest для тестов data-keeping зоны.

Тесты, помеченные @pytest.mark.db, требуют запущенный PostgreSQL,
доступный через переменную окружения TEST_DATABASE_URL (по умолчанию
тот же, что DATABASE_URL). Если она не задана — тесты автоматически
пропускаются.
"""
from __future__ import annotations

import asyncio
import os
import shutil
import tempfile
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


def _resolve_test_db_url() -> str | None:
    return os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL")


def pytest_collection_modifyitems(config, items):
    """Skip @pytest.mark.db tests if no test DB is available."""
    url = _resolve_test_db_url()
    if url:
        return
    skip = pytest.mark.skip(reason="TEST_DATABASE_URL не задан")
    for item in items:
        if "db" in item.keywords:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def db_session() -> AsyncIterator:
    """Чистая сессия SQLAlchemy. Каждый тест работает в отдельной транзакции
    и откатывается в конце — БД остаётся неизменной."""
    url = _resolve_test_db_url()
    assert url, "TEST_DATABASE_URL должен быть задан для @pytest.mark.db"

    # Импорт здесь, после возможного monkeypatch settings'ов
    from app import models  # noqa: F401 — регистрирует модели

    engine = create_async_engine(url, future=True)
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.connect() as conn:
        trans = await conn.begin()
        async with Session(bind=conn) as session:
            try:
                yield session
            finally:
                await trans.rollback()
    await engine.dispose()


@pytest.fixture()
def tmp_archive_root(monkeypatch) -> Path:
    """Изолированный каталог архива для одного теста."""
    root = Path(tempfile.mkdtemp(prefix="efrosci-test-archive-"))
    monkeypatch.setenv("ARCHIVE_PATH", str(root))
    # settings уже мог быть прочитан — пересоздаём
    from app.core import settings as settings_module

    settings_module.settings = settings_module.Settings()  # type: ignore[call-arg]
    yield root
    shutil.rmtree(root, ignore_errors=True)
