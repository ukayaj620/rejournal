from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from app.controllers.auth import AuthController
from app.controllers.user import UserController
from app.controllers.topic import TopicController
from app.controllers.journal import JournalController
from app.controllers.applicant import ApplicantController


base = Blueprint('base', __name__, template_folder='templates')
auth_controller = AuthController()
user_controller = UserController()
topic_controller = TopicController()
journal_controller = JournalController()
applicant_controller = ApplicantController()

@base.route('/', methods=['GET'])
def index():
  topics = topic_controller.fetch_all()
  if current_user.is_authenticated:
    return auth_controller.determine_redirection(role_id=current_user.role_id)
  return render_template('pages/about.html', topics=topics)


@base.route('/applicant', methods=['GET', 'POST'])
def application():
  topics = topic_controller.fetch_all()
  if request.method == 'POST':
    applicant_controller.apply(request=request.form, cv=request.files['cv'])
    return redirect(url_for('base.application'))
  return render_template('pages/applicant.html', topics=topics)


@base.route('/profile', methods=['GET'])
@login_required
def profile():
  print(user_controller.get_profile(user_id=current_user.id).picture_path)
  return render_template(
    '/pages/profile/view.html', 
    role=auth_controller.get_role_name(current_user.role_id).capitalize(),
    user=user_controller.get_profile(user_id=current_user.id)
  )


@base.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile_data():
  if request.method == 'POST':
    user_controller.update(request=request.form, user_id=current_user.id)
    return redirect(url_for('base.profile'))

  return render_template(
    '/pages/profile/update.html', 
    role=auth_controller.get_role_name(current_user.role_id).capitalize(),
    user=user_controller.get_profile(user_id=current_user.id)
  )


@base.route('/profile/image/update', methods=['POST'])
@login_required
def update_profile_image():
  return user_controller.update_profile_image(photo=request.files['photo'], user_id=current_user.id)


@base.route('/publication', methods=['GET'])
@login_required
def view_publication():
  journals, publication_year = journal_controller.fetch_publication()
  return render_template(
    '/pages/publication/view.html', 
    role=auth_controller.get_role_name(current_user.role_id).capitalize(), 
    journals=journals, 
    publication_year=publication_year,
    years=list(set(publication_year))[::-1]
  )


@base.route('/publication/detail/<id>', methods=['GET'])
@login_required
def view_publication_detail(id):
  journal = journal_controller.fetch_by_id(journal_id=id)
  return render_template('/pages/publication/detail.html', role=auth_controller.get_role_name(current_user.role_id).capitalize(), journal=journal)

