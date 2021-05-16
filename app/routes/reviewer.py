from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.controllers.auth import AuthController

reviewer = Blueprint('reviewer', __name__, template_folder='templates')

@reviewer.route('/', methods=['GET'])
@login_required
def index():
  return render_template('pages/index.html', role='Reviewer')

