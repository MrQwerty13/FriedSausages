from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ip_address = Column(String, unique=True, index=True)
    vendor = Column(String)
    device_type = Column(String)
    os_version = Column(String)
    status = Column(String, default="online")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    snapshots = relationship("ConfigSnapshot", back_populates="device")
    alerts = relationship("Alert", back_populates="device")
    vulnerabilities = relationship("Vulnerability", back_populates="device")

class ConfigSnapshot(Base):
    __tablename__ = "config_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    version_number = Column(Integer)
    config_text = Column(Text)
    config_hash = Column(String)
    collected_by = Column(String)
    collected_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String)

    device = relationship("Device", back_populates="snapshots")

class ConfigDiff(Base):
    __tablename__ = "config_diffs"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    old_snapshot_id = Column(Integer, ForeignKey("config_snapshots.id"))
    new_snapshot_id = Column(Integer, ForeignKey("config_snapshots.id"))
    diff_text = Column(Text)
    risk_level = Column(String)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class ComplianceRule(Base):
    __tablename__ = "compliance_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    pattern = Column(String)
    severity = Column(String)
    recommendation = Column(Text)
    enabled = Column(Boolean, default=True)

class ComplianceResult(Base):
    __tablename__ = "compliance_results"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    snapshot_id = Column(Integer, ForeignKey("config_snapshots.id"))
    rule_id = Column(Integer, ForeignKey("compliance_rules.id"))
    status = Column(String)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    cve_id = Column(String, index=True)
    title = Column(String)
    severity = Column(String)
    description = Column(Text)
    recommendation = Column(Text)
    detected_at = Column(DateTime, default=datetime.utcnow)

    device = relationship("Device", back_populates="vulnerabilities")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    type = Column(String)
    severity = Column(String)
    message = Column(Text)
    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)

    device = relationship("Device", back_populates="alerts")
