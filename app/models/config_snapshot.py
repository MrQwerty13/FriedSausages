from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func

from app.database import Base


class ConfigSnapshot(Base):
    __tablename__ = "config_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)

    version_number = Column(Integer, nullable=False)

    config_text = Column(Text, nullable=False)

    config_hash = Column(String, nullable=False)

    collected_by = Column(String, nullable=False)

    source = Column(String, nullable=False)

    collected_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )