# Efros Config Inspector — прототип

> Учебный прототип ПК «Efros Config Inspector» v.4 (АО «Газинформсервис»).
> Команда из 5 человек, метод vibe-coding (Cursor / Claude / Copilot).

---

## Запуск демо за 30 секунд

Просто двойной клик по `efros-ci-demo.html`. Откроется в браузере, никаких установок.

**Демо-аккаунты:**

| Логин | Пароль | Роль |
|---|---|---|
| `admin` | `admin123` | администратор |
| `operator` | `operator123` | оператор |
| `auditor` | `auditor123` | аудитор (только чтение) |

**Что показывает демо:**
- Логин с тремя ролями
- Мониторинг с метриками, графиками и журналом событий
- Управление устройствами (добавление, проверка подключения)
- История версий конфигов и diff между ними
- Журнал событий с фильтрами
- Прогон стандарта CIS Cisco IOS Lite с 10 правилами
- Настройки пользователей и расписаний

Это **mock-стенд** для презентации. Реальная сборка с PostgreSQL и FastAPI описана ниже.

---

## Что под капотом

```
┌─────────────────────────────────────────────┐
│  Frontend — React + TS + Tailwind + Vite    │
│  (зона Николая)                             │
└──────────────────┬──────────────────────────┘
                   │ HTTP /api/v1 + WebSocket
┌──────────────────▼──────────────────────────┐
│  Backend — FastAPI + SQLAlchemy 2 async     │
│  Auth, RBAC, audit (Алексей)                │
│  Connectors, compliance, syslog (Михаил)    │
└──────────────────┬──────────────────────────┘
                   │ SQL
┌──────────────────▼──────────────────────────┐
│  PostgreSQL 15 — 14 таблиц                  │
│  Alembic миграции, demo seed, архив         │
│  (зона Ивана — готово полностью)            │
└─────────────────────────────────────────────┘
```

| Слой | Технологии | Зона |
|---|---|---|
| UI | React 18 + TypeScript + Vite + Tailwind + Lucide | Николай |
| API | FastAPI 0.115 + Pydantic 2 + JWT + argon2 | Алексей, Михаил |
| Worker / sync | Celery 5 + Redis 7 + APScheduler | Михаил |
| Connectors | Netmiko, Paramiko, pysnmp | Михаил |
| DB | PostgreSQL 15 + SQLAlchemy 2 async + Alembic | **Иван (готово)** |
| Infra | Docker Compose, MailHog | команда |
| Docs | Markdown в `docs/` | Татьяна |

---

## Команда и зоны

| Кто | Роль | Главные файлы |
|---|---|---|
| Алексей | Backend core (auth, RBAC, события) | `backend/app/api/auth.py`, `users.py`, `events.py` |
| Михаил | Backend network (коннекторы, compliance) | `backend/app/services/connectors/`, `compliance_engine.py` |
| Николай | Frontend (вся консоль) | `frontend/` |
| **Иван** | **Data keeping (БД, миграции, импорт, бэкап)** | `backend/app/models/`, `alembic/`, `app/scripts/` |
| Татьяна | Документация и релизы | `docs/`, `README.md`, `CHANGELOG.md` |

---

## Реальный запуск стека (для разработки)

```bash
git clone https://github.com/MrQwerty13/FriedSausages.git
cd FriedSausages
cp .env.example .env
docker compose up -d --build
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.scripts.seed_demo
```

- Веб-консоль: <http://localhost:5173>
- API + Swagger: <http://localhost:8000/docs>
- MailHog: <http://localhost:8025>

После `seed_demo` в БД: 3 пользователя, 3 устройства, 3 расписания, 60 событий, стандарт CIS на 10 правил.

---

## Чекпоинты

| Чекпоинт | Цель | Срок |
|---|---|---|
| **0 — Всё стартует** | Логин работает, Swagger показывает эндпоинты | конец недели 1 |
| **1 — Устройство в системе** | Оператор добавил Linux-хост, проверил подключение | конец недели 2 |
| **2 — Конфиги и история** | Снимаются конфиги по расписанию, diff между версиями | конец недели 4 |
| **3 — Compliance и события** | CIS-проверки работают, syslog приходит, триггеры шлют письма | конец недели 6 |
| **4 — Релиз 0.1.0** | End-to-end сценарий записан на видео, бэкап восстанавливается | конец недели 8 |

