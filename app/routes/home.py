from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.middlewares.role_checker import RoleChecker
from app.controllers.topic import TopicController
from app.controllers.journal import JournalController


home = Blueprint('home', __name__, template_folder='templates')

role_checker = RoleChecker()
topic_controller = TopicController()
journal_controller = JournalController()

@home.route('/', methods=['GET'])
@login_required
@role_checker.check_permission(role='user')
def index():
  return render_template('pages/user/index.html', role='User')


@home.route('/journal/create', methods=['GET', 'POST'])
@login_required
@role_checker.check_permission(role='user')
def journal_create():
  if request.method == 'POST':
    return journal_controller.create(request=request.form, doc=request.files['doc'])
  
  topics = topic_controller.fetch_all()
  return render_template('pages/user/journal/add.html', role='User', topics=topics)
  