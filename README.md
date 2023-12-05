# django-reactJs
This web application is supposed to solve a challenge. It uses Django Rest Framework for the backend and ReactJs in the frontend. Further information about the challenge can be found following [this link](https://github.com/hiddenfounders/web-coding-challenge/blob/master/README.md).

## Backend: Django/ Django-rest-framework / MongoDB

Tools:
- django 1.9
- django-rest-framework 3.3.1
- django_mongoengine 0.2.1
- python 3.6
- mongoengine 0.15.0
- pymongo 3.6.0
- MongoDB 3.4
    
How it works:

- Install the database management system:
    Go to MongoDB [website](https://www.mongodb.com/try/download/community). Find your development environment, then download MongoDB installer.
    You can choose a specific version of MongoDB by checking the All version binaries link in the page.
    Install your MongoDB database now.
    
- Install python version 3.6, together with [pip](https://pip.pypa.io/en/stable/installation/) and [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html). 
- Clone the repository from my [github](https://github.com/Mehdi6/django-reactjs), and place it in a new folder.
- Install a virtualenv:
    run the command line, place yourself inside the project's folder, then create your new virtualenv.
    Install the requirements by running the following command line: `pip install -r requirements.txt`
- Import data:
    Now we need to create a new database where our application data will live.
    All you need is to run the data_import.py script. Go to the django_backend folder and run the `data_import.py` script. This script will import data from a remote server about shops and transfer them to a new database. Don't forget to run a MongoDB database instance first in your local environment.
    
- Run the server
(1) First run the command : `python manage.py migrate`
(2) Then: `python manage.py runserver`
(3) The server is now running on http://localhost:8000/

## Frontend: React/ Redux / NodeJS

Tools:
- react 
- redux
- react-google-maps
- react-bootstrap
- axios
- webpack
    
How it works:
    
- Install npm: go to https://nodejs.org/en/ and download NodeJs. Then install it in your environment
- Install the modules: open the command line and locate yourself in the react_frontend folder. Then run the next command line `npm install`
- Launch the server: `npm run start` to run the frontend server. 
- The server is now running on http://localhost:8083/

## What do I need to know to test the web application?

While testing the web app features, you will probably need to check emails sent by the backend. All the emails during the development mode are stored in the `tmp` folder (project_folder/django_backend/django_backend/tmp). When you signup, an email will be sent and stored in that folder, you will need to check the link that it contains, and run it in your browser to activate the user account.

## Issue Reporting

If you have found a bug or feature request, please report them at the repository issues section.
    
## License 

MIT

## Acknowledgements

Thanks to the quick starting [project](https://github.com/ZachLiuGIS/reactjs-auth-django-rest) by [@ZachLiuGIS](https://github.com/ZachLiuGIS) that demonstrate very well the combination of DRF with ReactJs to build a web app with user authentication features. 
