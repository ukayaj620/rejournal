from flask import Blueprint, render_template
from flask_login import login_required

base = Blueprint('base', __name__, template_folder='templates')

@base.route('/', methods=['GET'])
def index():
  return render_template('pages/about.html')
