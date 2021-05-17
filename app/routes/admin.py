from flask import Blueprint, render_template, request
from flask_login import login_required
from app.middlewares.role_checker import RoleChecker
from app.controllers.topic import TopicController
from app.controllers.user import UserController

admin = Blueprint('admin', __name__, template_folder='templates')
role_checker = RoleChecker()

topic_controller = TopicController()
user_controller = UserController()

@admin.route('/', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def index():
  return render_template('pages/index.html', role='Admin')


@admin.route('/topic', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def view_topic():
  return topic_controller.fetch_all()


@admin.route('/topic/create', methods=['POST'])
@login_required
@role_checker.check_permission(role='admin')
def create_topic():
  return topic_controller.create(request=request.form)


@admin.route('/topic/update/<int:id>', methods=['POST'])
@login_required
@role_checker.check_permission(role='admin')
def update_topic(id):
  return topic_controller.update(request=request.form, topic_id=id)


@admin.route('/topic/delete/<int:id>', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def delete_topic(id):
  return topic_controller.delete(topic_id=id)


@admin.route('/user', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def view_admin():
  admins = user_controller.fetch_user_by_role(role='admin')
  return render_template('/pages/admin/admin/view.html', admins=admins, role='Admin')

