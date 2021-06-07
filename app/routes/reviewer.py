from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.controllers.auth import AuthController
from app.controllers.journal import JournalController
from app.controllers.topic import TopicController
from app.middlewares.role_checker import RoleChecker


reviewer = Blueprint('reviewer', __name__, template_folder='templates')
role_checker = RoleChecker()
journal_controller = JournalController()
topic_controller = TopicController()

@reviewer.route('/', methods=['GET'])
@login_required
@role_checker.check_permission(role='reviewer')
def index():
  return render_template('pages/index.html', role='Reviewer')

@reviewer.route('/manuscript/submission', methods=['GET'])
@login_required
@role_checker.check_permission(role='reviewer')
def manuscript_submission():
  manuscripts = journal_controller.fetch_by_status(status='Submitted')
  topics = topic_controller.fetch_all()
  return render_template('pages/reviewer/manuscript/submission.html', role='Reviewer', manuscripts=manuscripts, topics=topics)

  