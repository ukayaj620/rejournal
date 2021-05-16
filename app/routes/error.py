from flask import Blueprint, render_template

error = Blueprint('error', __name__, template_folder='templates')

@error.route('/unauthorized', methods=['GET'])
def unauthorized():
  return render_template('error/401.html')