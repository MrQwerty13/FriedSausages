"""Тесты файлового архива (`app.services.archive`)."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest


@pytest.mark.asyncio
async def test_write_and_read(tmp_archive_root):
    from app.services import archive

    ts = datetime(2026, 5, 21, 12, 0, 0, tzinfo=timezone.utc)
    rel = await archive.write(
        device_id=42, report_type="running-config", ts=ts, text="hostname r1\n"
    )
    assert rel.startswith("42/running-config/")
    assert (tmp_archive_root / rel).exists()

    text = await archive.read(rel)
    assert text == "hostname r1\n"


@pytest.mark.asyncio
async def test_stat_returns_size(tmp_archive_root):
    from app.services import archive

    ts = datetime.now(tz=timezone.utc)
    rel = await archive.write(device_id=1, report_type="x", ts=ts, text="abc")
    st = await archive.stat(rel)
    assert st.size_bytes == 3


@pytest.mark.asyncio
async def test_delete_cleans_empty_dirs(tmp_archive_root):
    from app.services import archive

    ts = datetime.now(tz=timezone.utc)
    rel = await archive.write(
        device_id=99, report_type="config", ts=ts, text="x"
    )
    assert await archive.delete(rel) is True
    assert await archive.delete(rel) is False
    # Каталог device_id/report_type должен исчезнуть
    assert not (tmp_archive_root / "99").exists()


@pytest.mark.asyncio
async def test_path_traversal_rejected(tmp_archive_root):
    from app.services import archive

    with pytest.raises(ValueError):
        await archive.read("../../../etc/passwd")
    with pytest.raises(ValueError):
        await archive.delete("../escape.txt")


@pytest.mark.db
@pytest.mark.asyncio
async def test_gc_removes_orphans(tmp_archive_root, db_session):
    """GC удаляет файлы, на которые нет ссылок в report_versions."""
    from app.services import archive

    ts = datetime.now(tz=timezone.utc)
    # Кладём 3 orphan-файла
    for i in range(3):
        await archive.write(
            device_id=i + 1, report_type="x", ts=ts, text=f"file {i}"
        )

    deleted = await archive.gc(db_session, older_than_days=0)
    assert deleted == 3
    # Архив должен быть пустым (или содержать только корень)
    leftover = [p for p in tmp_archive_root.rglob("*.txt") if p.is_file()]
    assert leftover == []
