/**
 * API client for communicating with the FastAPI backend.
 */
import { PlayerSnapshot, PlayerAdvice } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchPlayer(tag: string): Promise<PlayerSnapshot> {
  const response = await fetch(`${API_URL}/api/player/${encodeURIComponent(tag)}`);
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  
  return response.json();
}

export async function fetchAdvice(
  tag: string,
  warFocus: boolean = false
): Promise<PlayerAdvice> {
  const response = await fetch(`${API_URL}/api/advice`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      tag,
      war_focus: warFocus,
    }),
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  
  return response.json();
}
