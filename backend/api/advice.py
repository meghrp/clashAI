"""
FastAPI routes for AI advice endpoints.
"""

import json
from fastapi import APIRouter, HTTPException, Body
from typing import Optional
from pydantic import BaseModel
from services.coc_client import CocClient
from services.advice_generator import AdviceGenerator
from models.player import normalize_player
from models.advice import PlayerAdvice
from storage.repository import PlayerRepository, AdviceRepository

router = APIRouter()
player_repo = PlayerRepository()
advice_repo = AdviceRepository()


class AdviceRequest(BaseModel):
    """Request model for advice endpoint."""

    tag: str
    war_focus: bool = False
    model: Optional[str] = None  # Optional model override


@router.post("/advice", response_model=PlayerAdvice)
async def get_advice(request: AdviceRequest = Body(...)):
    """
    Generate AI advice for a player.

    Accepts a player tag and optional flags (like war_focus).
    Fetches player data, normalizes it, requests AI advice, persists the response,
    and returns structured advice.
    """
    try:
        # Fetch player data
        async with CocClient() as coc_client:
            player = await coc_client.get_player(request.tag)
            snapshot = normalize_player(player)

            # Save player snapshot (convert player object to dict)
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
            db_snapshot = player_repo.save_snapshot(
                player_tag=snapshot.tag,
                raw_json=raw_json,
                town_hall_level=snapshot.town_hall_level,
            )

        # Generate advice
        model = request.model or "openai/gpt-4-turbo-preview"
        advice_gen = AdviceGenerator(model=model)
        advice, raw_response = await advice_gen.generate_advice(
            snapshot, war_focus=request.war_focus
        )

        # Save advice response
        advice_repo.save_advice(
            snapshot_id=db_snapshot.id,
            raw_response=raw_response,
            model_used=model,
            war_focus=request.war_focus,
        )

        return advice

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        error_type = type(e).__name__
        if "NotFound" in error_type:
            raise HTTPException(
                status_code=404, detail=f"Player with tag {request.tag} not found"
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
                status_code=500, detail=f"Error generating advice: {str(e)}"
            )
