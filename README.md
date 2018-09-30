# Quick start Secure Django Project Template

This is free quick start template for a secure Django web application using OAuth2 with server side encrypted tokens. 
This template has all my favorite bits for a good Django web site.  Questions and contributions are welcome.  

This project includes the following features.    

**Secure Oauth2 User Authentication**

This project uses the _django-oauth-toolkit_ to enable Oauth2 user authentication. Oauth tokens are 
encrypted and decrypted at the server. A custom middleware is provided that automates the encrypting, 
decrypting and refreshing of Oauth2 tokens.

Views need only to have the appropriate django security function decorators.  


**REST API w/ Swagger Documentation**

A template for REST API is included with automatic API documentation using Swagger. A separate API
authentication handler is available in proj.api_authentication.py. Rich API viewsets are available in 
proj.api_viewsets.py which can add various features to APIs.

**NGINX Configuration**

A NGINX web server configuration is available using FastCGI and UWSGI.

**Basic User Management**

Basic user management web pages are available to allow creating, editing and deleting system users. This has integration with Oauth2.   

**Authenticated and Non-Authenticated Templates**

All pages source a top level template from the 'templates' directory for pages where the user has authenticated or not.

**Oauth2 Unit Tests**

There are example unit tests to support testing when Oauth2 authentication is used.

**Support for Celery tasks**

This project also has support for Celery tasks, see proj.settings.celery

**Bootstrap 4**

Template web pages are formatted using Bootstrap 4  