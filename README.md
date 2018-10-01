# Quick Start Secure Django Project Template

This is free quick start template for a secure Django web application using OAuth2 with server side encrypted tokens. 
This template has all my favorite bits for a good secure Django web site.  Questions and contributions are welcome.  

### Quick Feature List

*Note: Features are explained in more detail below* 

* Oauth2 authentication with server side encrypting/decrypting/refreshing of tokens.
* REST API with auto documenation using Swagger.
* NGINX configuration using FastCGI and UWSGI.
* Oauth2 unit test templates.
* Celery configuration.
* Bootstrap 4.

### Quick Start

*Note: Please use Python 3.x for these instructions*

##### Run Quick Start Script

1. `source <(curl -s https://raw.githubusercontent.com/robabram/Quickstart-Secure-Django-Template/master/launch_app.sh)`

##### Manual Quick Start Steps

1. Clone project to local directory.

2. Change directory to git project root directory (Quickstart-Secure-Django-Template).

3. Create a new Virtual Environment: `python3 -m venv venv`

3. Activate VE: `source ./venv/bin/activate`

4. Update PIP to latest: `pip install --update pip`

5. Install required packages: `pip install -r requirements.txt` 

6. Set PYTHONPATH var: ``export PYTHONPATH=`pwd` ``

7. Set DJANGO_SETTINGS_MODULE var: ``export DJANGO_SETTINGS_MODULE="proj.settings.local"`` 

8. Change directory to Django project: `cd django_project`

9. Run django migrate: `python3 manage.py migrate`

10. Run admin command to setup Oauth: `python manage.py admin --init-oauth`

11. Run Django server: `python3 manage.py runserver`

### Features    

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

A NGINX web server configuration is available using FastCGI and UWSGI. SSL configuration will get an 'A+' on Qualys SSL test. 

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
