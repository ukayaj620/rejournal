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


@home.route('/journal/', methods=['GET'])
@login_required
@role_checker.check_permission(role='user')
def journal_view():
  journals = journal_controller.fetch_all()
  topics = topic_controller.fetch_all()
  return render_template('pages/user/journal/view.html', role='User', topics=topics, journals=journals)


@home.route('/journal/detail/<id>', methods=['GET'])
@login_required
@role_checker.check_permission(role='user')
def journal_view_detail(id):
  journal = journal_controller.fetch_by_id(journal_id=id)
  topics = topic_controller.fetch_all()
  return render_template('pages/user/journal/detail.html', role='User', topics=topics, journal=journal)


@home.route('/journal/create', methods=['GET', 'POST'])
@login_required
@role_checker.check_permission(role='user')
def journal_create():
  if request.method == 'POST':
    return journal_controller.create(request=request.form, doc=request.files['doc'])
  
  topics = topic_controller.fetch_all()
  return render_template('pages/user/journal/add.html', role='User', topics=topics)


@home.route('/journal/update/<id>', methods=['GET', 'POST'])
@login_required
@role_checker.check_permission(role='user')
def journal_update(id):
  if request.method == 'POST':
    return journal_controller.update(request=request.form, doc=request.files['doc'])
  
  topics = topic_controller.fetch_all()
  journal = journal_controller.fetch_by_id(journal_id=id)
  return render_template('pages/user/journal/edit.html', role='User', topics=topics, journal=journal)


@home.route('/journal/delete', methods=['POST'])
@login_required
@role_checker.check_permission(role='user')
def journal_delete():
  journal_controller.delete(request=request.form)
  return redirect(url_for('home.journal_view'))


@home.route('/journal/download/<filename>', methods=['GET'])
@login_required
@role_checker.check_permission(role='user')
def journal_download(filename):
  return journal_controller.download(filename)
  