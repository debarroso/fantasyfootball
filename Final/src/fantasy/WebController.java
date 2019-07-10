package fantasy;

//import all necessary libraries
import javax.sql.DataSource;
import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.ui.ModelMap;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;


/**
 * This is the WebController class. It is used by the spring MVC framework to
 * route requests to the proper jsp files.
 * 
 * @author debar
 */
@Controller
public class WebController {
	
	//set variables shared across methods
	public ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
	public DataSource datasource = (DataSource) context.getBean("datasource");
	public JdbcTemplate connection = new JdbcTemplate(datasource);
	public User user;
	
	/**
	 * called to create new jdbc connection for this class
	 */
	public void openConnection() {
		this.connection = new JdbcTemplate(datasource);
	}
	
	
	/**
	 * closes the existing jdbc connection in this class
	 */
	public void closeConnection() {
		((ConfigurableApplicationContext) context).close();
	}
	
	/**
	 * This is the first request when we first launch the program
	 * @param model - model passed in as a parameter
	 * @return - returns new model and view routing to login
	 */
	@RequestMapping(value="/", method=RequestMethod.GET)
	public ModelAndView login(ModelMap model) {
		//open the jdbc connection
		openConnection();
	    return new ModelAndView("login", "command", new User("","",""));
	}
	
