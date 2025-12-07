"""
AI advice generator using OpenRouter API.
Builds structured prompts from player data and parses AI responses.
"""
import os
import json
import httpx
from typing import Optional
from models.player import PlayerSnapshot
from models.advice import PlayerAdvice, UpgradeAdvice, AttackStrategyAdvice


class AdviceGenerator:
    """
    Generates AI advice for Clash of Clans players using OpenRouter.
    
    TODO: Extensibility points:
    - Add support for multiple model providers
    - Implement caching for similar player profiles
    - Add prompt templates for different game modes (farming, war, trophy pushing)
    - Support for clan-wide analysis and comparisons
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "openai/gpt-4-turbo-preview"
    ):
        """
        Initialize the advice generator.
        
        Args:
            api_key: OpenRouter API key. If None, reads from OPENROUTER_API_KEY env var.
            model: Model identifier for OpenRouter (default: gpt-4-turbo-preview)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY must be provided or set in environment")
        
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def _build_prompt(self, player: PlayerSnapshot, war_focus: bool = False) -> str:
        """Build a structured prompt from player data."""
        prompt_parts = [
            "You are an expert Clash of Clans advisor. Analyze the following player data and provide structured advice.",
            "",
            f"Player: {player.name} ({player.tag})",
            f"Town Hall Level: {player.town_hall_level}",
            f"Trophies: {player.trophies}",
            f"League: {player.league or 'Unranked'}",
            f"Clan: {player.clan_name or 'No clan'}",
            "",
            "Heroes:",
        ]
        
        for hero in player.heroes:
            prompt_parts.append(f"  - {hero.name}: Level {hero.level}/{hero.max_level}")
        
        prompt_parts.append("")
        prompt_parts.append("Key Troops:")
        # Show top 10 most important troops
        important_troops = [t for t in player.troops if t.village == "home"][:10]
        for troop in important_troops:
            prompt_parts.append(f"  - {troop.name}: Level {troop.level}/{troop.max_level}")
        
        prompt_parts.append("")
        prompt_parts.append("Spells:")
        for spell in player.spells[:10]:
            prompt_parts.append(f"  - {spell.name}: Level {spell.level}/{spell.max_level}")
        
        prompt_parts.append("")
        prompt_parts.append("Available Upgrades:")
        for upgrade in player.available_upgrades[:15]:
            prompt_parts.append(f"  - {upgrade.name} ({upgrade.type}): {upgrade.current_level} -> {upgrade.max_level}")
        
        prompt_parts.append("")
        if war_focus:
            prompt_parts.append("Focus: War attacks and defense")
        else:
            prompt_parts.append("Focus: General progression and farming")
        
        prompt_parts.append("")
        prompt_parts.append("Please provide advice in the following JSON format:")
        prompt_parts.append(json.dumps({
            "upgrade_priorities": [
                {
                    "item_name": "Troop/Hero/Spell name",
                    "priority": 1-10,
                    "reason": "Why this upgrade is important"
                }
            ],
            "attack_strategies": [
                {
                    "strategy_name": "Strategy name",
                    "description": "How to use this strategy",
                    "recommended_troops": ["troop1", "troop2"],
                    "recommended_spells": ["spell1", "spell2"],
                    "difficulty": "easy|medium|hard"
                }
            ],
            "general_tips": ["tip1", "tip2"],
            "war_tips": ["war tip1"] if war_focus else None
        }, indent=2))
        
        return "\n".join(prompt_parts)

    async def generate_advice(
        self,
        player: PlayerSnapshot,
        war_focus: bool = False
    ) -> tuple[PlayerAdvice, str]:
        """
        Generate AI advice for a player.
        
        Args:
            player: Normalized player snapshot
            war_focus: Whether to focus on war strategies
            
        Returns:
            Tuple of (PlayerAdvice object, raw_response_string)
        """
        prompt = self._build_prompt(player, war_focus)
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/clashai",  # Optional
                    "X-Title": "ClashAI"  # Optional
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert Clash of Clans advisor. Always respond with valid JSON in the exact format requested."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "response_format": {"type": "json_object"}
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract the content
            raw_response = data["choices"][0]["message"]["content"]
            
            # Parse JSON response
            try:
                advice_data = json.loads(raw_response)
            except json.JSONDecodeError:
                # Fallback: try to extract JSON from markdown code blocks
                if "```json" in raw_response:
                    json_start = raw_response.find("```json") + 7
                    json_end = raw_response.find("```", json_start)
                    raw_response = raw_response[json_start:json_end].strip()
                    advice_data = json.loads(raw_response)
                else:
                    raise ValueError(f"Invalid JSON response from AI: {raw_response[:200]}")
            
            # Convert to Pydantic models
            upgrade_priorities = [
                UpgradeAdvice(**item) for item in advice_data.get("upgrade_priorities", [])
            ]
            
            attack_strategies = [
                AttackStrategyAdvice(**item) for item in advice_data.get("attack_strategies", [])
            ]
            
            advice = PlayerAdvice(
                upgrade_priorities=upgrade_priorities,
                attack_strategies=attack_strategies,
                general_tips=advice_data.get("general_tips", []),
                war_tips=advice_data.get("war_tips") if war_focus else None
            )
            
            return advice, raw_response
