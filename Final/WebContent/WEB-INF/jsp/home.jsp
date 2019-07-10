<%@page contentType = "text/html;charset = UTF-8" language = "java" %>
<%@page isELIgnored = "false" %>
<%@taglib uri = "http://www.springframework.org/tags/form" prefix = "form"%>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<html>
  <title>Fantasy Football DB</title>
  <body>
	<div>
	  <table>
	  	<tr>
		<td>
		  <h4>Hello ${username}!</h4>
			<p>You are currently ${experience}<br>
			<a href="${url}logout">Logout here.</a>
			</p>
		</td>
		<td>
		  <table border="1">
			<thead><b>Watchlist</b><br></thead>
			  <thead>${message}</thead>
			  <tr>
			    <th>Player ID</th>
			    <th>Player Name</th>
			    <th>Position</th>
			    <th>Height</th>
			    <th>Weight</th>
			  </tr>
			  <c:forEach items="${players}" var="tmp">
                <tr>
                  <td>${tmp.getId()}</td>
                  <td>${tmp.getName()}</td>
                  <td>${tmp.getPosition()}</td>
                  <td>${tmp.getHeight()}</td>
                  <td>${tmp.getWeight()}</td>  			
                </tr>
              </c:forEach>
			  <tr>
		  </table>
		</td>
		</tr>
	  </table>
	    <form:form action = "${url}add" method = "POST">
		  <table>
		    <tr>
		      <td><label name = "id">Add:</label></td>
		      <td><input type="text" name="id"/></td>
              <td><input type = "submit" value = "Submit"></td>
    	    </tr>
    	  </table>
    	</form:form>
    	<form:form action = "${url}remove" method = "POST">
		  <table>
		    <tr>
		      <td><label name = "id">Remove:</label></td>
           	  <td><input type="text" name="id"/></td>
              <td><input type = "submit" value = "Submit"/></td>
    	    </tr>
    	  </table>
    	</form:form>
	</div>
	<div>
	<h4>Search Top Performances</h4>
		<form:form action = "${url}searchPerf" method = "POST">
		  <table>
		    <tr>
		      <td><label name = "pid">Player ID:</label><input type = "text" name = "pid"/></td>
		      <td><label name = "pname">Player Name:</label><input type = "text" name = "pname"/></td>
		      <td>
		        <select name = "position">
		      	<option value = "QB">QB</option>
		      	<option value = "NonQB">NonQB</option>
		      	</select>
		      </td>
		      <td><label name = "low">Low Range:</label><input type = "text" name = "low" value = "0"/></td>
		      <td><label name = "high">High Range:</label><input type = "text" name = "high" value = "99"/></td>
    	    </tr>
    	    <tr>
		      <td><label name = "opp">Opponent:</label><input type = "text" name = "opp"/></td>
    	      <td><label name = "gid">GameID:</label><input type = "text" name = "gid"/></td>
		      <td><label name = "rookie">Was Rookie:</label><input type = "checkbox" name = "rookie"/></td>
		      <td><label name = "bye">Was After Bye:</label><input type = "checkbox" name = "bye"/></td>
              <td><input type = "submit" value = "Submit"></td>
            </tr>
    	  </table>
    	</form:form>
	</div>
  </body>
</html>