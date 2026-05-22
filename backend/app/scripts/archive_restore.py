"""Восстановление прежней версии конфигурации устройства.

Использование:
    docker compose exec backend python -m app.scripts.archive_restore \\
        --device-id 12 --report-type running-config --version-id 88

После выполнения создаётся новая report_version, ссылающаяся на тот же
файл архива, и помечается как latest для соответствующего report'а.
Сам файл архива не копируется и не модифицируется.

Файл существующей версии должен лежать в архиве; если он был удалён —
команда вернёт ошибку и попросит сначала запустить полное восстановление
из бэкапа (`scripts/restore.sh`).
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import SessionLocal
from app.models.report import Report, ReportVersion
from app.services import archive


async def restore(
    db: AsyncSession,
    device_id: int,
    report_type: str,
    version_id: int,
    comment: str | None,
) -> int:
    report = await db.scalar(
        select(Report).where(
            Report.device_id == device_id, Report.report_type == report_type
        )
    )
    if not report:
        raise SystemExit(
            f"Отчёт type={report_type!r} для device_id={device_id} не найден"
        )

    source = await db.get(ReportVersion, version_id)
    if not source or source.report_id != report.id:
        raise SystemExit(
            f"Версия id={version_id} не принадлежит этому отчёту"
        )

    # Убедимся, что файл архива на месте
    try:
        await archive.stat(source.archive_path)
    except FileNotFoundError:
        raise SystemExit(
            f"Файл архива {source.archive_path} отсутствует. "
            f"Запустите scripts/restore.sh перед восстановлением версии."
        )

    new_version = ReportVersion(
        report_id=report.id,
        prev_id=report.latest_version_id,
        hash=source.hash,
        size_bytes=source.size_bytes,
        archive_path=source.archive_path,
        diff_unified=None,
        comment=comment or f"Восстановлено из версии id={version_id}",
    )
    db.add(new_version)
    await db.flush()

    report.latest_version_id = new_version.id
    report.taken_at = datetime.now(tz=timezone.utc)
    await db.commit()
    return new_version.id


async def main_async(args: argparse.Namespace) -> int:
    async with SessionLocal() as db:
        new_id = await restore(
            db,
            device_id=args.device_id,
            report_type=args.report_type,
            version_id=args.version_id,
            comment=args.comment,
        )
    print(f"Создана новая версия id={new_id}, помечена как latest")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device-id", type=int, required=True)
    parser.add_argument("--report-type", required=True)
    parser.add_argument("--version-id", type=int, required=True)
    parser.add_argument(
        "--comment", help="Опциональный комментарий к новой версии"
    )
    args = parser.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
