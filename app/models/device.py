from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip_address = Column(String, nullable=False, unique=True)
    vendor = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    os_version = Column(String, nullable=False)
    status = Column(String, default="offline")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )