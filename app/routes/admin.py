from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.middlewares.role_checker import RoleChecker
from app.controllers.topic import TopicController
from app.controllers.journal import JournalController
from app.controllers.user import UserController

admin = Blueprint('admin', __name__, template_folder='templates')
role_checker = RoleChecker()

topic_controller = TopicController()
user_controller = UserController()
journal_controller = JournalController()

@admin.route('/', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def index():
  metrics = {
    'topic': len(topic_controller.topic.query.all()),
    'manuscript': len(journal_controller.fetch_by_status(status='Submitted'))
  }
  return render_template('pages/admin/index.html', metrics=metrics, role='Admin')


@admin.route('/topic', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def view_topic():
  topics = topic_controller.fetch_all()
  return render_template('pages/admin/topic/view.html', topics=topics, role='Admin')


@admin.route('/topic/create', methods=['POST'])
@login_required
@role_checker.check_permission(role='admin')
def create_topic():
  topic_controller.create(request=request.form)
  return redirect(url_for('admin.view_topic'))


@admin.route('/topic/update/<int:id>', methods=['POST'])
@login_required
@role_checker.check_permission(role='admin')
def update_topic(id):
  topic_controller.update(request=request.form, topic_id=id)
  return redirect(url_for('admin.view_topic'))


@admin.route('/topic/delete/<int:id>', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def delete_topic(id):
  topic_controller.delete(topic_id=id)
  return redirect(url_for('admin.view_topic'))

@admin.route('/user', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def view_admin():
  admins = user_controller.fetch_user_by_role(role='admin')
  return render_template('/pages/admin/admin/view.html', admins=admins, role='Admin')


@admin.route('/user/create', methods=['POST'])
@login_required
@role_checker.check_permission(role='admin')
def create_admin():
  user_controller.create(request=request.form, role='admin')
  return redirect(url_for('admin.view_admin'))


@admin.route('/user/update/<int:id>', methods=['POST'])
@login_required
@role_checker.check_permission(role='admin')
def update_admin(id):
  user_controller.update(request=request.form, user_id=id)
  return redirect(url_for('admin.view_admin'))


@admin.route('/user/delete/<int:id>', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def delete_admin(id):
  user_controller.delete(user_id=id)
  return redirect(url_for('admin.view_admin'))


@admin.route('/reviewer', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def view_reviewer():
  reviewers = user_controller.fetch_user_by_role(role='reviewer')
  topics = topic_controller.fetch_all()
  return render_template('/pages/admin/reviewer/view.html', reviewers=reviewers, role='Admin', topics=topics)


@admin.route('/reviewer/create', methods=['POST'])
@login_required
@role_checker.check_permission(role='admin')
def create_reviewer():
  user_controller.create(request=request.form, role='reviewer')
  return redirect(url_for('admin.view_reviewer'))


@admin.route('/reviewer/update/<int:id>', methods=['POST'])
@login_required
@role_checker.check_permission(role='admin')
def update_reviewer(id):
  user_controller.update(request=request.form, user_id=id)
  return redirect(url_for('admin.view_reviewer'))


@admin.route('/reviewer/delete/<int:id>', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def delete_reviewer(id):
  user_controller.delete(user_id=id)
  return redirect(url_for('admin.view_reviewer'))
