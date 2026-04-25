from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class RequestType(str, Enum):
    PRICING = "pricing"
    DEMO_REQUEST = "demo_request"
    CONSULTATION_REQUEST = "consultation_request"
    INTEGRATION_QUESTION = "integration_question"
    PARTNERSHIP = "partnership"
    SUPPORT = "support"
    OTHER = "other"


class LeadStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    QUALIFIED = "qualified"
    HANDOFF = "handoff"
    DISQUALIFIED = "disqualified"
    CLOSED = "closed"


class SenderType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    AGENT = "agent"
    SYSTEM = "system"


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    request_type: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True)
    use_case: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    market: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    budget: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    timeline: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    status: Mapped[str] = mapped_column(
        String(50), default=LeadStatus.NEW.value, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="lead", cascade="all, delete-orphan")
    conversation_state: Mapped[Optional["ConversationState"]] = relationship(
        back_populates="lead",
        uselist=False,
        cascade="all, delete-orphan",
    )
    event_logs: Mapped[list["EventLog"]] = relationship(
        back_populates="lead", cascade="all, delete-orphan")
    handoffs: Mapped[list["Handoff"]] = relationship(
        back_populates="lead", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id"), nullable=False, index=True)

    sender: Mapped[str] = mapped_column(String(20), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    detected_intent: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="messages")


class ConversationState(Base):
    __tablename__ = "conversation_states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey(
        "leads.id"), nullable=False, unique=True, index=True)

    current_flow: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True)
    collected_fields: Mapped[dict] = mapped_column(
        JSON, default=dict, nullable=False)
    qualification_score: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False)
    handoff_required: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    lead: Mapped["Lead"] = relationship(back_populates="conversation_state")


class FAQItem(Base):
    __tablename__ = "faq_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)


class EventLog(Base):
    __tablename__ = "event_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id"), nullable=False, index=True)

    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="event_logs")


class Handoff(Base):
    __tablename__ = "handoffs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id"), nullable=False, index=True)

    reason: Mapped[str] = mapped_column(Text, nullable=False)
    assigned_to: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="pending", nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="handoffs")
