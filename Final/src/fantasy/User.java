package fantasy;

public class User {
	
	//object attributes
	private String username;
	private String password;
	private String experience;
	private Integer watchlist;
	
	//constructor
	public User(String username, String password, String experience) {
		this.username = username;
		this.password = password;
		this.experience = experience;
	}

	
	//setter methods
	public void setUsername(String username) {
		this.username = username;
	}
	public void setPassword(String password) {
		this.password = password;
	}
	public void setExperience(String experience) {
		this.experience = experience;
	}
	public void setWatchlist(Integer watchlist) {
		this.watchlist = watchlist;
	}
	
	//getter methods
	public String getUsername() {
		return this.username;
	}
	public String getPassword() {
		return this.password;
	}
	public String getExperience() {
		return this.experience;
	}
	public int getWatchlistId() {
		return this.watchlist;
	}
}
