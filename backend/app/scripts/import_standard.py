"""Импорт стандарта безопасности из XML.

Использование:
    docker compose exec backend python -m app.scripts.import_standard \
        --file backend/app/data/standards/cis_cisco_ios_lite.xml

Идемпотентен: повторный запуск перезаписывает требования стандарта
с тем же именем.
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from lxml import etree
from sqlalchemy import delete, select

from app.core.db import SessionLocal
from app.models.compliance import Requirement, RequirementSeverity, Standard
from app.models.device import DeviceType

TRUE_STRINGS = {"true", "1", "yes", "y"}


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in TRUE_STRINGS


async def import_standard_xml(path: Path) -> tuple[int, int]:
    """Загрузить стандарт из XML. Возвращает (standard_id, requirements_count)."""
    tree = etree.parse(str(path))
    root = tree.getroot()
    if root.tag != "standard":
        raise ValueError(f"Root tag must be <standard>, got <{root.tag}>")

    name = root.get("name", "").strip()
    device_type_code = root.get("device_type", "").strip()
    if not name or not device_type_code:
        raise ValueError("standard must have name and device_type attributes")

    try:
        device_type = DeviceType(device_type_code)
    except ValueError as exc:
        raise ValueError(
            f"Unknown device_type '{device_type_code}'. "
            f"Allowed: {[t.value for t in DeviceType]}"
        ) from exc

    is_builtin = _bool(root.get("is_builtin"), default=False)
    description = (root.get("description") or "").strip() or None

    async with SessionLocal() as db:
        standard = await db.scalar(select(Standard).where(Standard.name == name))
        if standard is None:
            standard = Standard(
                name=name,
                device_type=device_type,
                description=description,
                is_builtin=is_builtin,
            )
            db.add(standard)
            await db.flush()
        else:
            standard.device_type = device_type
            standard.description = description
            standard.is_builtin = is_builtin
            # Перетряхиваем requirements
            await db.execute(
                delete(Requirement).where(Requirement.standard_id == standard.id)
            )
            await db.flush()

        count = 0
        for req in root.iter("requirement"):
            req_name = (req.get("name") or "").strip()
            if not req_name:
                continue
            pattern = (req.get("pattern") or "").strip()
            if not pattern:
                raise ValueError(f"Requirement '{req_name}' missing pattern")

            severity_raw = (req.get("severity") or "medium").strip().lower()
            try:
                severity = RequirementSeverity(severity_raw)
            except ValueError:
                severity = RequirementSeverity.MEDIUM

            db.add(
                Requirement(
                    standard_id=standard.id,
                    name=req_name,
                    description=(req.get("description") or "").strip() or None,
                    category=(req.get("category") or "").strip() or None,
                    report_type=(req.get("report_type") or "running-config").strip(),
                    pcre_pattern=pattern,
                    must_match=_bool(req.get("must_match"), default=True),
                    severity=severity,
                    enabled=_bool(req.get("enabled"), default=True),
                )
            )
            count += 1

        await db.commit()
        return standard.id, count


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file", "-f", required=True, type=Path, help="Путь к XML-стандарту"
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if not args.file.exists():
        print(f"Файл {args.file} не найден", file=sys.stderr)
        return 1
    standard_id, count = asyncio.run(import_standard_xml(args.file))
    print(f"Импортирован стандарт id={standard_id}, требований: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
