# Efros Config Inspector MVP - Data Keeping Layer

Этот репозиторий содержит слой работы с данными (Data Keeping) для прототипа ConfigGuard AI (реплики Efros Config Inspector). 
Зона ответственности: **Иван**.

## Технологический стек
- **Python 3.10+**
- **SQLAlchemy 2.0+**
- **SQLite** (настроено для быстрого запуска MVP)

## Инструкция для Backend-разработчиков (Алексей и Михаил)

### 1. Установка зависимостей
`pip install -r requirements.txt`

### 2. Инициализация и демо-данные (Seed)
Для генерации БД и заполнения ее данными для демо-сценария (устройство `Router-01` и базовые проверки ИБ) выполните:
`python seed.py`
Это создаст файл `efros_inspector.db` в корне проекта.
