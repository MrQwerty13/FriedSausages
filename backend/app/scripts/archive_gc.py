"""Сборщик мусора файлового архива.

Удаляет файлы из архива, на которые нет ссылок в таблице report_versions
(orphan-файлы). Не трогает БД и не удаляет записи без файлов — для этого
есть scripts/integrity_check.py.

Использование:
    docker compose exec backend python -m app.scripts.archive_gc
    docker compose exec backend python -m app.scripts.archive_gc --older-than-days 90
    docker compose exec backend python -m app.scripts.archive_gc --dry-run
"""
from __future__ import annotations

import argparse
import asyncio
import sys

from app.core.db import SessionLocal
from app.services import archive


async def run(older_than_days: int, dry_run: bool) -> int:
    if dry_run:
        # В режиме dry-run пока просто перечислим что бы удалили.
        # Реализация — простая копия логики archive.gc без unlink'ов.
        from pathlib import Path
        from sqlalchemy import select
        from app.core.settings import settings
        from app.models.report import ReportVersion

        root = Path(settings.archive_path).resolve()
        if not root.exists():
            print("Архив пуст или не создан, нечего удалять.")
            return 0

        async with SessionLocal() as db:
            referenced = {
                str((root / p).resolve())
                for p in (await db.scalars(select(ReportVersion.archive_path)))
            }

        candidates: list[str] = []
        for path in root.rglob("*.txt"):
            if not path.is_file():
                continue
            if str(path.resolve()) in referenced:
                continue
            candidates.append(str(path.relative_to(root)))

        for c in candidates:
            print(f"[dry-run] удалил бы {c}")
        print(f"[dry-run] всего файлов под удаление: {len(candidates)}")
        return len(candidates)

    async with SessionLocal() as db:
        deleted = await archive.gc(db, older_than_days=older_than_days)

    print(f"Удалено orphan-файлов: {deleted}")
    return deleted


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--older-than-days",
        type=int,
        default=0,
        help="Удалять только файлы старше N дней (по mtime). 0 = удалить все orphan.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Только показать, что было бы удалено, без реального удаления.",
    )
    args = parser.parse_args()

    asyncio.run(run(args.older_than_days, args.dry_run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
