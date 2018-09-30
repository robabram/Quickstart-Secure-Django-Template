# Quick start Secure Django Project Template

This is free quick start template for a secure Django web application using OAuth2 with server side encrypted tokens. 
This template has all my favorite bits for a good Django web site.  Questions and contributions are welcome.  

This project includes the following features.    

**Secure Oauth2 User Authentication**

This project uses the _django-oauth-toolkit_ to enable Oauth2 user authentication. Oauth tokens are 
encrypted and decrypted at the server. A custom middleware is provided that automates the encrypting, 
decrypting and refreshing of Oauth2 tokens.


**REST API w/ Swagger Documentation**

A template for REST API is included with automatic API documentation using Swagger. A separate API
authentication handler is available in proj.api_authentication.py. Rich API viewsets are available in 
proj.api_viewsets.py which can add various features to APIs.

**NGINX Configuration**

Configurations are available for NGINX using FastCGI and UWSGI.

**Basic User Management**

Basic user management web pages are available to allow creating, editing and deleting system users. This has integration with Oauth2.   

 