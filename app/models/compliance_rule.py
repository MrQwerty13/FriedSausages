from sqlalchemy import Column, Integer, String, Boolean, Text

from app.database import Base


class ComplianceRule(Base):
    __tablename__ = "compliance_rules"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    pattern = Column(String, nullable=False)

    severity = Column(String, nullable=False)

    recommendation = Column(Text, nullable=False)

    enabled = Column(Boolean, default=True)