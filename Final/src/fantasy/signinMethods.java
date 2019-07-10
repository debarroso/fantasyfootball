package fantasy;


import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import javax.sql.DataSource;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.simple.SimpleJdbcCall;


/**
 * Class which contains all of the signin methods to verify user input
 * @author debar
 */
public class signinMethods {	
	/**
	 * Signs in for the user
	 * @param username
	 * @param password
	 * @param connection
	 * @return returns a user object
	 */
	public static User signin(String username, String password, JdbcTemplate connection) {
		String SQL = "SELECT * FROM users WHERE username = ? AND password = ?";
		
		try {
			User user = connection.queryForObject(SQL,
				new Object[] {username, password},
				new UserMapper());
			
			return user;
		//if we couldn't find a user return null
		} catch (EmptyResultDataAccessException e) {
			return null;
		}   
	}
	
	/**
	 * Checks to see if a username is taken when creating a user
	 * @param user
	 * @param connection
	 * @return
	 */
	public static boolean usernameTaken(User user, JdbcTemplate connection) {
		String username = user.getUsername();
		
		String SQL = "SELECT * FROM users WHERE username = ?";
		try {
			user = connection.queryForObject(SQL,
				new Object[] {username},
				new UserMapper());
				return true;
		} catch (EmptyResultDataAccessException e) {
			return false;
		}
	}
	
	/**
	 * Inserts a user into the DB. Should probably add exception handling :/
	 * @param user
	 * @param ds
	 */
	public static void insertUser(User user, DataSource ds) {
		//jdbc call and params obj
		SimpleJdbcCall proc = new SimpleJdbcCall(ds).withProcedureName("create_user");
		MapSqlParameterSource params = new MapSqlParameterSource();
		
		//map params
		params.addValue("uname", user.getUsername());
		params.addValue("pwd", user.getPassword());
		params.addValue("exp", user.getExperience());
		
		proc.execute(params);
	}
	
	/**
	 * retrieves a users watchlist from the DB
	 * @param i
	 * @param ds
	 * @return
	 */
	public static List<Player> getWatchlist(Integer i, DataSource ds){
		//jdbc call and params obj
		SimpleJdbcCall proc = new SimpleJdbcCall(ds).withProcedureName("get_watchlist_players");
		MapSqlParameterSource params = new MapSqlParameterSource();
		
		params.addValue("wlid", i);
		
		//list to store players (same as search methods, should be broken into its own class/method)
		List<Player> players = new ArrayList<Player>();
		Map<String, Object> result = proc.execute(params);
		
		@SuppressWarnings("unchecked")
		List<Object> plist = (ArrayList<Object>) result.get("#result-set-1");
		
		Iterator<Object> iter = plist.iterator();
		while(iter.hasNext())
		{
			@SuppressWarnings("unchecked")
			Map<String, Object> p = (Map<String, Object>) iter.next();

			Player player = new Player();
			player.setId((String) p.get("player_id"));
			player.setName((String) p.get("name"));
			player.setHeight((Integer) p.get("height"));
			player.setWeight((Integer) p.get("weight"));
			player.setPosition((String) p.get("position"));
			
			players.add(player);
		}
		
		return players;
	}
}