	/**
	 * Post request when the signin is submitted. Either redirects to homepage
	 * or will rerender the login page with a message of a failed attempt.
	 * @param username - username from form
	 * @param password - password from form
	 * @param model - model to display on the view
	 * @return - returns a new model and view
	 */
	@RequestMapping(value="/signin", method= RequestMethod.POST)
	public ModelAndView addUser(
			@RequestParam("username") String username,
			@RequestParam("password") String password,
			ModelMap model) {
		
		//call signin in method
		user = signinMethods.signin(username, password, connection);
		
		//if we got a user from the signin redirect to homepage
		if (user != null) {
			model.addAttribute("username", user.getUsername());
		    return new ModelAndView("redirect:home", "command", user);
		}
		
		//otherwise try again
		model.addAttribute("message", "User/Password combo not found try again or create a new account.");
		return new ModelAndView("login", "command", new User("","",""));
	}
	
	
	/**
	 * We are routed to this page if the user clicks on a link to create a user
	 * @param model - passed in model to display on view
	 * @param failed - if set to true the user failed to create an account and
	 * 		we display a message to them
	 * @return - new model and view rendering create user page
	 */
	@RequestMapping(value="/createUser", method=RequestMethod.GET)
	public ModelAndView createUser(ModelMap model, boolean failed) {
		//if we set failed login enter this block
		if (failed) {
			//add attribute to display failed message
			model.addAttribute("message", "Username taken or you have blank fields. Try again.");
			return new ModelAndView("userInfo", "command", new User("","",""));
		}
		
		//otherwise this is the first time we landed here. no message
		return new ModelAndView("userInfo", "command", new User("","",""));
	}
	
	
	/**
	 * When we post the userInfo form we route here. will either re-render userInfo page
	 * and pass in failed as a parameter, or redirect to homepage
	 * @param username - username from form
	 * @param password - password from form
	 * @param experience - experience level from form
	 * @param model - model to display on view
	 * @return - new model and view to render
	 */
	@RequestMapping(value="/failed", method=RequestMethod.POST)
	public ModelAndView redirect(
			@RequestParam("username") String username,
			@RequestParam("password") String password,
			@RequestParam("experience") String experience,
			ModelMap model) {
		
		//create a user from the form input
		User user = new User(username, password, experience);
		
		//if username is taken prompt them again and set failed
		if (signinMethods.usernameTaken(user, connection)) {
			return createUser(model, true);
		}
		
		//if any of the input is null then rerender and set failed
		else if (user.getUsername().isEmpty() || user.getPassword().isEmpty())
			return createUser(model, true);
		
		
		//else insert user into users table and redirect to homepage
		else {
			signinMethods.insertUser(user, datasource);			
			return addUser(username, password, model);
		}
	}
	
	
	/**
	 * Renders the homepage for the user
	 * @param username - username is the only request parameter we pass in
	 * @param model - model to display
	 * @return - return new model and view
	 */
	@RequestMapping(value="/home", method= {RequestMethod.GET, RequestMethod.POST})
	public ModelAndView home(ModelMap model) {
		List<Player> players = signinMethods.getWatchlist(user.getWatchlistId(), datasource);
		
		//check if they have any players on their watchlist
		if (players.isEmpty()) {
			model.addAttribute("message", "Watchlist is empty");
		} else {
			for(Player player : players) {
				player.toString();
			}
			model.addAttribute("players", players);
		}
		
		model.addAttribute("username", user.getUsername());
		model.addAttribute("experience", user.getExperience());
		return new ModelAndView("home", "command", user);
	}
	
	
	/**
	 * Handle form when they add player to watchlist
	 * @param id - player id they submitted
	 * @param model
	 * @return
	 */
	@RequestMapping(value="/add", method= RequestMethod.POST)
	public ModelAndView add(@RequestParam("id") String id, ModelMap model) {
		//add player to table in db and return model and view
		watchlistMethods.addPlayer(id, user.getWatchlistId(), datasource);
		model.addAttribute("username", user.getUsername());
		return new ModelAndView("redirect:home", "command", user);
	}
	
	
	/**
	 * Handle form when player is removed from watchlist
	 * @param id - player id
	 * @param model
	 * @return
	 */
	@RequestMapping(value="/remove", method= RequestMethod.POST)
	public ModelAndView remove(@RequestParam("id") String id, ModelMap model) {
		watchlistMethods.removePlayer(id, user.getWatchlistId(), datasource);
		model.addAttribute("username", user.getUsername());
		return new ModelAndView("redirect:home", "command", user);
	}
	
	
	/**
	 * Handles form submission from search function
	 * @param pid - player id
	 * @param name - player name
	 * @param position - position
	 * @param low - low pts range
	 * @param high - high pts range
	 * @param opp - oppenent
	 * @param gid - game id
	 * @param rookie - was rookie
	 * @param bye - after bye
	 * @param model
	 * @return
	 */
	@RequestMapping(value="/searchPerf", method= RequestMethod.POST)
	public ModelAndView search(@RequestParam(name="pid", required=false) String pid,
			@RequestParam(name="pname", required=false) String name,
			@RequestParam(name="position", required=false) String position,
			@RequestParam(name="low", required=false) String low,
			@RequestParam(name="high", required=false) String high,
			@RequestParam(name="opp", required=false) String opp,
			@RequestParam(name="gid", required=false) String gid,
			@RequestParam(name="rookie", required=false) String rookie,
			@RequestParam(name="bye",required=false) String bye,
			ModelMap model) {
		
		//handle null values
		if (pid == null)
			pid = "";
		if (name == null)
			name = "";
		if (position == null)
			position = "";
		if (low == null)
			low = "0";
		if (high == null)
			high = "99";
		if (opp == null)
			opp = "";
		if (gid == null)
			gid = "";
		if (rookie == null)
			rookie = "";
		if (bye == null)
			bye = "";
		
		//handle checkboxes
		if (rookie.equals("on")) {
			rookie = "TRUE";
		} else {
			rookie = "FALSE";
		}		
		if (bye.equals("on")) {
			bye = "TRUE";
		} else {
			bye = "FALSE";
		}
		
		//pass in parameters to search method
		List<QBstat> players = searchMethods.qbSearch(datasource, pid, name, Integer.parseInt(low.replace(",", "")), 
				Integer.parseInt(high.replace(",", "")), opp, gid, rookie, bye);
		
		//if returned list is empty add attribute to display message to user
		if (players.isEmpty()) {
			model.addAttribute("message", "No results returned");
		} else {
			model.addAttribute("message", "Top Performances");
			model.addAttribute("stats", players);
		}
		
		model.addAttribute("username", user.getUsername());
		
		//return results
		return new ModelAndView("qbsearch", "command", user);
	}
	
	/**
	 * When a user clicks on the logout link close the connection and logout
	 * @param model - model to display on view
	 * @return
	 */
	@RequestMapping(value="/logout", method=RequestMethod.GET)
	public String logout(ModelMap model) {
		closeConnection();
		user = null;
		return "logout";
	}
}
