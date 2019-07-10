package fantasy;

import java.sql.ResultSet;
import java.sql.SQLException;
import org.springframework.jdbc.core.RowMapper;

/**
 * Maps a row in a result set to a player object
 * @author debar
 */
public class PlayerMapper implements RowMapper<Player> {
	
	/**
	 * Maps a result set from the players table
	 * @return - returns a player object
	 */
	public Player mapRow(ResultSet rs, int rowNum) throws SQLException {
		Player player = new Player();
		player.setId(rs.getString("player_id"));
		player.setName(rs.getString("name"));
		player.setHeight(rs.getInt("height"));
		player.setWeight(rs.getInt("weight"));
		player.setPosition(rs.getString("position"));
      
		return player;
	}
}