# The Foodgram website
This service allows users to post recipes, subscribe to other users' publications, add their favourite recipes to their Favourites list, and download a list of the products needed to prepare the selected dishes.

## Steck tech
- Python (using Django REST Framework);
- library Djoser (authentication by tockens);
- library django-filter (request filters);
- PostgreSQL database;
- git (version control).

## The project in the internet:
- The project is up and available at [*]

- Admin available at [*]

- Documentation for writing api project available at [*]

## Project start
* Clone the repo for your local computer.

### To work with remote server (Ubuntu):
* Log onto your remote server.
* Install docker on the server.
sudo apt install docker.io 
* Install docker-compose on the server.
* Locally edit the file infra/nginx/default.conf.conf, write your IP in the server_name line.
* Copy the docker-compose.yml and nginx.conf files from the infra folder to the server.
```
scp infra/docker-compose.yml <username>@<ip host>:/home/<username>/docker-compose.yml
scp infra/nginx.conf <username>@<ip host>:/home/<username>/nginx.conf
```
* Copy the docs folder to the server:

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
* Workflow consists of the following steps:
- Checking the code for PEP8 compliance and executing the tests implemented in the project;
- Building and publishing the application image on DockerHub;
- Automatically downloading the application image and deplaying it to the remote server;
- Sending notifications to users via telegram-chat.  


## Author
Valeri Neuskaya
