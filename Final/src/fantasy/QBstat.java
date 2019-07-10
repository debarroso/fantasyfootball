package fantasy;

/**
 * Each variable represents a column in the qb performances table
 * @author debar
 *
 */
public class QBstat {
	
	//variables (columns)
	private String id;
	private String game_id;
	private Integer pts;
	private Boolean rookie;
	private String team;
	private Boolean after_bye;
	private Integer rush_att;
	private Integer rush_yards;
	private Integer rush_tds;
	private Integer completions;
	private Integer pass_att;
	private Double accuracy;
	private Integer interceptions;
	private Integer fumble;
	private Integer pass_yards;
	private Integer pass_tds;
	private Integer sacked;
	private Double qbr;
	
	
	//setter methods
	public void setId(String id) {
		this.id = id;
	}
	public void setGame(String game_id) {
		this.game_id = game_id;
	}
	public void setPts(Integer pts) {
		this.pts = pts;
	}
	public void setRookie(String isRookie) {
		if (isRookie.equals("TRUE")) {
			this.rookie = true;
		} else {
			this.rookie = false;
		}
	}
	public void setTeam(String team) {
		this.team = team;
	}
	public void setAfterBye(String afterBye) {
		if (afterBye.equals("TRUE")) {
			this.after_bye = true;
		} else {
			this.after_bye = false;
		}
	}
	public void setRushAtt(Integer rushes) {
		this.rush_att = rushes;
	}
	public void setRushYards(Integer rush_yards) {
		this.rush_yards = rush_yards;
	}
	public void setRushTds(Integer rush_tds) {
		this.rush_tds = rush_tds;
	}
	public void setCompletions(Integer completions) {
		this.completions = completions;
	}
	public void setPassAtt(Integer pass_att) {
		this.pass_att = pass_att;
	}
	public void setAccuracy(Double accuracy) {
		this.accuracy = accuracy;
	}
	public void setInterceptions(Integer interceptions) {
		this.interceptions =interceptions;
	}
	public void setFumble(Integer fumbles) {
		this.fumble = fumbles;
	}
	public void setPassYards(Integer pass_yards) {
		this.pass_yards = pass_yards;
	}
	public void setPassTds(Integer pass_tds) {
		this.pass_tds = pass_tds;
	}
	public void setSacked(Integer sacks) {
		this.sacked = sacks;
	}
	public void setQBR(Double qbr) {
		this.qbr = qbr;
	}
	
	
	//getter methods
	public String getId() {
		return id;
	}
	public String getGame() {
		return game_id;
	}
	public Integer getPts() {
		return pts;
	}
	public Boolean getRookie() {
		return rookie;
	}
	public String getTeam() {
		return team;
	}
	public Boolean getAfterBye() {
		return after_bye;
	}
	public Integer getRushes() {
		return rush_att;
	}
	public Integer getRushYards() {
		return rush_yards;
	}
	public Integer getRushTds() {
		return rush_tds;
	}
	public Integer getCompletions() {
		return completions;
	}
	public Integer getPassAtt() {
		return pass_att;
	}
	public Double getAccuracy() {
		return accuracy;
	}
	public Integer getInterceptions() {
		return interceptions;
	}
	public Integer getFumble() {
		return fumble;
	}
	public Integer getPassYards() {
		return pass_yards;
	}
	public Integer getPassTds() {
		return pass_tds;
	}
	public Integer getSacks() {
		return sacked;
	}
	public Double getQBR() {
		return qbr;
	}
}