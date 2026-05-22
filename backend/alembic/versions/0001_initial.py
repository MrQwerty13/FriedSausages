"""initial schema

Все таблицы прототипа Efros CI создаются одной миграцией. Если нужно
эволюционировать схему — делайте отдельные миграции, эту не правьте.

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-21
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ---------------------------------------------------------------------------
# Перечисления PostgreSQL (создаём один раз, переиспользуем во всех таблицах).
# ---------------------------------------------------------------------------
USER_ROLE = postgresql.ENUM("admin", "operator", "auditor", name="user_role")
DEVICE_TYPE = postgresql.ENUM(
    "cisco_ios",
    "mikrotik_routeros",
    "eltex_mes",
    "linux_host",
    "windows_host",
    "generic_ssh",
    name="device_type",
)
DEVICE_STATUS = postgresql.ENUM(
    "ok", "warning", "error", "unknown", name="device_status"
)
EVENT_SOURCE = postgresql.ENUM(
    "internal", "syslog", "snmp_trap", name="event_source"
)
EVENT_SEVERITY = postgresql.ENUM(
    "low", "medium", "high", "critical", name="event_severity"
)
SCHEDULE_KIND = postgresql.ENUM(
    "fetch_report",
    "run_compliance",
    "sync_vulnerabilities",
    "archive_gc",
    name="schedule_kind",
)
REQUIREMENT_SEVERITY = postgresql.ENUM(
    "low", "medium", "high", "critical", name="requirement_severity"
)
COMPLIANCE_RUN_STATUS = postgresql.ENUM(
    "running", "done", "failed", "cancelled", name="compliance_run_status"
)
VULN_SEVERITY = postgresql.ENUM(
    "none", "low", "medium", "high", "critical", name="vulnerability_severity"
)

ALL_ENUMS = (
    USER_ROLE,
    DEVICE_TYPE,
    DEVICE_STATUS,
    EVENT_SOURCE,
    EVENT_SEVERITY,
    SCHEDULE_KIND,
    REQUIREMENT_SEVERITY,
    COMPLIANCE_RUN_STATUS,
    VULN_SEVERITY,
)


def upgrade() -> None:
    bind = op.get_bind()
    for enum in ALL_ENUMS:
        enum.create(bind, checkfirst=True)

    # -----------------------------------------------------------------------
    # users
    # -----------------------------------------------------------------------
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("login", sa.String(64), nullable=False),
        sa.Column("password_hash", sa.String(256), nullable=False),
        sa.Column("email", sa.String(128), nullable=True),
        sa.Column(
            "role",
            postgresql.ENUM(name="user_role", create_type=False),
            nullable=False,
            server_default="auditor",
        ),
        sa.Column("description", sa.String(256), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "must_change_password",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("login", name="uq_users_login"),
    )
    op.create_index("ix_users_login", "users", ["login"])

    # -----------------------------------------------------------------------
    # device_groups
    # -----------------------------------------------------------------------
    op.create_table(
        "device_groups",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "parent_id",
            sa.Integer(),
            sa.ForeignKey("device_groups.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
    )
    op.create_index("ix_device_groups_parent", "device_groups", ["parent_id"])

    # -----------------------------------------------------------------------
    # auth_profiles
    # -----------------------------------------------------------------------
    op.create_table(
        "auth_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("username", sa.String(128), nullable=False),
        sa.Column("password_enc", sa.Text(), nullable=True),
        sa.Column("enable_password_enc", sa.Text(), nullable=True),
        sa.Column("private_key_enc", sa.Text(), nullable=True),
        sa.UniqueConstraint("name", name="uq_auth_profiles_name"),
    )

    # -----------------------------------------------------------------------
    # devices
    # -----------------------------------------------------------------------
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "group_id",
            sa.Integer(),
            sa.ForeignKey("device_groups.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "type",
            postgresql.ENUM(name="device_type", create_type=False),
            nullable=False,
        ),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("address", sa.String(128), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False, server_default="22"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "profile_id",
            sa.Integer(),
            sa.ForeignKey("auth_profiles.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "status",
            postgresql.ENUM(name="device_status", create_type=False),
            nullable=False,
            server_default="unknown",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_devices_group", "devices", ["group_id"])
    op.create_index("ix_devices_status", "devices", ["status"])
    op.create_index("ix_devices_type", "devices", ["type"])

    # -----------------------------------------------------------------------
    # audit_log
    # -----------------------------------------------------------------------
    op.create_table(
        "audit_log",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "ts",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("action", sa.String(64), nullable=False),
        sa.Column("target_type", sa.String(32), nullable=False),
        sa.Column("target_id", sa.String(64), nullable=True),
        sa.Column("ip", sa.String(64), nullable=True),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.execute("CREATE INDEX ix_audit_ts_desc ON audit_log (ts DESC)")
    op.execute("CREATE INDEX ix_audit_user_ts ON audit_log (user_id, ts DESC)")
    op.create_index("ix_audit_action", "audit_log", ["action"])

    # -----------------------------------------------------------------------
    # events
    # -----------------------------------------------------------------------
    op.create_table(
        "events",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "ts",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "source",
            postgresql.ENUM(name="event_source", create_type=False),
            nullable=False,
        ),
        sa.Column("type", sa.String(64), nullable=False),
        sa.Column(
            "severity",
            postgresql.ENUM(name="event_severity", create_type=False),
            nullable=False,
            server_default="low",
        ),
        sa.Column(
            "device_id",
            sa.Integer(),
            sa.ForeignKey("devices.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("fields", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.execute("CREATE INDEX ix_events_ts_desc ON events (ts DESC)")
    op.execute("CREATE INDEX ix_events_device_ts ON events (device_id, ts DESC)")
    op.execute("CREATE INDEX ix_events_severity_ts ON events (severity, ts DESC)")
    op.execute("CREATE INDEX ix_events_source_ts ON events (source, ts DESC)")
    op.create_index(
        "ix_events_fields_gin",
        "events",
        ["fields"],
        postgresql_using="gin",
    )

    # -----------------------------------------------------------------------
    # schedules
    # -----------------------------------------------------------------------
    op.create_table(
        "schedules",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("cron_expression", sa.String(64), nullable=False),
        sa.Column(
            "kind",
            postgresql.ENUM(name="schedule_kind", create_type=False),
            nullable=False,
        ),
        sa.Column(
            "params",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint("name", name="uq_schedules_name"),
    )

    # -----------------------------------------------------------------------
    # reports + report_versions (циклическая зависимость через latest_version_id)
    # -----------------------------------------------------------------------
    op.create_table(
        "reports",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "device_id",
            sa.Integer(),
            sa.ForeignKey("devices.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("report_type", sa.String(64), nullable=False),
        sa.Column(
            "taken_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        # FK на report_versions добавляем после создания таблицы.
        sa.Column("latest_version_id", sa.BigInteger(), nullable=True),
        sa.UniqueConstraint(
            "device_id", "report_type", name="uq_reports_device_type"
        ),
    )

    op.create_table(
        "report_versions",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "report_id",
            sa.BigInteger(),
            sa.ForeignKey("reports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "prev_id",
            sa.BigInteger(),
            sa.ForeignKey("report_versions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("hash", sa.String(64), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("archive_path", sa.String(512), nullable=False),
        sa.Column("diff_unified", sa.Text(), nullable=True),
        sa.Column(
            "accepted_by_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.execute(
        "CREATE INDEX ix_report_versions_report_ts "
        "ON report_versions (report_id, created_at DESC)"
    )
    op.create_index("ix_report_versions_hash", "report_versions", ["hash"])

    # Замыкаем FK reports.latest_version_id → report_versions.id
    op.create_foreign_key(
        "fk_reports_latest_version",
        source_table="reports",
        referent_table="report_versions",
        local_cols=["latest_version_id"],
        remote_cols=["id"],
        ondelete="SET NULL",
        use_alter=True,
    )

    # -----------------------------------------------------------------------
    # standards / requirements / compliance_runs / compliance_findings
    # -----------------------------------------------------------------------
    op.create_table(
        "standards",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column(
            "device_type",
            postgresql.ENUM(name="device_type", create_type=False),
            nullable=False,
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "is_builtin", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint("name", name="uq_standards_name"),
    )

    op.create_table(
        "requirements",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "standard_id",
            sa.BigInteger(),
            sa.ForeignKey("standards.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(128), nullable=True),
        sa.Column("report_type", sa.String(64), nullable=False),
        sa.Column("pcre_pattern", sa.Text(), nullable=False),
        sa.Column(
            "must_match", sa.Boolean(), nullable=False, server_default=sa.true()
        ),
        sa.Column(
            "severity",
            postgresql.ENUM(name="requirement_severity", create_type=False),
            nullable=False,
            server_default="medium",
        ),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.UniqueConstraint(
            "standard_id", "name", name="uq_requirements_standard_name"
        ),
    )
    op.create_index("ix_requirements_standard", "requirements", ["standard_id"])

    op.create_table(
        "compliance_runs",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "device_id",
            sa.Integer(),
            sa.ForeignKey("devices.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "standard_id",
            sa.BigInteger(),
            sa.ForeignKey("standards.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "status",
            postgresql.ENUM(name="compliance_run_status", create_type=False),
            nullable=False,
            server_default="running",
        ),
        sa.Column("total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("passed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
    )
    op.execute(
        "CREATE INDEX ix_compliance_runs_device_started "
        "ON compliance_runs (device_id, started_at DESC)"
    )
    op.create_index(
        "ix_compliance_runs_standard", "compliance_runs", ["standard_id"]
    )

    op.create_table(
        "compliance_findings",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "run_id",
            sa.BigInteger(),
            sa.ForeignKey("compliance_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "requirement_id",
            sa.BigInteger(),
            sa.ForeignKey("requirements.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=True),
    )
    op.create_index("ix_findings_run", "compliance_findings", ["run_id"])

    # -----------------------------------------------------------------------
    # vulnerabilities
    # -----------------------------------------------------------------------
    op.create_table(
        "vulnerabilities",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("cve_id", sa.String(32), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_modified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cvss_v3_score", sa.Numeric(3, 1), nullable=True),
        sa.Column(
            "severity",
            postgresql.ENUM(name="vulnerability_severity", create_type=False),
            nullable=False,
            server_default="none",
        ),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("vendor", sa.String(128), nullable=True),
        sa.Column("product", sa.String(128), nullable=True),
        sa.Column(
            "cpe_uri",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default="{}",
        ),
        sa.Column(
            "refs",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default="{}",
        ),
        sa.UniqueConstraint("cve_id", name="uq_vulnerabilities_cve"),
    )
    op.create_index("ix_vulnerabilities_severity", "vulnerabilities", ["severity"])
    op.create_index(
        "ix_vulnerabilities_vendor_product",
        "vulnerabilities",
        ["vendor", "product"],
    )
    op.create_index(
        "ix_vulnerabilities_cpe_gin",
        "vulnerabilities",
        ["cpe_uri"],
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_index("ix_vulnerabilities_cpe_gin", table_name="vulnerabilities")
    op.drop_index(
        "ix_vulnerabilities_vendor_product", table_name="vulnerabilities"
    )
    op.drop_index("ix_vulnerabilities_severity", table_name="vulnerabilities")
    op.drop_table("vulnerabilities")

    op.drop_index("ix_findings_run", table_name="compliance_findings")
    op.drop_table("compliance_findings")

    op.drop_index("ix_compliance_runs_standard", table_name="compliance_runs")
    op.execute("DROP INDEX IF EXISTS ix_compliance_runs_device_started")
    op.drop_table("compliance_runs")

    op.drop_index("ix_requirements_standard", table_name="requirements")
    op.drop_table("requirements")
    op.drop_table("standards")

    op.drop_constraint(
        "fk_reports_latest_version", "reports", type_="foreignkey"
    )
    op.drop_index("ix_report_versions_hash", table_name="report_versions")
    op.execute("DROP INDEX IF EXISTS ix_report_versions_report_ts")
    op.drop_table("report_versions")
    op.drop_table("reports")

    op.drop_table("schedules")

    op.drop_index("ix_events_fields_gin", table_name="events")
    op.execute("DROP INDEX IF EXISTS ix_events_source_ts")
    op.execute("DROP INDEX IF EXISTS ix_events_severity_ts")
    op.execute("DROP INDEX IF EXISTS ix_events_device_ts")
    op.execute("DROP INDEX IF EXISTS ix_events_ts_desc")
    op.drop_table("events")

    op.drop_index("ix_audit_action", table_name="audit_log")
    op.execute("DROP INDEX IF EXISTS ix_audit_user_ts")
    op.execute("DROP INDEX IF EXISTS ix_audit_ts_desc")
    op.drop_table("audit_log")

    op.drop_index("ix_devices_type", table_name="devices")
    op.drop_index("ix_devices_status", table_name="devices")
    op.drop_index("ix_devices_group", table_name="devices")
    op.drop_table("devices")

    op.drop_table("auth_profiles")

    op.drop_index("ix_device_groups_parent", table_name="device_groups")
    op.drop_table("device_groups")

    op.drop_index("ix_users_login", table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    for enum in (
        # порядок не критичен, но сначала «потребители», потом сами enum
        # они уже не используются ни одной таблицей — можно дропать в любом
        # порядке.
        "vulnerability_severity",
        "compliance_run_status",
        "requirement_severity",
        "schedule_kind",
        "event_severity",
        "event_source",
        "device_status",
        "device_type",
        "user_role",
    ):
        bind.execute(sa.text(f"DROP TYPE IF EXISTS {enum}"))
