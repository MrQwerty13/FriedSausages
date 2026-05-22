# Зона data keeping — ветка `dev_db`

Эта ветка содержит работу Ивана по поддержке данных прототипа Efros CI.

## Что внутри
- **`backend/app/models/`** — 14 ORM-моделей PostgreSQL
- **`backend/alembic/`** — миграции с async-engine
- **`backend/app/services/archive.py`** — файловый архив конфигов
- **`backend/app/scripts/`** — скрипты сопровождения (seed, import, gc, restore, integrity)
- **`backend/app/data/`** — справочники (типы устройств, severity, встроенные стандарты)
- **`backend/tests/`** — 12 pytest-тестов, все зелёные на PG 16
- **`scripts/backup.sh`** и **`scripts/restore.sh`** — резервное копирование

## Документация по зоне
См. подробный документ: [`backend/README_DATA.md`](backend/README_DATA.md)

## Быстрая проверка
```bash
docker compose up -d
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.scripts.seed_demo
docker compose exec backend pytest tests/
```

После сидинга в БД должно появиться: 3 пользователя, 3 группы, 3 устройства,
3 расписания, 60 событий, 1 стандарт с 10 требованиями.
