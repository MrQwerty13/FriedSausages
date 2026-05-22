"""Тесты импорта стандарта compliance из XML."""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.mark.db
@pytest.mark.asyncio
async def test_import_cis_cisco_ios_lite():
    """Идемпотентный импорт встроенного стандарта."""
    from sqlalchemy import select

    from app.core.db import SessionLocal
    from app.models.compliance import Requirement, Standard
    from app.scripts.import_standard import import_standard_xml

    xml_path = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "data"
        / "standards"
        / "cis_cisco_ios_lite.xml"
    )
    assert xml_path.exists()

    standard_id, count = await import_standard_xml(xml_path)
    assert count >= 5

    # Повторный импорт — то же количество, без дубликатов
    standard_id_2, count_2 = await import_standard_xml(xml_path)
    assert standard_id_2 == standard_id
    assert count_2 == count

    async with SessionLocal() as db:
        st = await db.get(Standard, standard_id)
        assert st is not None
        assert st.is_builtin
        rows = await db.scalars(
            select(Requirement).where(Requirement.standard_id == standard_id)
        )
        all_reqs = list(rows)
        assert len(all_reqs) == count
        # PCRE-паттерны не пустые
        assert all(r.pcre_pattern for r in all_reqs)


@pytest.mark.asyncio
async def test_import_rejects_bad_xml(tmp_path):
    from app.scripts.import_standard import import_standard_xml

    bad = tmp_path / "bad.xml"
    bad.write_text("<not-a-standard/>", encoding="utf-8")
    with pytest.raises(ValueError, match="Root tag"):
        await import_standard_xml(bad)
