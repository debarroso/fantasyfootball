<%@page contentType = "text/html;charset = UTF-8" language = "java" %>
<%@page isELIgnored = "false" %>
<%@taglib uri = "http://www.springframework.org/tags/form" prefix = "form"%>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<html>
  <title>Fantasy Football DB</title>
  <body>
	  <table border = "1">
	  	<thead>${message}<br></thead>
		  <tr>
			<th>Player ID</th>
			<th>Position</th>
			<th>Game ID</th>
			<th>Points Scored</th>
			<th>Team</th>
			<th>Rookie</th>
			<th>After Bye</th>
			<th>Rush Att</th>
			<th>Rush Yards</th>
			<th>Rush TDs</th>
			<th>Pass Attempt</th>
			<th>Pass Completions</th>
			<th>Pass Yards</th>
			<th>Pass TDs</th>
			<th>QBR</th>
			<th>Accuracy</th>
			<th>Interceptions</th>
		  </tr>
		  <c:forEach items="${stats}" var="tmp">
            <tr>
            <td>${tmp.getId()}</td>
            <td>QB</td>
            <td>${tmp.getGame()}</td>
			<td>${tmp.getPts()}</td>
			<td>${tmp.getTeam()}</td>
			<td>${tmp.getRookie()}</td>
			<td>${tmp.getAfterBye()}</td>
			<td>${tmp.getRushes()}</td>
			<td>${tmp.getRushYards()}</td>
			<td>${tmp.getRushTds()}</td>
			<td>${tmp.getPassAtt()}</td>
			<td>${tmp.getCompletions()}</td>
			<td>${tmp.getPassYards()}</td>
			<td>${tmp.getPassTds()}</td>
			<td>${tmp.getQBR()}</td>	
			<td>${tmp.getAccuracy()}</td>
			<td>${tmp.getInterceptions()}</td>
          </tr>
          </c:forEach>
       </table>
       <a href="${url}home">Back to home.</a>
  </body>
</html>