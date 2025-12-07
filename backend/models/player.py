"""
Pydantic models for normalized player data.
Maps coc.py Player objects to clean, frontend-friendly structures.
"""

from typing import List, Optional
from pydantic import BaseModel
from coc import Player as CocPlayer


class HeroInfo(BaseModel):
    """Hero information."""

    name: str
    level: int
    max_level: int
    village: str  # "home" or "builderBase"


class TroopInfo(BaseModel):
    """Troop information."""

    name: str
    level: int
    max_level: int
    village: str  # "home" or "builderBase"


class SpellInfo(BaseModel):
    """Spell information."""

    name: str
    level: int
    max_level: int
    village: str  # "home" or "builderBase"


class UpgradeState(BaseModel):
    """Represents an upgrade that can be done."""

    name: str
    current_level: int
    max_level: int
    type: str  # "troop", "hero", "spell", "building", etc.


class PlayerSnapshot(BaseModel):
    """Normalized player snapshot for frontend consumption."""

    tag: str
    name: str
    town_hall_level: int
    exp_level: int
    trophies: int
    best_trophies: int
    war_stars: int
    attack_wins: int
    defense_wins: int
    clan_name: Optional[str] = None
    clan_tag: Optional[str] = None
    league: Optional[str] = None

    # Normalized collections
    heroes: List[HeroInfo] = []
    troops: List[TroopInfo] = []
    spells: List[SpellInfo] = []

    # Available upgrades
    available_upgrades: List[UpgradeState] = []

    class Config:
        from_attributes = True


def normalize_player(player: CocPlayer) -> PlayerSnapshot:
    """
    Convert a coc.py Player object to a normalized PlayerSnapshot.

    Args:
        player: coc.py Player object

    Returns:
        Normalized PlayerSnapshot
    """
    # Extract heroes
    heroes = []
    for hero in player.heroes:
        # Safely determine village type
        village = "home"
        if hasattr(hero, "is_home_base"):
            village = "home" if hero.is_home_base else "builderBase"
        elif hasattr(hero, "village"):
            village = hero.village
        heroes.append(
            HeroInfo(
                name=hero.name,
                level=hero.level,
                max_level=hero.max_level,
                village=village,
            )
        )

    # Extract troops
    troops = []
    for troop in player.troops:
        # Safely determine village type
        village = "home"
        if hasattr(troop, "is_home_base"):
            village = "home" if troop.is_home_base else "builderBase"
        elif hasattr(troop, "village"):
            village = troop.village
        troops.append(
            TroopInfo(
                name=troop.name,
                level=troop.level,
                max_level=troop.max_level,
                village=village,
            )
        )

    # Extract spells
    spells = []
    for spell in player.spells:
        # Safely determine village type
        village = "home"
        if hasattr(spell, "is_home_base"):
            village = "home" if spell.is_home_base else "builderBase"
        elif hasattr(spell, "village"):
            village = spell.village
        spells.append(
            SpellInfo(
                name=spell.name,
                level=spell.level,
                max_level=spell.max_level,
                village=village,
            )
        )

    # Extract available upgrades
    available_upgrades = []
    for troop in player.troops:
        if troop.level < troop.max_level:
            available_upgrades.append(
                UpgradeState(
                    name=troop.name,
                    current_level=troop.level,
                    max_level=troop.max_level,
                    type="troop",
                )
            )

    for hero in player.heroes:
        if hero.level < hero.max_level:
            available_upgrades.append(
                UpgradeState(
                    name=hero.name,
                    current_level=hero.level,
                    max_level=hero.max_level,
                    type="hero",
                )
            )

    for spell in player.spells:
        if spell.level < spell.max_level:
            available_upgrades.append(
                UpgradeState(
                    name=spell.name,
                    current_level=spell.level,
                    max_level=spell.max_level,
                    type="spell",
                )
            )

    # Build snapshot
    # Note: coc.py uses 'town_hall' not 'town_hall_level'
    return PlayerSnapshot(
        tag=player.tag,
        name=player.name,
        town_hall_level=getattr(
            player, "town_hall", getattr(player, "town_hall_level", 1)
        ),
        exp_level=player.exp_level,
        trophies=player.trophies,
        best_trophies=player.best_trophies,
        war_stars=player.war_stars,
        attack_wins=player.attack_wins,
        defense_wins=player.defense_wins,
        clan_name=player.clan.name if player.clan else None,
        clan_tag=player.clan.tag if player.clan else None,
        league=player.league.name if player.league else None,
        heroes=heroes,
        troops=troops,
        spells=spells,
        available_upgrades=available_upgrades,
    )
