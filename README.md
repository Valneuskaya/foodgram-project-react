# The Foodgram website
![greetings!](https://github.com/Valneuskaya/
foodgram-project-react/actions/workflows/main.yml/badge.svg)

This service allows users to post recipes, subscribe to other users' publications, add their favourite recipes to their Favourites list, and download a list of the products needed to prepare the selected dishes.

## Steck tech
- Python (using Django REST Framework);
- library Djoser (authentication by tockens);
- library django-filter (request filters);
- PostgreSQL database;
- Docker
- git (version control).

# Screenshots of the project
<img src="https://github.com/Valneuskaya/foodgram-project-react/blob/master/images/main.png" width="600">
<img src="https://github.com/Valneuskaya/foodgram-project-react/blob/master/images/recipe%20create.png" width="600">
<img src="https://github.com/Valneuskaya/foodgram-project-react/blob/master/images/signup.png" width="600">
<img src="https://github.com/Valneuskaya/foodgram-project-react/blob/master/images/subscriptions.png" width="600">

## The project in the internet (disabled)
- The project is available at [http://84.201.162.109/]
- Documentation for writing api project available at [http://84.201.162.109/api/docs/redoc.html]

## Project start
* Clone the repo
* Build infra Docker containers (backend, frontend, db, nginx)
* Run Docker containers
* Create database
* Re-run containers
* Open App URL

## Workflow

* add environment variables to Secrets GitHub to work with:
 ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<database name postgres>
    DB_USER=<db-user>
    DB_PASSWORD=<password>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<dockerHub password>
    DOCKER_USERNAME=<user name on DockerHub>
    
    SECRET_KEY=<django project secret key>

    USER=<username for connecting to the server>
    HOST=<IP server>
    SSH_KEY=<your SSH key (cat/.ssh/id_rsa to get it)>
    PASSPHRASE=<if you used a passphrase when creating your ssh key>

    TELEGRAM_TO=<ID of chat you wish to send a message to, ask bot @userinfobot for your ID>
    TELEGRAM_TOKEN=<token of your bot, get this token from bot @BotFather>
```
Workflow consists of the following steps:
- Checking the code for PEP8 compliance and executing the tests implemented in the project;
- Building and publishing the application image on DockerHub;
- Automatically downloading the application image and deplaying it to the remote server;
- Sending notifications to users via telegram-chat.  


## Author
Backend by Valeri Neuskaya [https://github.com/Valneuskaya]

Frontend by yandex-praktikum [https://github.com/yandex-praktikum]
