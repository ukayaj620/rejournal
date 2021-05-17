from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.controllers.auth import AuthController
from app.controllers.user import UserController


base = Blueprint('base', __name__, template_folder='templates')
auth_controller = AuthController()
user_controller = UserController()

@base.route('/', methods=['GET'])
def index():
  if current_user.is_authenticated:
    return auth_controller.determine_redirection(role_id=current_user.role_id)
  return render_template('pages/about.html')


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

