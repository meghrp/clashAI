"""
SQLite schema for storing raw player data and AI advice responses.

TODO: Extensibility points:
- Add indexes for common queries (town hall level, trophies range)
- Add support for tracking upgrade history over time
- Add clan member relationships table
- Add scheduled refresh tracking
"""
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()


class PlayerSnapshot(Base):
    """Raw player data snapshot from Clash of Clans API."""
    __tablename__ = "player_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    player_tag = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    raw_json = Column(Text, nullable=False)  # Store full JSON response
    town_hall_level = Column(Integer, index=True)  # For quick filtering/indexing

    # Relationship to advice responses
    advice_responses = relationship("AdviceResponse", back_populates="snapshot")


class AdviceResponse(Base):
    """AI advice responses linked to player snapshots."""
    __tablename__ = "advice_responses"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey("player_snapshots.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    raw_response = Column(Text, nullable=False)  # Store raw AI response
    model_used = Column(String)  # Track which model was used
    war_focus = Column(Integer, default=0)  # Boolean flag (0/1)

    # Relationship back to snapshot
    snapshot = relationship("PlayerSnapshot", back_populates="advice_responses")


def get_engine(db_path: str = "clashai.db"):
    """Create SQLAlchemy engine for SQLite database."""
    return create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})


def get_session(db_path: str = "clashai.db"):
    """Create a database session."""
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def init_db(db_path: str = "clashai.db"):
    """Initialize the database schema."""
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
