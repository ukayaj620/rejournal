from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.controllers.auth import AuthController
from app.middlewares.role_checker import RoleChecker

reviewer = Blueprint('reviewer', __name__, template_folder='templates')
role_checker = RoleChecker()

@reviewer.route('/', methods=['GET'])
@login_required
@role_checker.check_permission(role='reviewer')
def index():
  return render_template('pages/index.html', role='Reviewer')

