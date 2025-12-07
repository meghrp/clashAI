"""
FastAPI routes for player data endpoints.
"""

import json
from fastapi import APIRouter, HTTPException, Path
from typing import List
from services.coc_client import CocClient
from models.player import PlayerSnapshot, normalize_player
from storage.repository import PlayerRepository
from pydantic import BaseModel

router = APIRouter()
player_repo = PlayerRepository()


class PlayerHistoryItem(BaseModel):
    """Metadata for a player snapshot."""

    id: int
    timestamp: str
    town_hall_level: int


@router.get("/player/{tag}", response_model=PlayerSnapshot)
async def get_player(
    tag: str = Path(..., description="Player tag (with or without #)")
):
    """
    Fetch latest player info from Clash of Clans API.
    Saves raw JSON to database and returns normalized PlayerSnapshot.
    """
    try:
        async with CocClient() as coc_client:
            player = await coc_client.get_player(tag)

            # Normalize player data
            snapshot = normalize_player(player)

            # Save raw JSON to database (convert player object to dict)
            # Note: coc.py uses 'town_hall' not 'town_hall_level'
            town_hall = getattr(
                player, "town_hall", getattr(player, "town_hall_level", 1)
            )
            raw_json = json.dumps(
                {
                    "tag": player.tag,
                    "name": player.name,
                    "town_hall_level": town_hall,
                    "exp_level": player.exp_level,
                    "trophies": player.trophies,
                    "best_trophies": player.best_trophies,
                    "war_stars": player.war_stars,
                    "attack_wins": player.attack_wins,
                    "defense_wins": player.defense_wins,
                    "clan": (
                        {"name": player.clan.name, "tag": player.clan.tag}
                        if player.clan
                        else None
                    ),
                    "league": player.league.name if player.league else None,
                }
            )
            player_repo.save_snapshot(
                player_tag=snapshot.tag,
                raw_json=raw_json,
                town_hall_level=snapshot.town_hall_level,
            )

            return snapshot

    except Exception as e:
        error_type = type(e).__name__
        if "NotFound" in error_type:
            raise HTTPException(
                status_code=404, detail=f"Player with tag {tag} not found"
            )
        elif "Maintenance" in error_type:
            raise HTTPException(
                status_code=503, detail="Clash of Clans API is in maintenance"
            )
        elif "Forbidden" in error_type:
            raise HTTPException(
                status_code=403, detail="Invalid API key or access denied"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Error fetching player: {str(e)}"
            )


@router.get("/player/{tag}/history", response_model=List[PlayerHistoryItem])
async def get_player_history(
    tag: str = Path(..., description="Player tag (with or without #)")
):
    """
    Get recent stored snapshots metadata for a player.
    """
    # Normalize tag
    if not tag.startswith("#"):
        tag = "#" + tag

    snapshots = player_repo.get_snapshot_history(tag, limit=20)

    return [
        PlayerHistoryItem(
            id=s.id,
            timestamp=s.timestamp.isoformat(),
            town_hall_level=s.town_hall_level or 0,
        )
        for s in snapshots
    ]
