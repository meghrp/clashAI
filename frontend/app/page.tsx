'use client';

import { useState } from 'react';
import { fetchPlayer, fetchAdvice } from '@/lib/api';
import { PlayerSnapshot, PlayerAdvice } from '@/types';
import PlayerDisplay from '@/components/PlayerDisplay';
import AdviceDisplay from '@/components/AdviceDisplay';

export default function Home() {
  const [playerTag, setPlayerTag] = useState('');
  const [player, setPlayer] = useState<PlayerSnapshot | null>(null);
  const [advice, setAdvice] = useState<PlayerAdvice | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingAdvice, setLoadingAdvice] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [warFocus, setWarFocus] = useState(false);

  const handleFetchPlayer = async () => {
    if (!playerTag.trim()) {
      setError('Please enter a player tag');
      return;
    }

    setLoading(true);
    setError(null);
    setPlayer(null);
    setAdvice(null);

    try {
      const playerData = await fetchPlayer(playerTag.trim());
      setPlayer(playerData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch player data');
    } finally {
      setLoading(false);
    }
  };

  const handleGetAdvice = async () => {
    if (!playerTag.trim()) {
      setError('Please enter a player tag');
      return;
    }

    setLoadingAdvice(true);
    setError(null);

    try {
      const adviceData = await fetchAdvice(playerTag.trim(), warFocus);
      setAdvice(adviceData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate advice');
    } finally {
      setLoadingAdvice(false);
    }
  };

  return (
    <div className="container">
      <h1>ClashAI</h1>
      
      <div className="card">
        <div className="form-group">
          <label htmlFor="player-tag">Player Tag</label>
          <input
            id="player-tag"
            type="text"
            value={playerTag}
            onChange={(e) => setPlayerTag(e.target.value)}
            placeholder="#YOURTAG"
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                handleFetchPlayer();
              }
            }}
          />
        </div>

        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={warFocus}
              onChange={(e) => setWarFocus(e.target.checked)}
              style={{ marginRight: '0.5rem' }}
            />
            Focus on war strategies
          </label>
        </div>

        <div>
          <button onClick={handleFetchPlayer} disabled={loading}>
            {loading ? 'Loading...' : 'Fetch Player Data'}
          </button>
          <button onClick={handleGetAdvice} disabled={loadingAdvice || !player}>
            {loadingAdvice ? 'Generating Advice...' : 'Get AI Advice'}
          </button>
        </div>

        {error && <div className="error">{error}</div>}
      </div>

      {player && <PlayerDisplay player={player} />}
      {advice && <AdviceDisplay advice={advice} />}
    </div>
  );
}
