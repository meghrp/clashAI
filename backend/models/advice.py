"""
Pydantic models for AI advice output.
"""
from typing import List, Optional
from pydantic import BaseModel


class UpgradeAdvice(BaseModel):
    """Advice about which upgrades to prioritize."""
    item_name: str
    priority: int  # 1-10, higher is more important
    reason: str


class AttackStrategyAdvice(BaseModel):
    """Advice about attack strategies."""
    strategy_name: str
    description: str
    recommended_troops: List[str]
    recommended_spells: List[str]
    difficulty: str  # "easy", "medium", "hard"


class PlayerAdvice(BaseModel):
    """Complete AI advice for a player."""
    # Upgrade recommendations
    upgrade_priorities: List[UpgradeAdvice] = []
    
    # Attack strategies
    attack_strategies: List[AttackStrategyAdvice] = []
    
    # General tips
    general_tips: List[str] = []
    
    # War-specific advice (if war_focus was True)
    war_tips: Optional[List[str]] = None
