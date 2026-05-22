# Data keeping — зона Ивана

> Документ синхронизируется с `docs/OWNERSHIP.md` и `prompts/ivan_data.md`.
> Если меняешь файл из своей зоны — обновляй и этот README.

## Что входит в зону

Всё, что связано с **данными** прототипа Efros CI:

- **Схема БД** — PostgreSQL 15, все ORM-модели (`backend/app/models/*`)
- **Миграции** — Alembic с async-engine (`backend/alembic/`)
- **Файловый архив** — конфиги и отчёты на диске (`backend/app/services/archive.py`)
- **Сид-данные** — стартовое наполнение БД для демо (`backend/app/scripts/seed_demo.py`)
- **Импорт справочников** — стандарты compliance (XML) и уязвимости CVE (NVD JSON)
- **Бэкап/восстановление** — pg_dump + tar архива (`scripts/backup.sh`, `scripts/restore.sh`)
- **Контроль целостности** — orphan-файлы и broken-link версии
- **Справочники** — типы устройств, уровни критичности (`backend/app/data/*.yaml`)
- **Тесты** на всё перечисленное (`backend/tests/`)

Зона **не покрывает**: API-эндпоинты (Алексей и Михаил), бизнес-логику
коннекторов и compliance-движок (Михаил), фронтенд (Николай).
**Но** все они потребляют то, что ты строишь, поэтому стабильность схемы и
скриптов — приоритет.

## Структура файлов

```
backend/
├── alembic/
│   ├── env.py                          ← async-engine + Base.metadata
│   ├── script.py.mako                  ← шаблон новых миграций
│   └── versions/
│       └── 0001_initial.py             ← все 14 таблиц одной миграцией
├── alembic.ini                          ← конфиг (URL читается из env)
├── pytest.ini                           ← pytest + marker @pytest.mark.db
├── app/
│   ├── models/
│   │   ├── __init__.py                 ← реестр всех моделей
│   │   ├── _enums.py                   ← helper pg_enum() для StrEnum
│   │   ├── user.py
│   │   ├── device.py
│   │   ├── audit.py
│   │   ├── event.py
│   │   ├── schedule.py
│   │   ├── report.py                   ← reports + report_versions
│   │   ├── compliance.py               ← standards, requirements, runs, findings
│   │   └── vulnerability.py
│   ├── data/
│   │   ├── device_types.yaml           ← справочник типов устройств
│   │   ├── severity_levels.yaml        ← уровни критичности
│   │   └── standards/
│   │       └── cis_cisco_ios_lite.xml  ← встроенный стандарт (10 правил)
│   ├── services/
│   │   └── archive.py                  ← async API файлового архива
│   └── scripts/
│       ├── seed_demo.py                ← наполнение БД демо-данными
│       ├── import_standard.py          ← импорт XML стандарта
│       ├── import_nvd.py               ← импорт CVE из NVD
│       ├── archive_gc.py               ← удаление orphan-файлов
│       ├── archive_restore.py          ← откат на прежнюю версию конфига
│       └── integrity_check.py          ← БД ↔ архив
└── tests/
    ├── conftest.py                     ← фикстуры: db_session, tmp_archive_root
    ├── test_models.py
    ├── test_archive.py
    ├── test_import_standard.py
    └── test_seed.py

scripts/
├── backup.sh                            ← полный бэкап (БД + архив)
└── restore.sh                           ← восстановление из бэкапа
```

## Список таблиц

| Таблица | Описание | Где модель |
|---|---|---|
| `users` | Локальные пользователи (admin/operator/auditor) | `models/user.py` |
| `device_groups` | Иерархия групп устройств | `models/device.py` |
| `auth_profiles` | Профили SSH/SNMP с шифрованными секретами | `models/device.py` |
| `devices` | Контролируемое оборудование | `models/device.py` |
| `audit_log` | Действия пользователей в консоли | `models/audit.py` |
| `events` | Журнал событий (syslog/internal/snmp) | `models/event.py` |
| `schedules` | Расписания Celery beat | `models/schedule.py` |
| `reports` | Отчёт = (устройство, тип отчёта) | `models/report.py` |
| `report_versions` | Версии в архиве с diff'ом | `models/report.py` |
| `standards` | Стандарты compliance | `models/compliance.py` |
| `requirements` | PCRE-правила стандарта | `models/compliance.py` |
| `compliance_runs` | Запуск стандарта на устройстве | `models/compliance.py` |
| `compliance_findings` | Результаты прогона | `models/compliance.py` |
| `vulnerabilities` | CVE из NVD/БДУ | `models/vulnerability.py` |

