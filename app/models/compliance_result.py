from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func

from app.database import Base


class ComplianceResult(Base):
    __tablename__ = "compliance_results"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)

    snapshot_id = Column(
        Integer,
        ForeignKey("config_snapshots.id"),
        nullable=False
    )

    rule_id = Column(
        Integer,
        ForeignKey("compliance_rules.id"),
        nullable=False
    )

    status = Column(String, nullable=False)

    details = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )