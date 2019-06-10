# This is my final project for CS50 course.
[![Open Source Society University - Computer Science](https://img.shields.io/badge/OSSU-computer--science-blue.svg)](https://github.com/open-source-society/computer-science)

I tried to solve a real world problem that fits into the scope of a CS50 course.
Flask based app that allows you to order a pizza and sends order information to Trello board.
From the board, staff can further process and deliver orders to customers.

https://restaurant-cs50.herokuapp.com

## Getting Started
```
sudo pip install virtualenv
git clone https://github.com/SkimFelBon/restaurant-cs50
sudo pip install -r requirements.txt
```
### To run locally:
install PostgreSQL
OR
use sqlite3 for simplicity
database included "HomePizzanew.db"

Import enviromental variables:
```
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/{DATABASE-NAME}?client_encoding=utf8"
```
make sure to append "?client_encoding=utf8" to your DATABASE URL


to start development server:
```
FLASK_APP=app.py flask run
```
OR
```
export FLASK_APP=app.py
```
and in terminal type
```
flask run
```
#### Prerequisites for PostgreSQL
Link for a great explanation of how to run PostgreSQL with flask and Heroku
at the end of the readme.

install PostgreSQL
```
sudo apt-get install postgresql postgresql-contrib
```
Start the PostgreSQL service
```
sudo service postgresql start
```
create a superuser for PostgreSQL
```
sudo -u postgres createuser --superuser name_of_user
```
create a database
```
sudo -u name_of_user createdb name_of_database
```
You can access created database with created user by,
```
psql -U name_of_user -d name_of_database
```
to migrate we need this 3 packages
(already included in requirements.txt)
```
pip install flask_script
pip install flask_migrate
pip install psycopg2-binary
```
First, run this code to create a folder named migrations
```
python manage.py db init
```
to migrate with this files use
```
python manage.py db migrate
```
lastly apply the migrations to the database using
```
python manage.py db upgrade
```

Great explanation how to install psql, and how to build app with flask+psql+heroku...

https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc

## MIT License

> Copyright (c) 2019 Leonid Kozak

> Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
