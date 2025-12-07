import { PlayerAdvice } from '@/types';

interface AdviceDisplayProps {
  advice: PlayerAdvice;
}

export default function AdviceDisplay({ advice }: AdviceDisplayProps) {
  return (
    <div className="card">
      <h2>AI Advice</h2>

      {advice.upgrade_priorities.length > 0 && (
        <div className="advice-section">
          <h3>Upgrades to Prioritize</h3>
          {advice.upgrade_priorities.map((item, index) => (
            <div key={index} className="advice-item">
              <span className="priority-badge">Priority {item.priority}</span>
              <strong>{item.item_name}</strong>
              <p style={{ marginTop: '0.5rem', color: '#666' }}>{item.reason}</p>
            </div>
          ))}
        </div>
      )}

      {advice.attack_strategies.length > 0 && (
        <div className="advice-section">
          <h3>Suggested Attack Strategies</h3>
          {advice.attack_strategies.map((strategy, index) => (
            <div key={index} className="advice-item">
              <h4 style={{ marginBottom: '0.5rem' }}>
                {strategy.strategy_name}
                <span
                  className={`difficulty-badge difficulty-${strategy.difficulty}`}
                >
                  {strategy.difficulty}
                </span>
              </h4>
              <p style={{ marginBottom: '0.5rem', color: '#666' }}>
                {strategy.description}
              </p>
              {strategy.recommended_troops.length > 0 && (
                <p style={{ marginBottom: '0.25rem' }}>
                  <strong>Troops:</strong>{' '}
                  {strategy.recommended_troops.join(', ')}
                </p>
              )}
              {strategy.recommended_spells.length > 0 && (
                <p>
                  <strong>Spells:</strong>{' '}
                  {strategy.recommended_spells.join(', ')}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {advice.general_tips.length > 0 && (
        <div className="advice-section">
          <h3>General Tips</h3>
          <ul className="tip-list">
            {advice.general_tips.map((tip, index) => (
              <li key={index}>{tip}</li>
            ))}
          </ul>
        </div>
      )}

      {advice.war_tips && advice.war_tips.length > 0 && (
        <div className="advice-section">
          <h3>War-Specific Tips</h3>
          <ul className="tip-list">
            {advice.war_tips.map((tip, index) => (
              <li key={index}>{tip}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
