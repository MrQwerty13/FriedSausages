#!/usr/bin/env bash
# Восстановление прототипа из бэкапа (сделанного backup.sh).
#
# Использование:
#   ./scripts/restore.sh path/to/backups/efrosci-YYYYMMDDTHHMMSSZ
#
# (укажи префикс без суффиксов -db.sql.gz / -archive.tar.gz)
#
# ВНИМАНИЕ: команда снесёт текущую БД и каталог архива.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [[ $# -lt 1 ]]; then
    echo "usage: $0 <backup_prefix>" >&2
    echo "       (например ./backups/efrosci-20260521T1200Z)" >&2
    exit 2
fi

PREFIX="$1"
DUMP_FILE="${PREFIX}-db.sql.gz"
ARCHIVE_TAR="${PREFIX}-archive.tar.gz"

if [[ ! -f "${DUMP_FILE}" ]]; then
    echo "Не найден ${DUMP_FILE}" >&2; exit 1
fi
if [[ ! -f "${ARCHIVE_TAR}" ]]; then
    echo "Не найден ${ARCHIVE_TAR}" >&2; exit 1
fi

if [[ -f "${ROOT_DIR}/.env" ]]; then
    # shellcheck disable=SC1091
    set -a; source "${ROOT_DIR}/.env"; set +a
fi

: "${DATABASE_URL:?DATABASE_URL is required}"
: "${ARCHIVE_PATH:=/var/lib/efrosci/archive}"

PG_URI="$(printf '%s' "${DATABASE_URL}" | sed -E 's#^postgresql\+asyncpg#postgresql#')"

# Парсим имя БД из URI (часть после последнего '/' и до '?')
DB_NAME="$(printf '%s' "${PG_URI}" | sed -E 's#.*/([^/?]+).*#\1#')"
ADMIN_URI="$(printf '%s' "${PG_URI}" | sed -E "s#/${DB_NAME}([?]|\$)#/postgres\\1#")"

echo "Будут уничтожены:"
echo "  - БД '${DB_NAME}' (через ${PG_URI})"
echo "  - Каталог архива ${ARCHIVE_PATH}"
read -r -p "Продолжить? (yes/no) " ans
if [[ "${ans}" != "yes" ]]; then
    echo "Отменено."; exit 0
fi

# 1) Восстановить БД ---------------------------------------------------------

echo "==> drop+create database ${DB_NAME}"
psql "${ADMIN_URI}" -v ON_ERROR_STOP=1 <<SQL
DROP DATABASE IF EXISTS "${DB_NAME}";
CREATE DATABASE "${DB_NAME}";
SQL

echo "==> psql restore ← ${DUMP_FILE}"
gunzip -c "${DUMP_FILE}" | psql -v ON_ERROR_STOP=1 "${PG_URI}"

# 2) Восстановить архив ------------------------------------------------------

echo "==> очищаю архив ${ARCHIVE_PATH}"
rm -rf "${ARCHIVE_PATH:?}"
mkdir -p "$(dirname "${ARCHIVE_PATH}")"

echo "==> tar -xzf ${ARCHIVE_TAR} → $(dirname "${ARCHIVE_PATH}")"
tar -xzf "${ARCHIVE_TAR}" -C "$(dirname "${ARCHIVE_PATH}")"

echo "==> Готово. Рекомендуем запустить:"
echo "    python -m app.scripts.integrity_check"
