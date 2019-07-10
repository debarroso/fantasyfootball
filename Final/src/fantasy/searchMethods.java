package fantasy;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import javax.sql.DataSource;

import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.simple.SimpleJdbcCall;

/**
 * Only had time to implement one search, but this method executes a stored procedure
 * to find quarterback performances
 * @author debar
 *
 */
public class searchMethods {
	/**
	 * Accepts the parameters submitted from the form
	 * @param ds - datasource
	 * @param pid - player id
	 * @param name - player name
	 * @param low - low range of pts
	 * @param high - high range of pts
	 * @param opp - opponenet
	 * @param gid - game id
	 * @param rookie - was rookie
	 * @param bye - was after bye
	 * @return
	 */
	public static List<QBstat> qbSearch(DataSource ds, String pid, String name, Integer low, 
			Integer high, String opp, String gid, String rookie, String bye) {
		
		//New jdbc call to stored procedure and obj to hold params
		SimpleJdbcCall proc = new SimpleJdbcCall(ds).withProcedureName("search_qbperf");
		MapSqlParameterSource params = new MapSqlParameterSource();
		
		//add values as params
		params.addValue("pid", pid);
		params.addValue("pname", name);
		params.addValue("low", low);
		params.addValue("high", high);
		params.addValue("opp", opp);
		params.addValue("gid", gid);
		params.addValue("rook", rookie);
		params.addValue("bye", bye);
	
		//list to store qbstat object and a map for the result of the procedure execution
		List<QBstat> players = new ArrayList<QBstat>();
		Map<String, Object> result = proc.execute(params);
		
		//thinks the cast is a warning. i disagree
		@SuppressWarnings("unchecked")
		List<Object> plist = (ArrayList<Object>) result.get("#result-set-1");
	
		//iterate over entries
		Iterator<Object> iter = plist.iterator();
		while(iter.hasNext()){
			
			//again, ignoring cast warning
			@SuppressWarnings("unchecked")
			Map<String, Object> p = (Map<String, Object>) iter.next();

			//store map entries in qbstats object
			QBstat player = new QBstat();
			player.setId((String) p.get("player_id"));
			player.setGame((String) p.get("game_id"));
			player.setPts((Integer) p.get("fant_pts"));
			player.setRookie((String) p.get("rookie"));
			player.setTeam((String) p.get("team"));
			player.setAfterBye((String) p.get("after_bye"));
			player.setRushAtt((Integer) p.get("rush_att"));
			player.setRushYards((Integer) p.get("rush_yards"));
			player.setRushTds((Integer) p.get("rush_tds"));
			player.setCompletions((Integer) p.get("completions"));
			player.setPassAtt((Integer) p.get("pass_att"));
			player.setAccuracy((Double) p.get("accuracy"));
			player.setInterceptions((Integer) p.get("interceptions"));
			player.setFumble((Integer) p.get("fumbles"));
			player.setPassYards((Integer) p.get("pass_yards"));
			player.setPassTds((Integer) p.get("pass_tds"));
			player.setSacked((Integer) p.get("sacks"));
			player.setQBR((Double) p.get("qbr"));
		
			//finally add to list
			players.add(player);
		
		}	
		
		//return list
		return players;
	}
}
