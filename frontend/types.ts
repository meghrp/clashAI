/**
 * Shared types matching backend Pydantic models.
 */

export interface HeroInfo {
  name: string;
  level: number;
  max_level: number;
  village: string;
}

export interface TroopInfo {
  name: string;
  level: number;
  max_level: number;
  village: string;
}

export interface SpellInfo {
  name: string;
  level: number;
  max_level: number;
  village: string;
}

export interface UpgradeState {
  name: string;
  current_level: number;
  max_level: number;
  type: string;
}

export interface PlayerSnapshot {
  tag: string;
  name: string;
  town_hall_level: number;
  exp_level: number;
  trophies: number;
  best_trophies: number;
  war_stars: number;
  attack_wins: number;
  defense_wins: number;
  clan_name: string | null;
  clan_tag: string | null;
  league: string | null;
  heroes: HeroInfo[];
  troops: TroopInfo[];
  spells: SpellInfo[];
  available_upgrades: UpgradeState[];
}

export interface UpgradeAdvice {
  item_name: string;
  priority: number;
  reason: string;
}

export interface AttackStrategyAdvice {
  strategy_name: string;
  description: string;
  recommended_troops: string[];
  recommended_spells: string[];
  difficulty: string;
}

export interface PlayerAdvice {
  upgrade_priorities: UpgradeAdvice[];
  attack_strategies: AttackStrategyAdvice[];
  general_tips: string[];
  war_tips: string[] | null;
}
