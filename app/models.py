import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Column, DateTime, String, Text, func
from sqlalchemy.orm import DeclarativeBase


def utcnow() -> datetime:
    return datetime.now(UTC)


def pk_uuid() -> str:
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String(36), primary_key=True, default=pk_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50))
    location = Column(String(255))
    linkedin_url = Column(String(500))
    current_role = Column(String(255))
    summary = Column(Text)
    skills = Column(JSON, default=list)
    experience = Column(JSON, default=list)
    education = Column(JSON, default=list)
    certifications = Column(JSON, default=list)
    parsed_resume_raw = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
