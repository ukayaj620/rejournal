from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.controllers.auth import AuthController

base = Blueprint('base', __name__, template_folder='templates')
auth_controller = AuthController()

@base.route('/', methods=['GET'])
def index():
  if current_user.is_authenticated:
    return auth_controller.determine_redirection(role_id=current_user.role_id)
  return render_template('pages/about.html')


@base.route('/profile', methods=['GET'])
@login_required
def profile():
  return render_template('/pages/profile.html', role=auth_controller.get_role_name(current_user.role_id).capitalize())
