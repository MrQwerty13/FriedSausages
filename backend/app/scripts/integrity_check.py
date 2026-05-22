"""Проверка целостности «БД ↔ архив».

Сценарий:
    1) Файл архива есть, но `report_versions` на него не ссылается → orphan-файл.
       Чистится `archive_gc`.
    2) В БД есть `report_version.archive_path`, но файл отсутствует на диске →
       broken-link. Это серьёзнее: значит файл удалили мимо нашего GC.

Использование:
    docker compose exec backend python -m app.scripts.integrity_check
    docker compose exec backend python -m app.scripts.integrity_check --fix-broken
        # автоматически отметит broken-версии комментарием (но не удалит их)

Возвращает exit code 0, если расхождений нет; 1 — если что-то найдено.
Полезно встроить в CI или периодическую задачу.
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select

from app.core.db import SessionLocal
from app.core.settings import settings
from app.models.report import ReportVersion


async def check(fix_broken: bool) -> int:
    root = Path(settings.archive_path).resolve()
    if not root.exists():
        print(f"Архив {root} не создан, считаем что расхождений нет.")
        return 0

    async with SessionLocal() as db:
        rows = (
            await db.execute(
                select(ReportVersion.id, ReportVersion.archive_path)
            )
        ).all()
        referenced = {r.archive_path: r.id for r in rows}

        # 1) orphan-файлы
        orphan_files: list[str] = []
        referenced_abs = {
            str((root / p).resolve()) for p in referenced
        }
        for path in root.rglob("*.txt"):
            if not path.is_file():
                continue
            if str(path.resolve()) not in referenced_abs:
                orphan_files.append(str(path.relative_to(root)))

        # 2) broken-link записи
        broken_versions: list[tuple[int, str]] = []
        for rel_path, version_id in referenced.items():
            if not (root / rel_path).exists():
                broken_versions.append((version_id, rel_path))

        if orphan_files:
            print(f"⚠️  Orphan-файлы в архиве: {len(orphan_files)}")
            for f in orphan_files[:20]:
                print(f"     {f}")
            if len(orphan_files) > 20:
                print(f"     … и ещё {len(orphan_files) - 20}")
        else:
            print("✔  Orphan-файлов в архиве нет")

        if broken_versions:
            print(
                f"❌ В БД есть {len(broken_versions)} версий "
                f"со ссылкой на отсутствующий файл"
            )
            for vid, p in broken_versions[:20]:
                print(f"     version_id={vid} archive_path={p}")
            if len(broken_versions) > 20:
                print(f"     … и ещё {len(broken_versions) - 20}")

            if fix_broken:
                now = datetime.now(tz=timezone.utc).isoformat()
                for vid, _ in broken_versions:
                    v = await db.get(ReportVersion, vid)
                    if v:
                        existing = v.comment or ""
                        v.comment = (
                            existing + f"\n[integrity_check {now}] файл архива отсутствует"
                        ).strip()
                await db.commit()
                print(f"   Отмечено комментарием: {len(broken_versions)}")
        else:
            print("✔  Все ссылки из БД на архив корректны")

    return 0 if not (orphan_files or broken_versions) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fix-broken",
        action="store_true",
        help="Добавить комментарий к broken-версиям (не удалять)",
    )
    args = parser.parse_args()
    return asyncio.run(check(args.fix_broken))


if __name__ == "__main__":
    sys.exit(main())
