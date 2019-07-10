package fantasy;

import java.sql.ResultSet;
import java.sql.SQLException;
import org.springframework.jdbc.core.RowMapper;

/**
 * Maps a row in a result set to a QBstat object
 * @author debar
 */
public class QBStatMapper implements RowMapper<QBstat> {
	public QBstat mapRow(ResultSet rs, int rowNum) throws SQLException {
		QBstat player = new QBstat();	
		player.setId(rs.getString("player_id"));
		player.setGame(rs.getString("game_id"));
		player.setPts(Integer.parseInt(rs.getString("fant_pts")));
		player.setRookie(rs.getString("rookie"));
		player.setTeam(rs.getString("team"));
		player.setAfterBye(rs.getString("after_bye"));
		player.setRushAtt(Integer.parseInt(rs.getString("rush_att")));
		player.setRushYards(Integer.parseInt(rs.getString("rush_yards")));
		player.setRushTds(Integer.parseInt(rs.getString("rush_tds")));
		player.setCompletions(Integer.parseInt(rs.getString("completions")));
		player.setPassAtt(Integer.parseInt(rs.getString("pass_att")));
		player.setAccuracy(Double.parseDouble(rs.getString("accuracy")));
		player.setInterceptions(Integer.parseInt(rs.getString("interceptions")));
		player.setFumble(Integer.parseInt(rs.getString("fumbles")));
		player.setPassYards(Integer.parseInt(rs.getString("pass_yards")));
		player.setPassTds(Integer.parseInt(rs.getString("pass_tds")));
		player.setSacked(Integer.parseInt(rs.getString("sacks")));
		player.setQBR(Double.parseDouble(rs.getString("qbr")));
      
		return player;
	}
}