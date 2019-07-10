package fantasy;

import java.sql.ResultSet;
import java.sql.SQLException;
import org.springframework.jdbc.core.RowMapper;

/**
 * Maps rows to a user object
 * @author debar
 *
 */
public class UserMapper implements RowMapper<User>{
	public User mapRow(ResultSet rs, int rowNum) throws SQLException {
		User user = new User(rs.getString("username"),
				rs.getString("password"),
				rs.getString("experience_level"));
		
		//set the watchlist id here
		user.setWatchlist(rs.getInt("watchlist_id"));
		return user;
	}
}
