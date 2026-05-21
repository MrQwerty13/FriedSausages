from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func

from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)

    type = Column(String, nullable=False)

    severity = Column(String, nullable=False)

    message = Column(Text, nullable=False)

    status = Column(String, default="open")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )