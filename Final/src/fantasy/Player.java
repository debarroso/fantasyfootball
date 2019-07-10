package fantasy;

/**
 * Player class: each variable corresponds to a column in
 * the players table
 * @author debar
 *
 */
public class Player {
	private String id;
	private String name;
	private Integer height;
	private Integer weight;
	private String position;

	//setter methods
	public void setId(String id) {
		this.id = id;
	}
	public void setName(String name) {
		this.name = name;
	}
	public void setHeight(Integer height) {
		this.height = height;
	}
	public void setWeight(Integer weight) {
		this.weight = weight;
	}
	public void setPosition(String position) {
		this.position = position;
	}
	   
	//getter methods
	public String getId() {
		return id;
	}
	public String getName() {
		return name;
	}
	public Integer getHeight() {
		return height;
	}
	public Integer getWeight() {
		return weight;
	}
	public String getPosition() {
		return position;
	}		
}