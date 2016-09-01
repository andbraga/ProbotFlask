---To run the web server---

1 - cd into the directory flask_starter

2 - type: source venv/bin/activate

3 - copy and past the cmmands bellow (replace the < ... > fields with your data)

export APP_SETTINGS="config.DevelopmentConfig"

export DATABASE_URL=$PWD

export CONTACT_EMAIL=<email@mail.com>

export LOGGING_URL=localhost:514

export APP_MAIL_USERNAME=<email username>

export APP_MAIL_PASSWORD=<email password>

4 - When executing for the 1st time you may need to use the following commands

python manage.py db init

python manage.py db migrate

python manage.py db upgrade

5 - Run the server with: python manage.py runserver

---To run the socker server---

1 - First you need to install crossbar.io usind the command: pip install crossbar

2- cd into the directory ProBot_Server

2- run the socket server with: crossbar start


