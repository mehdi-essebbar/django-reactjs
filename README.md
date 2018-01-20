# django-reactJs
This web application is supposed to solve a challenge. It uses Django Rest Framework for the backend and ReactJs in the frontend. Further information about the challenge can be found following this link: https://github.com/hiddenfounders/web-coding-challenge/blob/master/README.md

## Backend: Django/ Django-rest-framework / MongoDB

Tools:
    - django 1.9
    - django-rest-framework 3.3.1
    - python 3.6
    - mongoengine 0.15.0
    - pymongo 3.6.0
    
    -MongoDB 3.4
    
How it works:
    
    - install the database:
        Go to MongoDB website (https://www.mongodb.com/download-center#community). Find your developpement environement, then download MongoDB installer.
        You can choose a specific version of MongoDB by checking the All version binaries link in the page.
        Install your MongoDB database now.
        
    - install python version 3.6, together with pip and virtualenv.
    - clone the repository from my github https://github.com/Mehdi6/django-reactjs, and place it in a new folder.
    - install a virtualenv:
        run the command line, place yourself inside the folder of the project then create activate your new virtualenv.
        install the requirements by runing the following command: `pip install -r requirements.txt`
    - import data
        Now we need to create a new database where our application data will live.
        All you need is to run the data_import.py script. Go to the django_backend folder and run the data_import script. This script will import dump data from a remote server about shops and transfer them to a new database.
        
    - run the server
        first run the command : `python manage.py migrate`
        then: `python manage.py runserver`
    
## Frontend: React/ Redux / NodeJS

Tools:
    - react 
    - redux
    - react-google-maps
    - react-bootstrap
    - axios
    - webpack
    
How it works:
    
    - install npm: go to https://nodejs.org/en/ and download NodeJs. Then install it in your environment
    - install the modules: open the command line and locate yourself in the react_frontend folder. Then run the next command line `npm install`
    - launch the server: `npm run start` to run the frontend server. 
    
## Issue Reporting

If you have found a bug or feature request, please report them at the repository issues section.
    
## License 

MIT
