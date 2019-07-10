<%@taglib uri = "http://www.springframework.org/tags/form" prefix = "form"%>
<%@taglib uri = "http://www.springframework.org/tags" prefix = "spring" %>

<html>
	<spring:url value="/" var="url" htmlEscape="true"/>
   	<head>
  	  <title>Fantasy User</title>
   	</head>

   	<body>
   	  <div>
        <h2>User Information</h2>
        <h4><font color = "Red">${message}</font></h4>
      </div>
      <div>
      	<form:form method = "POST" action = "${url}failed">
          <table>
            <tr>
              <td><form:label path = "username">Username</form:label></td>
           	  <td><form:input path = "username" /></td>
            </tr>
            <tr>
              <td><form:label path = "password">Password</form:label></td>
              <td><form:password path = "password" /></td>
            </tr>
            <tr>
              <td><form:label path = "experience">Experience</form:label></td>
              <td>
                <form:select path = "experience">
                  <form:option value = "Beginner"/>
                  <form:option value = "Casual"/>
                  <form:option value = "Pro"/>
                  <form:option value = "Guru"/>
                </form:select>
              </td>
            </tr>
            <tr>
              <td colspan = "2">
                <input type = "submit" value = "Submit"/>
              </td>
            </tr>
          </table>  
        </form:form>
      </div>
   </body>
   
</html>