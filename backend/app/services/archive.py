"""Файловый архив отчётов и конфигураций.

Структура хранения:
    {settings.archive_path}/{device_id}/{report_type}/{timestamp}.txt

Соответствует функции 4 «Архив текстовых конфигураций и отчётов»
оригинального ПК. Версии в БД (`report_versions`) ссылаются на файлы
через колонку `archive_path` (относительный путь от archive root).

Владелец: Иван. Потребитель: Михаил (report_loader).
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import aiofiles
import aiofiles.os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.models.report import ReportVersion


@dataclass
class FileStat:
    size_bytes: int
    created_at: datetime


def _root() -> Path:
    root = Path(settings.archive_path)
    root.mkdir(parents=True, exist_ok=True)
    return root


def _safe_join(*parts: str) -> Path:
    """Безопасный join: запрещает выход за пределы archive root."""
    root = _root().resolve()
    path = root.joinpath(*parts).resolve()
    if not str(path).startswith(str(root)):
        raise ValueError(f"Path escape detected: {path}")
    return path


def make_relative_path(device_id: int, report_type: str, ts: datetime) -> str:
    """Сформировать относительный путь для архивного файла."""
    safe_type = report_type.replace("/", "_").replace("\\", "_")
    stamp = ts.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{device_id}/{safe_type}/{stamp}.txt"


async def write(device_id: int, report_type: str, ts: datetime, text: str) -> str:
    """Записать отчёт в архив. Возвращает относительный путь."""
    rel_path = make_relative_path(device_id, report_type, ts)
    full_path = _safe_join(rel_path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(full_path, "w", encoding="utf-8") as f:
        await f.write(text)
    return rel_path


async def read(rel_path: str) -> str:
    """Прочитать архивный файл по относительному пути."""
    full_path = _safe_join(rel_path)
    if not full_path.exists():
        raise FileNotFoundError(rel_path)
    async with aiofiles.open(full_path, "r", encoding="utf-8") as f:
        return await f.read()


async def delete(rel_path: str) -> bool:
    """Удалить архивный файл. Возвращает True если файл существовал."""
    full_path = _safe_join(rel_path)
    if not full_path.exists():
        return False
    await aiofiles.os.remove(full_path)
    # Удалим пустые директории-родители (до root).
    parent = full_path.parent
    root = _root().resolve()
    while parent != root and parent.exists() and not any(parent.iterdir()):
        parent.rmdir()
        parent = parent.parent
    return True


async def stat(rel_path: str) -> FileStat:
    """Метаданные архивного файла."""
    full_path = _safe_join(rel_path)
    if not full_path.exists():
        raise FileNotFoundError(rel_path)
    st = full_path.stat()
    return FileStat(
        size_bytes=st.st_size,
        created_at=datetime.fromtimestamp(st.st_ctime, tz=timezone.utc),
    )


async def gc(db: AsyncSession, *, older_than_days: int = 0) -> int:
    """Удалить файлы из архива, на которые нет ссылок в report_versions.

    Если older_than_days > 0 — учитываются только файлы старше N дней
    (по mtime). Возвращает число удалённых файлов.

    Внимание: orphan-записи в report_versions без файла этой функцией
    НЕ чистятся. Для двусторонней проверки используется
    scripts/integrity_check.py.
    """
    root = _root().resolve()
    referenced: set[str] = set()
    rows = await db.scalars(select(ReportVersion.archive_path))
    for path in rows:
        referenced.add(str((root / path).resolve()))

    deleted = 0
    now_ts = datetime.now(tz=timezone.utc).timestamp()
    threshold = older_than_days * 86400

    for path in root.rglob("*.txt"):
        if not path.is_file():
            continue
        if str(path.resolve()) in referenced:
            continue
        if older_than_days > 0 and (now_ts - path.stat().st_mtime) < threshold:
            continue
        path.unlink()
        deleted += 1

    # Чистим пустые каталоги.
    for path in sorted(root.rglob("*"), key=lambda p: -len(str(p))):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()

    return deleted


async def restore_to_db(
    db: AsyncSession,
    *,
    rel_path: str,
    new_archive_path: str | None = None,
) -> int:
    """Создать новый report_version из существующего файла архива.

    Используется, когда нужно «откатить» устройство к прежней версии
    конфигурации. Файл копируется (с новым timestamp), а в БД создаётся
    запись, которая становится latest_version_id для отчёта.

    Возвращает id новой записи report_version.
    Реализация — в scripts/archive_restore.py, чтобы не создавать
    тут циклическую зависимость с loader'ом Михаила.
    """
    raise NotImplementedError(
        "Используйте scripts/archive_restore.py для восстановления версий"
    )


def make_archive_root_writable() -> None:
    """Идемпотентно создаёт корень архива. Полезно для смокового
    запуска приложения и тестов."""
    _root()


def remove_archive_root_for_tests() -> None:
    """Только для тестов: полностью удалить корень архива."""
    root = Path(settings.archive_path)
    if root.exists():
        shutil.rmtree(root)
