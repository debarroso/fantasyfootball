<%@page contentType = "text/html;charset = UTF-8" language = "java" %>
<%@page isELIgnored = "false" %>
<%@taglib uri = "http://www.springframework.org/tags/form" prefix = "form"%>
<%@taglib uri = "http://www.springframework.org/tags" prefix = "spring" %>
<html>
  <spring:url value="/" var="url" htmlEscape="true"/>
  <head>
     <title>Logout: Fantasy Football DB</title>
  </head>

  <body>
    <h2>You have logged out.</h2>
    <a href="${url}">Click here to sign in.</a>
  </body>
   
</html>