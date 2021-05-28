from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from datetime import datetime
from werkzeug.security import generate_password_hash
import click
from app.config import Config

db = SQLAlchemy()
mail = Mail()

def create_app():
  app = Flask(__name__)

  @app.cli.command('seed')
  @click.argument('args')
  def seed(args):
    if args == 'status':
      status = Status()
      status.create(name='Submitted', color='text-info')
      status.create(name='In Review', color='text-warning')
      status.create(name='Rejected', color='text-danger')
      status.create(name='Accepted', color='text-primary')
      status.create(name='Published', color='text-success')
      print('Status has been seeded')
      return 

    if args == 'role':
      role = Role()
      role.create(name='user')
      role.create(name='admin')
      role.create(name='reviewer')
      print('Role has been seeded')
      return 

    if args == 'admin':
      user = User()
      role = Role()
      user.create(
        name='Rejournal Admin',
        email='adm.rejournal@gmail.com',
        telephone='081239567845',
        password=generate_password_hash(Config.ADMIN_PASSWORD, method='sha256'),
        gender='M',
        is_verified=1,
        role_id=role.query.filter_by(name='admin').first().id
      )
      print('Admin has been seeded')
      return 

  app.config.from_object(Config)

  db.init_app(app)
  migrate = Migrate(app, db)
  mail.init_app(app)

  login_manager = LoginManager()

  login_manager.login_view = 'auth.login'
  login_manager.login_message_category = 'danger'
  login_manager.init_app(app)

  from app.models.user import User
  from app.models.verification import Verification
  from app.models.role import Role
  from app.models.status import Status
  from app.models.topic import Topic
  from app.models.journal import Journal
  from app.models.author import Author
  from app.models.journal_log import JournalLog
  from app.models.reviewer import Reviewer

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  from app.routes.base import base
  app.register_blueprint(base, url_prefix='/')

  from app.routes.auth import auth
  app.register_blueprint(auth, url_prefix='/auth')

  from app.routes.home import home
  app.register_blueprint(home, url_prefix='/home')

  from app.routes.admin import admin
  app.register_blueprint(admin, url_prefix='/admin')
  
  from app.routes.reviewer import reviewer
  app.register_blueprint(reviewer, url_prefix='/reviewer')

  from app.routes.error import error
  app.register_blueprint(error, url_prefix='/error')

  return app