## Команды на каждый день

Все Python-скрипты запускаются модулем (так корректно резолвится `app.*`):

```bash
# Применить миграции
docker compose exec backend alembic upgrade head

# Откатиться на одну миграцию назад
docker compose exec backend alembic downgrade -1

# Снести всё (только для dev!)
docker compose exec backend alembic downgrade base

# Наполнить БД демо-данными (идемпотентно)
docker compose exec backend python -m app.scripts.seed_demo

# Загрузить стандарт compliance из XML
docker compose exec backend python -m app.scripts.import_standard \
    --file backend/app/data/standards/cis_cisco_ios_lite.xml

# Импорт уязвимостей за 2024 год
docker compose exec backend python -m app.scripts.import_nvd --year 2024

# GC файлового архива (dry-run сначала!)
docker compose exec backend python -m app.scripts.archive_gc --dry-run
docker compose exec backend python -m app.scripts.archive_gc --older-than-days 90

# Откатить устройство на прежнюю версию конфига
docker compose exec backend python -m app.scripts.archive_restore \
    --device-id 12 --report-type running-config --version-id 88

# Проверка целостности БД ↔ архив
docker compose exec backend python -m app.scripts.integrity_check

# Бэкап и восстановление (запускать с хоста)
./scripts/backup.sh ./backups
./scripts/restore.sh ./backups/efrosci-20260521T120000Z

# Прогон тестов своей зоны
docker compose exec backend pytest tests/
```

## Создание новой миграции

При любом изменении модели:

```bash
docker compose exec backend alembic revision --autogenerate -m "add some_column"
# отредактируй сгенерированный файл в backend/alembic/versions/
docker compose exec backend alembic upgrade head
# обязательно проверь downgrade на dev:
docker compose exec backend alembic downgrade -1
docker compose exec backend alembic upgrade head
```

**Правила:**
- одна миграция = одно семантическое изменение
- никогда не правишь уже применённые миграции — только новые
- в `downgrade()` всегда есть рабочий обратный путь
- индексы под все ожидаемые WHERE
- для PostgreSQL ENUM используй helper `app.models._enums.pg_enum`

## Контракты с командой

| Если... | То... |
|---|---|
| Алексей хочет новое поле в `users` или `audit_log` | PR с reviewer = Иван, миграция + правка модели |
| Михаил просит таблицу для compliance/reports | Cогласуем поля в `docs/CONTRACTS.md`, потом миграция |
| Николай хочет видеть новое поле в API-ответе | Сначала Алексей/Михаил правят схему, потом Иван миграцию |
| Кто-то добавил seed-данные → нужны в демо | Обнови `scripts/seed_demo.py` идемпотентно |
| Татьяна спрашивает «зачем эта таблица» | Дополни `docs/CONTRACTS.md` разделом про неё |

## Чеклист перед мержом

- [ ] `pytest tests/` — все 12+ тестов зелёные
- [ ] `alembic upgrade head && alembic downgrade base && alembic upgrade head` без ошибок
- [ ] для новых моделей: добавил в `models/__init__.py` и индексы
- [ ] для скриптов: новая команда документирована в этом README
- [ ] обновил `docs/CONTRACTS.md`, если поменялись поля
- [ ] PR-ревьюер из `docs/OWNERSHIP.md` назначен

## Что я уже сделал (готово к коммиту)

Все файлы по списку выше **уже созданы и протестированы** на живой
PostgreSQL 16. Тесты проходят (12/12). Round-trip backup→restore проверен.
`seed_demo` идемпотентен. Готово к push'у в ветку `dev_db`.
