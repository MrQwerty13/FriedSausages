#!/usr/bin/env bash
# Полный бэкап прототипа Efros CI: дамп PostgreSQL + tar архива конфигов.
#
# Использование:
#   ./scripts/backup.sh [target_dir]
#
# По умолчанию пишет в ./backups/.
#
# Переменные окружения (читаются из .env, если файл рядом):
#   DATABASE_URL   — postgresql+asyncpg://user:pass@host:port/db
#   ARCHIVE_PATH   — путь к файловому архиву (по умолчанию /var/lib/efrosci/archive)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET_DIR="${1:-${ROOT_DIR}/backups}"

if [[ -f "${ROOT_DIR}/.env" ]]; then
    # shellcheck disable=SC1091
    set -a; source "${ROOT_DIR}/.env"; set +a
fi

: "${DATABASE_URL:?DATABASE_URL is required}"
: "${ARCHIVE_PATH:=/var/lib/efrosci/archive}"

mkdir -p "${TARGET_DIR}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
PREFIX="${TARGET_DIR}/efrosci-${STAMP}"

DUMP_FILE="${PREFIX}-db.sql.gz"
ARCHIVE_TAR="${PREFIX}-archive.tar.gz"
META_FILE="${PREFIX}-meta.txt"

# 1) Dump PostgreSQL ---------------------------------------------------------

# pg_dump хочет URI вида postgresql://... Переписываем драйвер.
PG_URI="$(printf '%s' "${DATABASE_URL}" | sed -E 's#^postgresql\+asyncpg#postgresql#')"

echo "==> pg_dump → ${DUMP_FILE}"
pg_dump --no-owner --no-privileges --format=plain --dbname="${PG_URI}" | gzip > "${DUMP_FILE}"

# 2) Tar архив ---------------------------------------------------------------

if [[ -d "${ARCHIVE_PATH}" ]]; then
    echo "==> tar архив ${ARCHIVE_PATH} → ${ARCHIVE_TAR}"
    tar -czf "${ARCHIVE_TAR}" -C "$(dirname "${ARCHIVE_PATH}")" "$(basename "${ARCHIVE_PATH}")"
else
    echo "    Архив ${ARCHIVE_PATH} не существует, создаю пустой tar"
    tar -czf "${ARCHIVE_TAR}" --files-from /dev/null
fi

# 3) Метаданные --------------------------------------------------------------

{
    echo "Efros CI Prototype backup"
    echo "Created at:    ${STAMP}"
    echo "Host:          $(hostname)"
    echo "Database URI:  ${PG_URI}"
    echo "Archive path:  ${ARCHIVE_PATH}"
    echo "Tooling:"
    echo "  pg_dump: $(pg_dump --version | head -1)"
    echo "  tar:     $(tar --version | head -1)"
} > "${META_FILE}"

# 4) Итог --------------------------------------------------------------------

echo "==> Готово:"
ls -lh "${DUMP_FILE}" "${ARCHIVE_TAR}" "${META_FILE}"
