"""Импорт уязвимостей из открытого NVD JSON-фида.

Использование:
    python -m app.scripts.import_nvd --year 2024
    python -m app.scripts.import_nvd --file path/to/nvdcve-2.0-2024.json.gz

NVD-фиды доступны на https://nvd.nist.gov/feeds/json/cve/2.0/
Структура файла соответствует NVD CVE 2.0 schema.

Скрипт стримит JSON и делает upsert по cve_id, не дублируя записи.
"""
from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, IO

import httpx
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.db import SessionLocal
from app.models.vulnerability import Vulnerability, VulnerabilitySeverity

NVD_URL_TEMPLATE = (
    "https://nvd.nist.gov/feeds/json/cve/2.0/nvdcve-2.0-{year}.json.gz"
)


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        # NVD пишет 2024-05-01T12:34:56.000
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(
            timezone.utc
        )
    except ValueError:
        return None


def _severity_from(metrics: dict[str, Any]) -> tuple[VulnerabilitySeverity, Decimal | None]:
    """Извлечь base severity и score из metrics блока NVD."""
    for key in ("cvssMetricV31", "cvssMetricV30"):
        items = metrics.get(key) or []
        if not items:
            continue
        primary = next((m for m in items if m.get("type") == "Primary"), items[0])
        data = primary.get("cvssData", {})
        score = data.get("baseScore")
        sev = (data.get("baseSeverity") or "NONE").lower()
        try:
            return VulnerabilitySeverity(sev), (Decimal(str(score)) if score else None)
        except ValueError:
            return VulnerabilitySeverity.NONE, None
    return VulnerabilitySeverity.NONE, None


def _description(cve: dict[str, Any]) -> str:
    for entry in cve.get("descriptions", []):
        if entry.get("lang") == "en":
            return entry.get("value", "")
    descs = cve.get("descriptions", [])
    return descs[0].get("value", "") if descs else ""


def _cpe_uris(cve: dict[str, Any]) -> list[str]:
    out: set[str] = set()
    for conf in cve.get("configurations", []) or []:
        for node in conf.get("nodes", []) or []:
            for match in node.get("cpeMatch", []) or []:
                criteria = match.get("criteria")
                if criteria:
                    out.add(criteria)
    return sorted(out)


def _references(cve: dict[str, Any]) -> list[str]:
    return [ref["url"] for ref in cve.get("references", []) if ref.get("url")]


def _vendor_product(cpe_uris: list[str]) -> tuple[str | None, str | None]:
    """Грубая эвристика: берём первый cpe:2.3:o|a — vendor и product."""
    for cpe in cpe_uris:
        parts = cpe.split(":")
        if len(parts) >= 6 and parts[0] == "cpe" and parts[1] == "2.3":
            return parts[3], parts[4]
    return None, None


async def _upsert_batch(
    rows: list[dict[str, Any]],
) -> int:
    if not rows:
        return 0
    async with SessionLocal() as db:
        stmt = pg_insert(Vulnerability).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Vulnerability.cve_id],
            set_={
                "last_modified_at": stmt.excluded.last_modified_at,
                "cvss_v3_score": stmt.excluded.cvss_v3_score,
                "severity": stmt.excluded.severity,
                "description": stmt.excluded.description,
                "vendor": stmt.excluded.vendor,
                "product": stmt.excluded.product,
                "cpe_uri": stmt.excluded.cpe_uri,
                "refs": stmt.excluded.refs,
            },
        )
        await db.execute(stmt)
        await db.commit()
        return len(rows)


def _iter_cve_records(stream: IO[bytes]):
    """Yield-ить только тело vulnerabilities[].cve без полного парсинга."""
    data = json.load(stream)
    for item in data.get("vulnerabilities", []):
        cve = item.get("cve")
        if cve:
            yield cve


def _row_from_cve(cve: dict[str, Any]) -> dict[str, Any] | None:
    cve_id = cve.get("id")
    if not cve_id:
        return None
    cpe_uris = _cpe_uris(cve)
    vendor, product = _vendor_product(cpe_uris)
    severity, score = _severity_from(cve.get("metrics", {}) or {})
    return {
        "cve_id": cve_id,
        "published_at": _parse_dt(cve.get("published")),
        "last_modified_at": _parse_dt(cve.get("lastModified")),
        "cvss_v3_score": score,
        "severity": severity.value,
        "description": _description(cve),
        "vendor": vendor,
        "product": product,
        "cpe_uri": cpe_uris,
        "refs": _references(cve),
    }


async def import_from_stream(stream: IO[bytes], batch_size: int = 500) -> int:
    total = 0
    batch: list[dict[str, Any]] = []
    for cve in _iter_cve_records(stream):
        row = _row_from_cve(cve)
        if not row:
            continue
        batch.append(row)
        if len(batch) >= batch_size:
            inserted = await _upsert_batch(batch)
            total += inserted
            batch.clear()
            print(f"  ...обработано {total}", flush=True)
    if batch:
        total += await _upsert_batch(batch)
    return total


async def import_from_file(path: Path) -> int:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rb") as f:
        return await import_from_stream(f)


async def import_from_year(year: int) -> int:
    url = NVD_URL_TEMPLATE.format(year=year)
    print(f"Загружаю {url}…")
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
    import io
    stream = gzip.GzipFile(fileobj=io.BytesIO(resp.content))
    return await import_from_stream(stream)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--year", type=int, help="Год фида NVD (например 2024)")
    g.add_argument(
        "--file",
        type=Path,
        help="Путь к локальному файлу nvdcve-2.0-*.json[.gz]",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.file:
        if not args.file.exists():
            print(f"Файл {args.file} не найден", file=sys.stderr)
            return 1
        total = asyncio.run(import_from_file(args.file))
    else:
        total = asyncio.run(import_from_year(args.year))
    print(f"Импортировано/обновлено уязвимостей: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
