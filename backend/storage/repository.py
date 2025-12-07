"""
Repository abstraction for database operations.
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from storage.schema import PlayerSnapshot, AdviceResponse, get_session, init_db


class PlayerRepository:
    """Repository for player snapshot operations."""

    def __init__(self, db_path: str = "clashai.db"):
        self.db_path = db_path
        init_db(db_path)

    def save_snapshot(
        self,
        player_tag: str,
        raw_json: str,
        town_hall_level: Optional[int] = None
    ) -> PlayerSnapshot:
        """Save a player snapshot to the database."""
        db = get_session(self.db_path)
        try:
            snapshot = PlayerSnapshot(
                player_tag=player_tag,
                raw_json=raw_json,
                town_hall_level=town_hall_level,
                timestamp=datetime.utcnow()
            )
            db.add(snapshot)
            db.commit()
            db.refresh(snapshot)
            return snapshot
        finally:
            db.close()

    def get_latest_snapshot(self, player_tag: str) -> Optional[PlayerSnapshot]:
        """Get the most recent snapshot for a player tag."""
        db = get_session(self.db_path)
        try:
            return db.query(PlayerSnapshot)\
                .filter(PlayerSnapshot.player_tag == player_tag)\
                .order_by(PlayerSnapshot.timestamp.desc())\
                .first()
        finally:
            db.close()

    def get_snapshot_history(
        self,
        player_tag: str,
        limit: int = 10
    ) -> List[PlayerSnapshot]:
        """Get recent snapshots for a player tag."""
        db = get_session(self.db_path)
        try:
            return db.query(PlayerSnapshot)\
                .filter(PlayerSnapshot.player_tag == player_tag)\
                .order_by(PlayerSnapshot.timestamp.desc())\
                .limit(limit)\
                .all()
        finally:
            db.close()


class AdviceRepository:
    """Repository for advice response operations."""

    def __init__(self, db_path: str = "clashai.db"):
        self.db_path = db_path
        init_db(db_path)

    def save_advice(
        self,
        snapshot_id: int,
        raw_response: str,
        model_used: str,
        war_focus: bool = False
    ) -> AdviceResponse:
        """Save an AI advice response."""
        db = get_session(self.db_path)
        try:
            advice = AdviceResponse(
                snapshot_id=snapshot_id,
                raw_response=raw_response,
                model_used=model_used,
                war_focus=1 if war_focus else 0,
                timestamp=datetime.utcnow()
            )
            db.add(advice)
            db.commit()
            db.refresh(advice)
            return advice
        finally:
            db.close()