---

## Что готово сейчас (статус 22.05.2026)

### ✅ Зона data keeping (Иван) — 100%

- 14 ORM-моделей PostgreSQL с правильными ENUM через helper `pg_enum()`
- Alembic initial-миграция (round-trip upgrade↔downgrade проверен)
- Файловый архив с защитой от path traversal, GC, integrity check
- 7 скриптов: `seed_demo`, `import_standard`, `import_nvd`, `archive_gc`, `archive_restore`, `integrity_check`, `create_admin`
- Bash-скрипты `backup.sh` / `restore.sh` (round-trip проверен)
- Встроенный стандарт `CIS Cisco IOS Lite` на 10 PCRE-правил
- 12 pytest-тестов — все зелёные на PG 16

### 🟡 Backend core (Алексей) — ~30%

- Готовы: FastAPI bootstrap, JWT-auth (`/auth/login`, `/me`, `/refresh`), RBAC, argon2id
- Осталось: audit-middleware, rate-limit на логин, /users CRUD, /events с фильтрами, WebSocket `/ws/notifications`, тесты

### 🟡 Backend network (Михаил) — ~20%

- Готовы: интерфейс DeviceConnector, плагин Linux-host, Celery-app
- Осталось: Cisco/Mikrotik коннекторы, report_loader с хешированием и diff, compliance-движок, syslog-парсер, beat из БД, тесты

### 🟢 Frontend (Николай) — каркас готов

- Готовы: Vite + React + TS + Tailwind, Sidebar, Header, Dashboard, mock-данные
- Осталось: страница логина с AuthContext, замена mock на API-вызовы (`src/api/`), интеграция с бэком

### 🟡 Документация (Татьяна) — ~60%

- Готовы: ARCHITECTURE, INSTALL, ROADMAP, TEAM_ROLES, OWNERSHIP, CONTRACTS, MODULES, VIBE_CODING
- Осталось: 4 руководства пользователя/администратора, API.md, скриншоты, демо-видео 5-7 минут

---

## Демо-сценарий для презентации (5 минут)

1. **Открыть `efros-ci-demo.html` двойным кликом**
2. Залогиниться `admin / admin123` — показать, что есть 3 роли
3. Показать **Мониторинг**: 4 метрики, граф событий по severity, список самых уязвимых
4. Перейти в **Устройства** → нажать «+ Добавить устройство», заполнить форму, увидеть тост о проверке подключения
5. Открыть **Отчёты** → нажать «Diff» на v.12 → показать подсветку добавленных/удалённых строк
6. Открыть **События** → показать фильтры по severity и источнику, 8 разных событий с разными severity
7. Открыть **Compliance** → показать 10 правил CIS, нажать «Перезапустить проверку», увидеть результат
8. **Выйти и зайти `auditor / auditor123`** → показать, что кнопка «Добавить устройство» исчезла (RBAC)

---

## Структура репозитория

```
FriedSausages/
├── backend/
│   ├── app/
│   │   ├── api/             ← FastAPI эндпоинты (Алексей/Михаил)
│   │   ├── models/          ← ORM-модели (Иван) ✓ готово
│   │   ├── services/        ← Бизнес-логика
│   │   │   ├── archive.py   ← (Иван) ✓ готово
│   │   │   └── connectors/  ← (Михаил)
│   │   ├── scripts/         ← Утилиты (Иван) ✓ готово
│   │   ├── workers/         ← Celery (Михаил)
│   │   └── data/            ← Справочники (Иван) ✓ готово
│   ├── alembic/             ← Миграции (Иван) ✓ готово
│   └── tests/               ← 12 тестов ✓ зелёные
├── frontend/                ← React + TS (Николай)
├── docs/                    ← Документация (Татьяна)
├── scripts/                 ← Bash-утилиты бэкапа (Иван) ✓ готово
└── docker-compose.yml
```

---

## Ссылки

- Репозиторий: <https://github.com/MrQwerty13/FriedSausages>
- Демо-стенд: открыть `efros-ci-demo.html` в браузере
- Прототипный продукт: <https://www.gaz-is.ru/produkty/zashchita-it-infrastrukturi/efros-config-inspector>

---

*Документ собран 22.05.2026 для презентации команде.*
