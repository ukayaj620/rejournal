# Rejournal
Research Journal Website. Clone it as you like it!

To run this website on your local PC, you need to have Python runtime and a virtual environment. Here is the step to get started:
1. Clone this project and download it into your local PC.
2. Create a virtual environment.
3. Activate the virtual environment.
4. Install all packages specified in ```requirements.txt``` using command ```pip install -r requirements.txt```.
5. Set FLASK_APP variable pointing to ```app.py``` as the main by using command ```set FLASK_APP=app.py```.
6. Generate migration file by typing in the command below: 
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```
   NB: The database dialect is MySQL
7. Seed the table by typing in the command below:
   ```
   flask seed status
   flask seed role
   flask seed topic
   flask seed admin
   ```
8. If you want to run this website in development mode, please set the value FLASK_ENV variable using command ```set FLASK_ENV=development```.
9. Run your website using command ```flask run```.

This website is created using amazing packages such as:
- [Flask](https://github.com/pallets/flask)
- [Flask-MySQLAlchemy](https://github.com/pallets/flask-sqlalchemy)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [Flask-Login](https://github.com/maxcountryman/flask-login)
- [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate)
- [Flask-Mail](https://github.com/mattupstate/flask-mail)

For the front-end side, this website is created using Bootstrap CSS Framework.

To be honest this website still premature and needs lots of development. I'll keep developing it if there is time for me to develop it.
Thank you.
