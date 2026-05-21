from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func

from app.database import Base


class ConfigDiff(Base):
    __tablename__ = "config_diffs"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)

    old_snapshot_id = Column(
        Integer,
        ForeignKey("config_snapshots.id"),
        nullable=False
    )

    new_snapshot_id = Column(
        Integer,
        ForeignKey("config_snapshots.id"),
        nullable=False
    )

    diff_text = Column(Text, nullable=False)

    risk_level = Column(String, nullable=False)

    summary = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )