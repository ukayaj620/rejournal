from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/', methods=['GET'])
def index():
  return render_template('/pages/index.html', role='Admin')
