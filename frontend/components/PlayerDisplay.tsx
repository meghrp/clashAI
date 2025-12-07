import { PlayerSnapshot } from '@/types';

interface PlayerDisplayProps {
  player: PlayerSnapshot;
}

export default function PlayerDisplay({ player }: PlayerDisplayProps) {
  return (
    <div className="card">
      <h2>Player Information</h2>
      
      <div className="player-summary">
        <div className="summary-item">
          <div className="summary-label">Name</div>
          <div className="summary-value">{player.name}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">Tag</div>
          <div className="summary-value">{player.tag}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">Town Hall</div>
          <div className="summary-value">Level {player.town_hall_level}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">Trophies</div>
          <div className="summary-value">{player.trophies.toLocaleString()}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">Best Trophies</div>
          <div className="summary-value">{player.best_trophies.toLocaleString()}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">League</div>
          <div className="summary-value">{player.league || 'Unranked'}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">Clan</div>
          <div className="summary-value">{player.clan_name || 'No clan'}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">War Stars</div>
          <div className="summary-value">{player.war_stars}</div>
        </div>
      </div>

      {player.heroes.length > 0 && (
        <div className="table-container">
          <h3>Heroes</h3>
          <table>
            <thead>
              <tr>
                <th>Hero</th>
                <th>Level</th>
                <th>Max Level</th>
                <th>Village</th>
              </tr>
            </thead>
            <tbody>
              {player.heroes.map((hero) => (
                <tr key={hero.name}>
                  <td>{hero.name}</td>
                  <td>{hero.level}</td>
                  <td>{hero.max_level}</td>
                  <td>{hero.village}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {player.troops.length > 0 && (
        <div className="table-container">
          <h3>Troops</h3>
          <table>
            <thead>
              <tr>
                <th>Troop</th>
                <th>Level</th>
                <th>Max Level</th>
                <th>Village</th>
              </tr>
            </thead>
            <tbody>
              {player.troops.slice(0, 20).map((troop) => (
                <tr key={troop.name}>
                  <td>{troop.name}</td>
                  <td>{troop.level}</td>
                  <td>{troop.max_level}</td>
                  <td>{troop.village}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {player.spells.length > 0 && (
        <div className="table-container">
          <h3>Spells</h3>
          <table>
            <thead>
              <tr>
                <th>Spell</th>
                <th>Level</th>
                <th>Max Level</th>
                <th>Village</th>
              </tr>
            </thead>
            <tbody>
              {player.spells.slice(0, 15).map((spell) => (
                <tr key={spell.name}>
                  <td>{spell.name}</td>
                  <td>{spell.level}</td>
                  <td>{spell.max_level}</td>
                  <td>{spell.village}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
