"""
Clash of Clans API client wrapper using coc.py.
Handles rate limiting, retries, and provides typed access to player data.
"""

import os
import asyncio
from typing import Optional
import coc
from coc import Player


class CocClient:
    """Wrapper around coc.py Client with rate limiting and error handling."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Clash of Clans client.

        Args:
            api_key: Clash of Clans API key. If None, reads from COC_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("COC_API_KEY")
        if not self.api_key:
            raise ValueError("COC_API_KEY must be provided or set in environment")

        self.client = coc.Client()
        self._initialized = False

    async def initialize(self):
        """Initialize the client connection."""
        if not self._initialized:
            # await self.client.login(self.api_key)
            await self.client.login(
                "zebrafish931@carpkingdom.com", "DMK@vdg6emb6ndr*dby"
            )
            self._initialized = True

    async def get_player(self, tag: str) -> Player:
        """
        Fetch player data from Clash of Clans API.

        Args:
            tag: Player tag (with or without #)

        Returns:
            Player object from coc.py

        Raises:
            coc.NotFound: If player not found
            coc.Maintenance: If API is in maintenance
            coc.Forbidden: If API key is invalid
        """
        await self.initialize()

        # Normalize tag (ensure it starts with #)
        if not tag.startswith("#"):
            tag = "#" + tag

        # Fetch player with retry logic and load game data
        max_retries = 3
        for attempt in range(max_retries):
            try:
                player = await self.client.get_player(tag, load_game_data=True)
                return player
            except coc.NotFound:
                raise
            except (coc.Maintenance, coc.Forbidden) as e:
                raise
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2**attempt)  # Exponential backoff
                    continue
                raise

    async def close(self):
        """Close the client connection."""
        if self._initialized:
            await self.client.close()
            self._initialized = False

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
