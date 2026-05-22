"""Утилиты для согласованной работы с PostgreSQL ENUM-типами.

SQLAlchemy 2 при работе с StrEnum по умолчанию пишет имена (ADMIN),
а в БД у нас значения (admin). values_callable выравнивает это.
"""
from enum import Enum
from typing import TypeVar

from sqlalchemy import Enum as SAEnum

E = TypeVar("E", bound=Enum)


def pg_enum(enum_cls: type[E], *, name: str) -> SAEnum:
    """Создать SAEnum, который сериализует Python-enum в его .value."""
    return SAEnum(
        enum_cls,
        name=name,
        values_callable=lambda cls: [e.value for e in cls],
        native_enum=True,
        create_type=False,  # Тип создаётся миграцией, не моделью
    )
