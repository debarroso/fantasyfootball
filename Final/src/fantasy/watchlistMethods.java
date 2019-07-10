package fantasy;

import javax.sql.DataSource;

import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.simple.SimpleJdbcCall;

/**
 * Methods to add/remove players from watchlist
 * @author debar
 *
 */
public class watchlistMethods {
	/**
	 * Remove a player
	 * @param player - player id
	 * @param i - watchlist id
	 * @param ds - datasource
	 */
	public static void removePlayer(String player, Integer i, DataSource ds) {
		//jdbc call and params obj
		SimpleJdbcCall proc = new SimpleJdbcCall(ds).withProcedureName("remove_from_watchlist");
		MapSqlParameterSource params = new MapSqlParameterSource();
		
		//map params
		params.addValue("wl_id", i);
		params.addValue("pid", player);
		
		proc.execute(params);
	}

	/**
	 * Adds a player to the watchlist
	 * @param player - player id
	 * @param i -watchlist id
	 * @param ds - datasource
	 */
	public static void addPlayer(String player, Integer i, DataSource ds) {
		//jdbc call and params obj
		SimpleJdbcCall proc = new SimpleJdbcCall(ds).withProcedureName("add_to_watchlist");
		MapSqlParameterSource params = new MapSqlParameterSource();
		
		//map params
		params.addValue("wl_id", i);
		params.addValue("pid", player);
		
		proc.execute(params);
	}
}
